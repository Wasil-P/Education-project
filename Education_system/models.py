from Users.models import User

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


def validate_date(date):
    if date <= timezone.now().date():
        raise ValidationError


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(validators=[validate_date])
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_users = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField()

    class Meta:
        db_table = "course"

    def __str__(self):
        return self.name


class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_course_access"


@receiver([post_save], sender=UserCourseAccess)
def target(sender, instance: UserCourseAccess, **kwargs):
    from .run import distribute_users_to_groups
    distribute_users_to_groups(instance)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson_course")
    name = models.CharField(max_length=255)
    link_to_video = models.URLField(max_length=200)

    class Meta:
        db_table = "lesson"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="group_course")
    users = models.ManyToManyField(User, related_name="group_users")

    @property
    def is_available_to_add_user(self):
        return self.course.max_users > len(self.users.all()) and self.course.min_users > len(self.users.all())

    class Meta:
        db_table = "group"

    def __str__(self):
        return self.name
