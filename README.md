 # Photo Point Test Project

## Основные возможности

- **Пользовательская модель `User`** с полями:
  - Email
  - Телефон
  - Telegram ID и username
  - Telegram токен для привязки

- **Модели уведомлений:**
  - `Notification` — основная модель рассылки
  - `NotificationReceiver` — связанная модель получателей
  - `NotificationLog` — связанная модель истории рассылок

- **Сервис уведомлений (`NotificationService`)**:
  - Отправка сообщений через Telegram, SMS и Email
  - Приоритетная доставка: Telegram → SMS → Email
  - Логирование ошибок и статусов доставки

- **Асинхронная обработка уведомлений** с помощью Celery

- **Django Admin:**
  - Управление пользователями и их Telegram привязкой
  - Создание и запуск асинхронной рассылки уведомлений

- **Тесты** с использованием `pytest`

## Технологии

- Python 3.12
- Django 5.x
- PostgreSQL
- Celery
- RabbitMQ
- Docker & Docker Compose
- python-telegram-bot
- SMS.RU API

## Установка

```bash
git clone https://github.com/yavorich/photo_point_test.git
cd photo_point_test
```

## Запуск

```bash
make build
make up
```

или через Docker Compose напрямую:

```bash
docker-compose up -d --build
```

## Миграции, создание суперпользователя, статика

```bash
make migrate
make createsuperuser
make collectstatic
```

или через контейнер:

```bash
docker exec -it ppt_backend python manage.py migrate
docker exec -it ppt_backend python manage.py createsuperuser
docker exec -it ppt_backend python manage.py collectstatic --noinput
```

## Создание пользователя

В разделе **Пользователи** админ-панели:
1. Нажать "Добавить пользователь"
2. Заполнить форму (пароль можно не указывать)
3. Нажать "Сохранить"

## Привязка Telegram

Перейти по ссылке **"Привязать Telegram"** для необходимого пользователя в списке.

## Создание уведомления

В разделе **Уведомления** админ-панели:
1. Нажать "Добавить уведомление"
2. Указать текст и получателей
3. Нажать "Сохранить"

## Отправка уведомлений

1. В списке уведомлений выбрать необходимые
2. В меню действий выбрать **"Отправить уведомления пользователям"**
3. Нажать "Выполнить"

Для отправленных уведомлений отображается:
- Число успешных отправок и ошибок
- Время выполнения и завершения
- Статус и способ отправки для каждого получателя