import pytest

from apps.notifications.models import NotificationChannel, NotificationStatus
from apps.notifications.tasks import send_notification_to_user
from apps.notifications.services import NotificationService


@pytest.mark.django_db
def test_send_notification_task_sms_success(mocker, notification_with_receiver):
    notification, receiver = notification_with_receiver

    mocker.patch(
        "apps.notifications.services.NotificationService.send_to_user",
        return_value=NotificationChannel.SMS,
    )

    send_notification_to_user(notification.id, receiver.user.id)

    # Проверка обновления receiver
    receiver.refresh_from_db()
    assert receiver.status == NotificationStatus.SENT
    assert receiver.channel == NotificationChannel.SMS
    assert receiver.sent_at is not None


@pytest.mark.django_db
def test_send_notification_task_failed(mocker, notification_with_receiver):
    notification, receiver = notification_with_receiver

    mocker.patch(
        "apps.notifications.services.NotificationService.send_to_user",
        return_value=None,
    )

    send_notification_to_user(notification.id, receiver.user.id)

    receiver.refresh_from_db()
    assert receiver.status == NotificationStatus.FAILED
    assert receiver.channel is None
    assert receiver.sent_at is None
