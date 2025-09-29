import logging

from telegram.ext import ApplicationBuilder
from telegram import Update

from config.settings import TELEGRAM_BOT_TOKEN
from telegram_bot.main.endpoints import handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handlers(handlers)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
