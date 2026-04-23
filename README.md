# bot_4_voice

Telegram-бот для изменения голоса в голосовых сообщениях через ffmpeg.

## Возможности

- Принимает голосовые сообщения и аудиофайлы (до 20 МБ)
- 12 эффектов: бурундук, бас, робот, эхо, реверс, телефон, шёпот, ускорение, замедление, пещера, радио, вибрато
- Результат — голосовое сообщение (OGG Opus)
- Кнопка «Другой эффект» для повторного применения
- Три языка: русский, узбекский, английский
- Обязательная подписка на каналы
- Админ-панель: статистика, каналы, рассылка

## Стек

- Python 3.12 + aiogram 3.26
- PostgreSQL 16 (SQLAlchemy 2.x async)
- ffmpeg
- Docker Compose

## Деплой

```bash
cp .env.example .env
# заполнить BOT_TOKEN, DB_PASSWORD, ADMIN_IDS

docker compose up -d --build
docker compose logs -f bot
```

## Структура

```
bot/
  main.py, config.py, i18n.py, emojis.py
  database/   — models, crud
  handlers/   — start, admin, voice
  middlewares/ — subscription, rate_limit
  keyboards/  — inline, admin
  services/   — voice_effects
  utils/      — commands, fsm_cleanup
```
