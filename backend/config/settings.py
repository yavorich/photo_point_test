from os import environ
import os
from pathlib import Path
from telegram import Bot

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get("DEBUG", "0").lower() in ("true", "1")

ALLOWED_HOSTS = environ["ALLOWED_HOSTS"].split(",")

# https
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

LOCAL_APPS = [
    "apps.accounts",
    "apps.notifications",
]

THIRD_PARTY_APPS = [
    "phonenumber_field",
    "smsru",
]

INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

AUTH_USER_MODEL = "accounts.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

# Database config
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["POSTGRES_DB"],
        "USER": environ["POSTGRES_USER"],
        "PASSWORD": environ["POSTGRES_PASSWORD"],
        "HOST": environ["POSTGRES_HOST"],
        "PORT": environ["POSTGRES_PORT"],
        "ATOMIC_REQUESTS": True,
    }
}

# RabbitMQ config
RABBITMQ = {
    "PROTOCOL": "amqp",
    "HOST": environ["RABBITMQ_HOST"],
    "PORT": environ["RABBITMQ_PORT"],
    "USER": environ["RABBITMQ_USER"],
    "PASSWORD": environ["RABBITMQ_PASSWORD"],
}

# Celery config
CELERY_BROKER_URL = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}"
    f":{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_ENABLE_UTC = False
CELERY_MAX_TASKS_PER_CHILD = 1
CELERY_RESULT_BACKEND = "rpc://"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

DJANGO_CELERY_BEAT_TZ_AWARE = True

# SMTP config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True
FROM_EMAIL = os.environ.get("FROM_EMAIL", "noreply@test.com")

# SMS_RU config
SMS_RU_API_ID = os.environ.get("SMS_RU_API_ID")
SMS_RU_TEST = os.environ.get("SMS_RU_TEST", "0").lower() in ("true", "1")
SMS_RU = {
    "API_ID": SMS_RU_API_ID,
    "TEST": SMS_RU_TEST,
    "SENDER": None,
}

# Telegram Bot config
TELEGRAM_BOT_NAME = os.environ.get("TELEGRAM_BOT_NAME")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)

MAIN_BOT = Bot(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else None

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
os.makedirs("logs", exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/django.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
            "formatter": "verbose",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
