from Education_system.models import UserCourseAccess, Group

from django.utils import timezone
from django.db import transaction


def distribute_users_to_groups(user_course_access: UserCourseAccess):

    course = user_course_access.course
    user = user_course_access.user
    groups = Group.objects.filter(course=course)

    filtered_groups = Group.objects.filter(users__count__lt=groups.max_users).order_by('users__count')

    if not filtered_groups:
        raise ValueError("Достигнуто максимальное количество пользователей во всех группах.")


    with transaction.atomic():
        if course.start_date > timezone.now():
            sorted_groups = groups.order_by("users__count")
            target_group = sorted_groups.first()
            target_group.users.add(user)

            target_group.save()

        else:
            first_group = groups.first()
            first_group.users.add(user)
            first_group.save()

        user_course_access.save()
