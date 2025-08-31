import random
from typing import Any, Dict, List, Tuple

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Lesson, QuizAttempt, XpEvent

import re
import unicodedata



_WS_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]")  # remove punctuation except letters/digits/space

def strip_diacritics(s: str) -> str:
    # NFD split + drop combining marks; covers Romanian safely
    if not isinstance(s, str):
        s = str(s or "")
    nfd = unicodedata.normalize("NFD", s)
    no_marks = "".join(ch for ch in nfd if not unicodedata.combining(ch))
    # map Romanian special letters that aren’t combining-based in some fonts
    return (
        no_marks
        .replace("ș", "s").replace("Ş", "S").replace("ț", "t").replace("Ţ", "T")
        .replace("ă", "a").replace("Ă", "A")
        .replace("â", "a").replace("Â", "A")
        .replace("î", "i").replace("Î", "I")
    )

def norm_text(s: str) -> str:
    s = strip_diacritics(s or "")
    s = s.lower().strip()
    s = _PUNCT_RE.sub(" ", s)      # remove punctuation
    s = _WS_RE.sub(" ", s)         # collapse whitespace
    return s




def _extract_quiz_items(lesson: Lesson) -> List[Dict[str, Any]]:
    """
    Expect lesson.content["quiz"]["items"] list.
    """
    content = lesson.content or {}
    quiz = content.get("quiz") or {}
    items = quiz.get("items") or []
    return items


def _grade_answer(item: Dict[str, Any], selected: Any) -> bool:
    t = (item.get("type") or "").lower()

    # normalize aliases
    if t == "choose":
        t = "mcq"
    if t == "fill_blank":
        # these can be MCQ if options exist; otherwise it's free text
        t = "mcq" if item.get("options") else "fill"

    # ---------- MCQ ----------
    if t in ("mcq", "dialogue_reply"):
        # selected is {"index": int}
        correct_idx = item.get("correct_index")
        if correct_idx is None:
            # allow seeds that store a 'correct' option text instead of index
            options = item.get("options") or []
            correct_text = item.get("correct")
            if correct_text is not None and correct_text in options:
                correct_idx = options.index(correct_text)
        try:
            return int(selected.get("index")) == int(correct_idx)
        except Exception:
            return False

    # ---------- True/False ----------
    if t in ("tf", "true_false"):
        # selected is {"value": bool}
        correct = item.get("correct_bool")
        if correct is None:
            correct = item.get("answer_bool")
        if correct is None:
            correct = item.get("correct")
        return bool(selected.get("value")) is bool(correct)

    # ---------- Free text fill ----------
    if t == "fill":
        # selected is {"text": str}
        ans = item.get("answer")
        answers = item.get("answers") or ([] if ans is None else [ans])
        accept = item.get("accept") or []
        normalized_expected = [norm_text(a) for a in (answers + accept) if a]
        user_text = norm_text(selected.get("text") or "")
        return user_text in normalized_expected

    if t in ("translate_ro_en", "translate_en_ro", "word_order"):
        expected = (
            item.get("answer_en")
            or item.get("answer_ro")
            or item.get("answer")
            or item.get("expected")
        )
        accept = item.get("accept") or []
        user_text = norm_text(selected.get("text") or "")
        normalized_expected = [norm_text(expected or "")]
        normalized_expected += [norm_text(a) for a in accept]
        return user_text in normalized_expected

    return False


class QuizAttemptView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        """
        Input:
          { lesson_id: int,
            answers: [ {question_id:int, selected:{...}} ]
          }
        Output:
          { score_pct, xp_delta, results:[{question_id,is_correct}] }
        """
        lesson_id = request.data.get("lesson_id")
        answers = request.data.get("answers") or []

        if lesson_id is None or not isinstance(answers, list):
            return Response({"detail": "lesson_id and answers[] are required"}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        items = _extract_quiz_items(lesson)
        if not items:
            return Response({"detail": "Lesson has no quiz items"}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        correct = 0
        total = 0

        item_by_id: Dict[int, Dict[str, Any]] = {}
        for idx, it in enumerate(items, start=1):
            item_by_id[idx] = it

        for a in answers:
            qid = a.get("question_id")
            sel = a.get("selected") or {}
            it = item_by_id.get(int(qid)) if qid is not None else None
            if it is None:
                continue
            is_correct = _grade_answer(it, sel)
            results.append({"question_id": int(qid), "is_correct": bool(is_correct)})
            total += 1
            if is_correct:
                correct += 1

        if total == 0:
            total = len(items)
            results = [{"question_id": i, "is_correct": False} for i in range(1, total + 1)]

        score_pct = int(round(100 * correct / total)) if total else 0
        xp_delta = correct * 10

        QuizAttempt.objects.create(
            user=request.user,
            lesson=lesson,
            total_questions=total,
            correct_answers=correct,
        )
        if xp_delta:
            XpEvent.objects.create(user=request.user, amount=xp_delta, reason=f"Lesson {lesson.id} quiz")

        return Response({
            "score_pct": score_pct,
            "xp_delta": xp_delta,
            "results": results,
        })


class RandomQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return a mixed quiz across lessons.
        Query params:
          size: total questions (default 10)
          category_id: optional filter
        """
        size = int(request.query_params.get("size", 10))
        category_id = request.query_params.get("category_id")

        qs = Lesson.objects.all()
        if category_id:
            qs = qs.filter(category_id=category_id)

        pool: List[Tuple[int, Dict[str, Any]]] = []
        for lesson in qs.order_by("-created_at")[:100]:
            for it in _extract_quiz_items(lesson):
                pool.append((lesson.id, it))

        if not pool:
            return Response({"items": []})

        sample = random.sample(pool, k=min(size, len(pool)))

        out = []
        qid = 1
        for lesson_id, it in sample:
            t = (it.get("type") or "").lower()

            # normalize
            if t == "choose":
                qtype = "mcq"
            elif t == "fill_blank":
                qtype = "fill"
            elif t in ("tf", "true_false"):
                qtype = "tf"
            elif t in ("translate_ro_en", "translate_en_ro", "word_order"):
                qtype = "build"
            else:
                # unknown; skip this item
                continue

            prompt = it.get("prompt_en") or it.get("prompt_ro") or ""

            payload = {}
            if qtype == "mcq":
                payload = {"options": it.get("options") or []}
            elif qtype == "fill":
                payload = {"blanks": 1}
            elif qtype == "build":
                # derive tokens (prefer seed 'tokens', else split the expected answer)
                expected = (
                    it.get("answer_en")
                    or it.get("answer_ro")
                    or it.get("answer")
                    or ""
                )
                tokens = it.get("tokens") or expected.split()
                shuf = tokens[:]  # do not mutate original
                random.shuffle(shuf)
                payload = {"tokens": shuf}

            out.append({
                "id": qid,
                "lesson_id": lesson_id,
                "prompt": prompt,
                "qtype": qtype,
                "payload": payload,
            })
            qid += 1

        return Response({"items": out})
