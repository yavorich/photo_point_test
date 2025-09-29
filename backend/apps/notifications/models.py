from django.db import models

from apps.accounts.models import User


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "Ожидает отправки"
    SENT = "sent", "Отправлено"
    FAILED = "failed", "Ошибка"


class NotificationChannel(models.TextChoices):
    TELEGRAM = "telegram", "Telegram"
    EMAIL = "email", "Email"
    SMS = "sms", "SMS"


class Notification(models.Model):
    users = models.ManyToManyField(
        to=User,
        through="notifications.NotificationReceiver",
        related_name="notifications",
    )
    message = models.TextField("Текст уведомления")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Уведомления"
        verbose_name = "Уведомление"

    def __str__(self):
        return f"Уведомление {self.pk}"


class NotificationReceiver(models.Model):
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="receivers"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
    )
    channel = models.CharField(
        "Способ отправки",
        max_length=20,
        choices=NotificationChannel.choices,
        blank=True,
        null=True,
    )
    sent_at = models.DateTimeField("Время отправки", blank=True, null=True)

    def __str__(self):
        return f"{self.user} <- {self.notification}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
