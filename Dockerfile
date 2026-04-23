FROM python:3.12-slim

# ffmpeg для обработки аудио, curl для утилит
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# сначала зависимости (кэшируется Docker слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# потом код
COPY bot/ bot/

CMD ["python", "-m", "bot.main"]
