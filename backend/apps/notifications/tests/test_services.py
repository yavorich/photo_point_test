import pytest
from apps.notifications.services import (
    NotificationService,
    NotificationChannel,
    SmsRuApi,
)

import pytest
from apps.notifications.services import NotificationService
from apps.notifications.models import NotificationChannel


@pytest.mark.django_db
def test_send_telegram_success(mocker, user):
    # mock class for MAIN_BOT
    class MockBot:
        async def send_message(self, chat_id, text):
            self.chat_id = chat_id
            self.text = text
            return None

    mock_bot = MockBot()
    mocker.patch("apps.notifications.services.MAIN_BOT", mock_bot)

    result = NotificationService.send_telegram(user, "Hello")
    assert result == NotificationChannel.TELEGRAM
    assert mock_bot.chat_id == user.telegram_id
    assert mock_bot.text == "Hello"


@pytest.mark.django_db
def test_send_email_success(mocker, user):
    mocker.patch("apps.notifications.services.send_mail", return_value=1)
    result = NotificationService.send_email(user, "Hello")
    assert result == NotificationChannel.EMAIL


@pytest.mark.django_db
def test_send_sms_success(mocker, user):
    phone = SmsRuApi().beautify_phone(str(user.phone))
    mock_response = {phone: {"status": True}}
    mocker.patch(
        "apps.notifications.services.SmsRuApi.send_one_sms", return_value=mock_response
    )

    result = NotificationService.send_sms(user, "Hello")
    assert result == NotificationChannel.SMS


@pytest.mark.django_db
def test_send_to_user_priority(mocker, user):
    mocker.patch(
        "apps.notifications.services.NotificationService.send_telegram",
        return_value=None,
    )
    mocker.patch(
        "apps.notifications.services.NotificationService.send_sms",
        return_value=NotificationChannel.SMS,
    )
    mocker.patch(
        "apps.notifications.services.NotificationService.send_email",
        return_value=NotificationChannel.EMAIL,
    )

    result = NotificationService.send_to_user(user, "Hello")
    assert result == NotificationChannel.SMS
