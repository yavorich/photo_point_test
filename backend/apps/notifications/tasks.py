from celery import shared_task
from django.utils import timezone
from apps.notifications.models import (
    NotificationStatus,
    NotificationReceiver,
)
from apps.notifications.services import NotificationService


@shared_task
def send_notification_to_user(notification_id, user_id):
    receiver = NotificationReceiver.objects.select_related("notification", "user").get(
        notification_id=notification_id, user_id=user_id
    )
    notification = receiver.notification
    user = receiver.user

    channel = NotificationService.send_to_user(user, notification.message)

    if channel:
        receiver.channel = channel
        receiver.status = NotificationStatus.SENT
        receiver.sent_at = timezone.now()
    else:
        receiver.status = NotificationStatus.FAILED

    receiver.save()
    notification.update_log()
