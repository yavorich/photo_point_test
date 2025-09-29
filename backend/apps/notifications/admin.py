from celery import group
from django.contrib import admin
from django.utils.html import format_html, mark_safe

from apps.notifications.models import (
    Notification,
    NotificationReceiver,
    NotificationLog,
)
from apps.notifications.tasks import send_notification_to_user


class NotificationReceiversInline(admin.TabularInline):
    model = NotificationReceiver
    extra = 0
    readonly_fields = ["sent_at", "status", "channel"]


class NotificationLogInline(admin.TabularInline):
    model = NotificationLog
    extra = 0
    # can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "message",
        "created_at",
        "total_users",
        "last_sent",
    ]
    actions = ["send_notifications"]
    inlines = [NotificationReceiversInline, NotificationLogInline]

    @admin.display(description="Число получателей")
    def total_users(self, obj: Notification):
        return obj.users.count()

    @admin.display(description="Последняя рассылка")
    def last_sent(self, obj: Notification):
        last_log = obj.last_log
        if not last_log:
            return None

        if last_log.in_progress:
            color, status_text = "orange", "Выполняется"
            extra_lines = (
                f"Отправлено: {last_log.total_sent}/{last_log.total_users}<br>"
                f"Ошибок: {last_log.total_failed}/{last_log.total_users}"
            )
        else:
            extra_lines = (
                f'Время: {last_log.finished_at.strftime("%Y-%m-%d %H:%M:%S")}<br>'
                f"Отправлено: {last_log.total_sent}/{last_log.total_users}<br>"
                f"Ошибок: {last_log.total_failed}/{last_log.total_users}<br>"
                f"Длительность: {last_log.duration_seconds}s"
            )
            if last_log.total_failed == 0:
                color, status_text = "green", "Выполнено успешно"
            else:
                color, status_text = "red", "Выполнено с ошибками"

        return format_html(
            '<span style="color:{};">{}</span><br>{}',
            color,
            status_text,
            mark_safe(extra_lines),
        )

    @admin.action(description="Отправить уведомления пользователям")
    def send_notifications(self, request, queryset: list[Notification]):
        for notification in queryset:
            last_log = notification.last_log
            if last_log and last_log.in_progress:
                self.message_user(
                    request,
                    f"Уведомление {notification.id} ещё в процессе рассылки, дождитесь завершения.",
                    level="error",
                )
                continue
            user_ids = list(notification.users.values_list("id", flat=True))
            NotificationLog.objects.create(
                notification=notification,
                total_users=len(user_ids),
            )

            # Формируем и запускаем группу задач
            tasks = [
                send_notification_to_user.s(notification.id, user_id)
                for user_id in user_ids
            ]
            group(tasks).apply_async()
