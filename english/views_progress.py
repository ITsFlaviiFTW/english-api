# english/views_progress.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lesson, LessonProgress


class ProgressUpsertView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Input: { lesson_id: int, percent: int }
        """
        lesson_id = request.data.get("lesson_id")
        percent = request.data.get("percent")

        if lesson_id is None or percent is None:
            return Response({"detail": "lesson_id and percent are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            percent = int(percent)
            if percent < 0 or percent > 100:
                raise ValueError
        except Exception:
            return Response({"detail": "percent must be an integer between 0 and 100"}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lp, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
        lp.percent = percent
        lp.save()
        return Response({"ok": True, "percent": lp.percent})
