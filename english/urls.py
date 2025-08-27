from django.urls import path
from .views import HealthView, RegisterView, LoginView, MeView, MeSummaryView
from . import views

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("me/summary/", MeSummaryView.as_view()),
]
