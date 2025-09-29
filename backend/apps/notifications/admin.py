from celery import group
from django.contrib import admin

from apps.notifications.models import Notification, NotificationReceiver, NotificationStatus
from apps.notifications.tasks import send_notification_to_user


class NotificationReceiversInline(admin.TabularInline):
    model = NotificationReceiver
    extra = 0
    readonly_fields = ["sent_at", "status", "channel"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "message", "created_at", "sent_count", "failed_count"]
    actions = ["send_notifications"]
    inlines = [NotificationReceiversInline]

    @admin.display(description="Отправлено")
    def sent_count(self, obj):
        return obj.receivers.filter(status=NotificationStatus.SENT).count()

    @admin.display(description="Ошибка")
    def failed_count(self, obj):
        return obj.receivers.filter(status=NotificationStatus.FAILED).count()

    @admin.action(description="Отправить уведомления пользователям")
    def send_notifications(self, request, queryset):
        all_tasks = []
        for notification in queryset:
            user_ids = notification.users.values_list("id", flat=True)
            all_tasks.extend(
                send_notification_to_user.s(notification.id, user_id) for user_id in user_ids
            )
        group(all_tasks).apply_async()
