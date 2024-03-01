from ..models import Lesson, Course
from .serializers import CourseModelSerializer, CourseLessonsSerializer

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseModelSerializer

    def get_queryset(self):
        return Course.objects.filter(start_date__gt=timezone.now().date())\
            .order_by('start_date')


class CourseLessonsListAPIView(generics.ListAPIView):
    serializer_class = CourseLessonsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(course__usercourseaccess__user=user)
