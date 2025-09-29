from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms
from django.utils.html import format_html
from config.settings import TELEGRAM_BOT_NAME

from apps.accounts.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label="Пароль", required=False
    )

    class Meta:
        model = User
        fields = ["email", "phone", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ["id", "email", "phone", "telegram_link", "is_telegram_linked"]

    @admin.display(description="Ссылка для привязки Telegram")
    def telegram_link(self, obj: User):
        if obj.telegram_id is None:
            return format_html(
                '<a href="https://t.me/{bot_name}?start={token}" target="_blank">Привязать Telegram</a>',
                bot_name=TELEGRAM_BOT_NAME,
                token=obj.telegram_token,
            )
        return None

    @admin.display(description="Telegram привязан", boolean=True)
    def is_telegram_linked(self, obj: User):
        return obj.telegram_id is not None


admin.site.unregister(Group)
