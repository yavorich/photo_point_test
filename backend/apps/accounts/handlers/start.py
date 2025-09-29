from telegram import Update
from telegram.ext import ContextTypes
from apps.accounts.models import User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Неверная ссылка.")
        return

    token = context.args[0]

    # Ищем пользователя по telegram_token
    user = await User.objects.filter(telegram_token=token).afirst()
    if not user:
        await update.message.reply_text("Пользователь не найден.")
        return

    # Привязываем telegram_id и username
    telegram_user = update.effective_user
    user.telegram_id = telegram_user.id
    user.telegram_username = telegram_user.username
    await user.asave()

    await update.message.reply_text(f"Аккаунт успешно привязан к Telegram.")
