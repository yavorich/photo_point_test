import pytest
from celery import current_app

from apps.notifications.models import Notification, NotificationReceiver
from apps.accounts.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        password="123456",
        phone="+79001234567",
        telegram_id=123456789,
    )


@pytest.fixture(autouse=True)
def celery_eager():
    # Все задачи Celery будут выполняться синхронно для тестов
    current_app.conf.task_always_eager = True


@pytest.fixture
def notification_with_receiver(db, user):
    notification = Notification.objects.create(message="Test message")
    receiver = NotificationReceiver.objects.create(notification=notification, user=user)
    return notification, receiver