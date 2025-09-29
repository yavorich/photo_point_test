from django.db import models, transaction
from django.utils import timezone

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

    @property
    def last_log(self):
        return self.logs.order_by("-started_at").first()

    def update_log(self):
        # Берём последний незавершённый лог
        with transaction.atomic():
            log = (
                NotificationLog.objects.select_for_update()
                .filter(notification=self, finished_at__isnull=True)
                .order_by("-started_at")
                .first()
            )
            if not log:
                return  # Нет активного лога

            # Получаем receivers запросом к базе, чтобы не было проблем синхронизации
            total_sent = self.receivers.filter(status=NotificationStatus.SENT).count()
            total_failed = self.receivers.filter(
                status=NotificationStatus.FAILED
            ).count()

            updates = {
                "total_sent": total_sent,
                "total_failed": total_failed,
            }

            # Если все отправки выполнены — закрываем лог
            if total_sent + total_failed == log.total_users:
                now = timezone.now()
                updates.update(
                    {
                        "finished_at": now,
                        "duration_seconds": (now - log.started_at).total_seconds(),
                    }
                )

            NotificationLog.objects.filter(pk=log.pk).update(**updates)


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


class NotificationLog(models.Model):
    notification = models.ForeignKey(
        Notification,
        related_name="logs",
        on_delete=models.CASCADE,
    )
    started_at = models.DateTimeField(auto_now_add=True)
    total_users = models.PositiveIntegerField("Всего получателей", default=0)
    total_sent = models.PositiveIntegerField("Отправлено", default=0)
    total_failed = models.PositiveIntegerField("Ошибки", default=0)
    duration_seconds = models.FloatField("Время выполнения (c)", null=True, blank=True)
    finished_at = models.DateTimeField("Завершено", null=True, blank=True)

    class Meta:
        verbose_name = "История рассылки"
        verbose_name_plural = "Истории рассылок"

    def __str__(self):
        return f"Log {self.notification_id} at {self.started_at:%Y-%m-%d %H:%M:%S}"

    @property
    def in_progress(self):
        return self.finished_at is None
