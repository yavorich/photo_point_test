from telegram import Update
from telegram.ext import ContextTypes
from apps.accounts.models import User


async def unlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user = update.effective_user
    user = await User.objects.filter(telegram_id=telegram_user.id).afirst()

    if not user:
        await update.message.reply_text("Ваш аккаунт не привязан к Telegram.")
        return

    # Отвязываем
    user.telegram_id = None
    user.telegram_username = None
    await user.asave(update_fields=["telegram_id", "telegram_username"])

    await update.message.reply_text("Ваш Telegram-аккаунт успешно отвязан.")
