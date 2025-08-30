import random
from typing import Any, Dict, List, Tuple

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Lesson, QuizAttempt, XpEvent


def _extract_quiz_items(lesson: Lesson) -> List[Dict[str, Any]]:
    """
    Expect lesson.content["quiz"]["items"] list.
    """
    content = lesson.content or {}
    quiz = content.get("quiz") or {}
    items = quiz.get("items") or []
    return items


def _grade_answer(item: Dict[str, Any], selected: Any) -> bool:
    t = item.get("type")

    if t == "choose":
        t = "mcq"
    if t == "fill_blank":
        t = "fill"

    if t == "mcq":
        correct_idx = item.get("correct_index")
        try:
            return int(selected.get("index")) == int(correct_idx)
        except Exception:
            return False

    if t == "tf":
        correct = item.get("correct_bool")
        return bool(selected.get("value")) is bool(correct)

    if t == "fill":
        ans = item.get("answer")
        answers = item.get("answers") or ([] if ans is None else [ans])
        user_text = (selected.get("text") or "").strip().lower()
        normalized = [str(a).strip().lower() for a in answers]
        return user_text in normalized

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
            t = it.get("type")
            if t == "choose":
                t = "mcq"
            if t == "fill_blank":
                t = "fill"
            payload = {}
            if t == "mcq":
                payload = {"options": it.get("options") or []}
            elif t == "fill":
                payload = {"blanks": 1}
            elif t == "tf":
                payload = {}
            out.append({
                "id": qid,
                "lesson_id": lesson_id,
                "prompt": it.get("prompt_en") or it.get("prompt_ro") or "",
                "qtype": t,
                "payload": payload,
            })
            qid += 1

        return Response({"items": out})
