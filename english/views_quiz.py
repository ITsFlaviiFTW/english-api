# english/views_quiz.py
import random
import re
import unicodedata
from typing import Any, Dict, List, Tuple

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lesson, QuizAttempt, XpEvent, LessonProgress

_WS_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]")  # remove punctuation except letters/digits/space


def strip_diacritics(s: str) -> str:
    if not isinstance(s, str):
        s = str(s or "")
    nfd = unicodedata.normalize("NFD", s)
    no_marks = "".join(ch for ch in nfd if not unicodedata.combining(ch))
    return (
        no_marks
        .replace("ș", "s").replace("Ş", "S").replace("Ș", "S")
        .replace("ț", "t").replace("Ţ", "T").replace("Ț", "T")
        .replace("ă", "a").replace("Ă", "A")
        .replace("â", "a").replace("Â", "A")
        .replace("î", "i").replace("Î", "I")
    )


def norm_text(s: str) -> str:
    s = strip_diacritics(s or "")
    s = s.lower().strip()
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s)
    return s


def _normalize_type(t: str) -> str:
    t = (t or "").lower()
    if t in ("choose", "dialogue_reply", "mcq"):
        return "mcq"
    if t in ("tf", "true_false"):
        return "tf"
    if t in ("fill_blank", "fill"):
        return "fill"
    if t in ("translate_ro_en", "translate_en_ro", "word_order", "build"):
        return "build"
    return t


def _extract_quiz_items(lesson: Lesson) -> List[Dict[str, Any]]:
    content = lesson.content or {}
    quiz = content.get("quiz") or {}
    return quiz.get("items") or []


def _expected_texts(item: Dict[str, Any]) -> List[str]:
    vals: List[str] = []
    for k in ("answer_en", "answer_ro", "answer", "expected", "solution"):
        v = item.get(k)
        if isinstance(v, str) and v:
            vals.append(v)
    for k in ("answers", "accept", "accept_en", "answer_variants"):
        v = item.get(k)
        if isinstance(v, list):
            vals.extend([x for x in v if isinstance(x, str) and x])
    out, seen = [], set()
    for s in vals:
        ns = norm_text(s)
        if ns and ns not in seen:
            seen.add(ns)
            out.append(ns)
    return out


def _tokens_to_text(selected: Dict[str, Any]) -> str:
    toks = selected.get("tokens")
    if isinstance(toks, list) and toks:
        return " ".join(str(t) for t in toks)
    return selected.get("text") or ""


def _grade_answer(item: Dict[str, Any], selected: Any) -> bool:
    t = _normalize_type(item.get("type"))

    if t == "mcq":
        correct_idx = (
            item.get("correct_index")
            if item.get("correct_index") is not None
            else None
        )
        if correct_idx is None:
            options = item.get("options") or []
            correct_text = item.get("correct")
            if correct_text is not None and correct_text in options:
                correct_idx = options.index(correct_text)
        try:
            return int(selected.get("index")) == int(correct_idx)
        except Exception:
            return False

    if t == "tf":
        correct = item.get("correct_bool")
        if correct is None:
            correct = item.get("answer_bool")
        if correct is None:
            correct = item.get("correct")
        return bool(selected.get("value")) is bool(correct)

    if t == "fill":
        ans = item.get("answer")
        answers = item.get("answers") or ([] if ans is None else [ans])
        accept = item.get("accept") or []
        expected_norms = [norm_text(a) for a in (answers + accept) if a]
        cand = norm_text(selected.get("text") or "")
        return cand in expected_norms

    if t == "build":
        cand_raw = _tokens_to_text(selected)
        cand_norm = norm_text(cand_raw)
        if not cand_norm:
            return False
        expected_norms = _expected_texts(item)
        return cand_norm in expected_norms

    return False


class QuizAttemptView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        lesson_id = request.data.get("lesson_id")
        answers = request.data.get("answers") or []

        if lesson_id is None or not isinstance(answers, list):
            return Response({"detail": "lesson_id and answers[] are required"}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        items = _extract_quiz_items(lesson)
        if not items:
            return Response({"detail": "Lesson has no quiz items"}, status=status.HTTP_400_BAD_REQUEST)

        ans_by_id: Dict[int, Dict[str, Any]] = {}
        for a in answers:
            try:
                ans_by_id[int(a.get("question_id"))] = a
            except Exception:
                continue

        results: List[Dict[str, Any]] = []
        correct = 0
        total = len(items)

        for idx, it in enumerate(items, start=1):
            sel = (ans_by_id.get(idx) or {}).get("selected") or {}
            ok = _grade_answer(it, sel)
            results.append({"question_id": idx, "is_correct": bool(ok)})
            if ok:
                correct += 1

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

        lp, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
        lp.percent = max(lp.percent or 0, score_pct)
        lp.save()

        return Response({"score_pct": score_pct, "xp_delta": xp_delta, "results": results})


class RandomQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = int(request.query_params.get("size", 10))
        category_id = request.query_params.get("category_id")

        qs = Lesson.objects.all()
        if category_id:
            qs = qs.filter(category_id=category_id)

        pool: List[Tuple[int, int, Dict[str, Any]]] = []
        for lesson in qs.order_by("-created_at")[:100]:
            items = _extract_quiz_items(lesson)
            for idx, it in enumerate(items, start=1):
                pool.append((lesson.id, idx, it))

        if not pool:
            return Response({"items": []})

        sample = random.sample(pool, k=min(size, len(pool)))

        out = []
        qid = 1
        for lesson_id, item_index, it in sample:
            t = _normalize_type(it.get("type"))
            prompt = it.get("prompt_en") or it.get("prompt_ro") or ""

            if t == "mcq":
                payload = {"options": it.get("options") or []}
                qtype = "mcq"
            elif t == "tf":
                payload = {}
                qtype = "tf"
            elif t == "build":
                expected = (
                    it.get("answer_en")
                    or it.get("answer_ro")
                    or it.get("answer")
                    or it.get("expected")
                    or ""
                )
                tokens = it.get("tokens") or expected.split()
                shuf = tokens[:]
                random.shuffle(shuf)
                payload = {"tokens": shuf}
                qtype = "build"
            else:
                payload = {"blanks": 1}
                qtype = "fill"

            out.append({
                "id": qid,
                "lesson_id": lesson_id,
                "item_index": item_index,
                "prompt": prompt,
                "qtype": qtype,
                "payload": payload,
            })
            qid += 1

        return Response({"items": out})


class RandomQuizAttemptView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        entries = request.data.get("answers") or []
        if not isinstance(entries, list) or not entries:
            return Response({"detail": "answers[] required"}, status=status.HTTP_400_BAD_REQUEST)

        by_lesson: Dict[int, List[Dict[str, Any]]] = {}
        for e in entries:
            try:
                lid = int(e.get("lesson_id"))
                by_lesson.setdefault(lid, []).append(e)
            except Exception:
                continue

        total = 0
        correct = 0
        results: List[Dict[str, Any]] = []

        for lesson_id, group in by_lesson.items():
            lesson = get_object_or_404(Lesson, pk=lesson_id)
            items = _extract_quiz_items(lesson)

            t_this = 0
            c_this = 0
            for e in group:
                qid = int(e.get("qid"))
                idx = int(e.get("item_index"))  # 1-based
                selected = e.get("selected") or {}
                it = items[idx - 1] if 1 <= idx <= len(items) else None
                ok = _grade_answer(it, selected) if it else False
                results.append({"qid": qid, "is_correct": bool(ok)})
                t_this += 1
                if ok:
                    c_this += 1

            total += t_this
            correct += c_this

            if t_this:
                QuizAttempt.objects.create(
                    user=request.user,
                    lesson=lesson,
                    total_questions=t_this,
                    correct_answers=c_this,
                )
                pct = int(round(100 * c_this / t_this))
                lp, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
                lp.percent = max(lp.percent or 0, pct)
                lp.save()

        xp_delta = correct * 10
        if xp_delta:
            XpEvent.objects.create(user=request.user, amount=xp_delta, reason="Random quiz")

        score_pct = int(round(100 * correct / total)) if total else 0
        return Response({"score_pct": score_pct, "xp_delta": xp_delta, "results": results})
