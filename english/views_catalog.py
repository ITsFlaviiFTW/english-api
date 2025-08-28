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
        return Response({"results": CategorySerializer(qs, many=True).data})

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        cat = get_object_or_404(Category, slug=slug)
        return Response(CategorySerializer(cat).data)

class CategoryLessonsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        cat = get_object_or_404(Category, slug=slug)
        lessons = Lesson.objects.filter(category=cat).order_by("id")
        return Response({"results": LessonListSerializer(lessons, many=True).data})

class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        return Response(LessonDetailSerializer(lesson).data)
