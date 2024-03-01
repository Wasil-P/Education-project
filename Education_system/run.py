from Education_system.models import UserCourseAccess, Group

from django.utils import timezone
from django.db import transaction
from django.db.models import Count


def distribute_users_to_groups(user_course_access: UserCourseAccess):

    course = user_course_access.course
    user = user_course_access.user
    groups = Group.objects.filter(course=course)

    filtered_groups = Group.objects.annotate(user_count=Count('users')).\
        filter(user_count__lt=course.max_users).order_by('user_count')

    if not filtered_groups:
        last_group = groups.last()
        new_group = Group.objects.create(
            name=str(last_group.name) + "1",
            course=course)
        new_group.users.set([user])

        user_course_access.save()

    if course.start_date > timezone.now():
        with transaction.atomic():
            sorted_groups = groups.annotate(user_count=Count('users')).order_by("user_count")
            target_group = sorted_groups.first()
            target_group.users.add(user)

            target_group.save()


