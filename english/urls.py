from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import HealthView, RegisterView, LoginView, MeView, MeSummaryView
from .views_catalog import CategoriesView, CategoryDetailView, CategoryLessonsView, LessonDetailView
from .views_progress import ProgressUpsertView
from .views_quiz import QuizAttemptView, RandomQuizView, RandomQuizAttemptView

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),

    path("me/", MeView.as_view()),
    path("me/summary/", MeSummaryView.as_view()),

    # Catalog
    path("categories/", CategoriesView.as_view()),
    path("categories/<slug:slug>/", CategoryDetailView.as_view()),
    path("categories/<slug:slug>/lessons/", CategoryLessonsView.as_view()),
    path("lessons/<int:pk>/", LessonDetailView.as_view()),

    # Progress + Quiz
    path("progress/", ProgressUpsertView.as_view()),
    path("quiz-attempts/", QuizAttemptView.as_view()),
    path("quiz/random/", RandomQuizView.as_view()),
    path("quiz/random/attempts/", RandomQuizAttemptView.as_view()),
]
