from telegram.ext import CommandHandler

from apps.accounts.handlers import start, unlink


handlers = [
    CommandHandler("start", start),
    CommandHandler("unlink", unlink),
]
