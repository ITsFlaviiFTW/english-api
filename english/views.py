# english/views.py
from datetime import timedelta

from django.apps import apps
from django.contrib.auth import authenticate
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, _):
        return Response({"ok": True})


def _tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        access, refresh = _tokens_for_user(user)
        return Response(
            {"access": access, "refresh": refresh, "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        access, refresh = _tokens_for_user(user)
        return Response({"access": access, "refresh": refresh, "user": UserSerializer(user).data})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class MeSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        LessonProgress = apps.get_model("english", "LessonProgress", require_ready=False)
        QuizAttempt = apps.get_model("english", "QuizAttempt", require_ready=False)
        XpEvent = apps.get_model("english", "XpEvent", require_ready=False)

        completed_lessons = 0
        accuracy = 0
        xp = 0
        streak = 0

        if LessonProgress:
            completed_lessons = LessonProgress.objects.filter(user=user, percent__gte=100).count()

        total_q = correct_q = 0
        if QuizAttempt:
            agg = QuizAttempt.objects.filter(user=user).aggregate(
                total_q=Coalesce(Sum("total_questions"), 0),
                correct_q=Coalesce(Sum("correct_answers"), 0),
            )
            total_q = agg.get("total_q") or 0
            correct_q = agg.get("correct_q") or 0
            accuracy = int(round(100 * correct_q / total_q)) if total_q else 0

        if XpEvent:
            xp = XpEvent.objects.filter(user=user).aggregate(total=Coalesce(Sum("amount"), 0)).get("total") or 0
        else:
            xp = correct_q * 10

        level = 1 + xp // 100

        if LessonProgress or QuizAttempt:
            days = set()
            if LessonProgress:
                for d in LessonProgress.objects.filter(user=user).values_list("updated_at", flat=True):
                    if d:
                        days.add(d.date())
            if QuizAttempt:
                for d in QuizAttempt.objects.filter(user=user).values_list("created_at", flat=True):
                    if d:
                        days.add(d.date())
            today = timezone.localdate()
            cur = today
            while cur in days:
                streak += 1
                cur -= timedelta(days=1)

        return Response({
            "username": user.username,
            "display_name": getattr(user, "first_name", "") or user.username,
            "avatar_url": "",
            "xp": xp,
            "level": level,
            "streak": streak,
            "completedLessons": completed_lessons,
            "accuracy": accuracy,
        })
