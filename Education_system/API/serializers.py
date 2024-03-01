from ..models import Course, Lesson

from rest_framework import serializers


class CourseModelSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lesson_course.count()

    class Meta:
        model = Course
        fields = ['author', 'name', 'cost', 'lesson_count']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseLessonsSerializer(serializers.ModelSerializer):
    lesson_course = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
