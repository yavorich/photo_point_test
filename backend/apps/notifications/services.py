import logging
from django.core.mail import send_mail
from smsru.service import SmsRuApi

from apps.accounts.models import User
from apps.notifications.models import NotificationChannel
from config.settings import MAIN_BOT, FROM_EMAIL
from apps.notifications.utils import ptb_async_to_sync

logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    @ptb_async_to_sync
    async def send_telegram(user: User, message: str):
        if not user.telegram_id:
            return None
        await MAIN_BOT.send_message(chat_id=user.telegram_id, text=message)
        return NotificationChannel.TELEGRAM

    @staticmethod
    def send_email(user: User, message: str):
        if not user.email:
            return None
        # Стандартная отправка через SMTP без подтверждения доставки
        # Можно использовать сервисы с подтверждением (SendGrid, MailGun, etc)
        send_mail(
            subject="Уведомление",
            message=message,
            from_email=FROM_EMAIL,
            recipient_list=[user.email],
        )
        return NotificationChannel.EMAIL

    @staticmethod
    def send_sms(user: User, message: str):
        if not user.phone:
            return None
        sms_ru_api = SmsRuApi()
        phone = sms_ru_api.beautify_phone(str(user.phone))
        response = sms_ru_api.send_one_sms(phone, message)
        if response.get(phone, {}).get("status", False):
            return NotificationChannel.SMS
        return None

    @classmethod
    def send_to_user(cls, user, message):
        # Приоритет способов отправки уведомления
        channels = [
            cls.send_telegram,
            cls.send_sms,
            cls.send_email,
        ]

        for channel in channels:
            try:
                result = channel(user, message)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"{channel.__name__} failed for {user.id}: {e}")

        return None
