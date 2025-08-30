from django.db import models
from django.conf import settings


class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    emoji = models.CharField(max_length=8, blank=True)
    completion_percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, blank=True)  # e.g., A1
    word_count = models.PositiveIntegerField(null=True, blank=True)
    content = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category.slug})"


class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    percent = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class XpEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reason = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
