# english/views_catalog.py
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Lesson
from .serializers import CategorySerializer, LessonListSerializer, LessonDetailSerializer


class CategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = Category.objects.all().order_by("title")
        data = CategorySerializer(qs, many=True, context={"request": request}).data
        return Response(data)  # <-- array


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        cat = get_object_or_404(Category, slug=slug)
        return Response(CategorySerializer(cat, context={"request": request}).data)


class CategoryLessonsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        cat = get_object_or_404(Category, slug=slug)
        lessons = Lesson.objects.filter(category=cat).order_by("id")
        return Response(LessonListSerializer(lessons, many=True).data)  # <-- array


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        return Response(LessonDetailSerializer(lesson).data)
