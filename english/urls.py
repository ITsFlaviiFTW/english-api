from django.urls import path
from .views import HealthView, RegisterView, LoginView, MeView, MeSummaryView
from . import views
from .views_catalog import CategoriesView, CategoryDetailView, CategoryLessonsView, LessonDetailView

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("me/summary/", MeSummaryView.as_view()),

        # Catalog (read-only)
    path("categories/", CategoriesView.as_view()),
    path("categories/<slug:slug>/", CategoryDetailView.as_view()),
    path("categories/<slug:slug>/lessons/", CategoryLessonsView.as_view()),
    path("lessons/<int:pk>/", LessonDetailView.as_view()),
]
