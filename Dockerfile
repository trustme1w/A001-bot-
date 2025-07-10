# Используем стабильный образ Python
FROM python:3.10-slim

# Устанавливаем системные зависимости, нужные aiohttp и другим библиотекам
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем всё приложение
COPY . .

# Запускаем бота
CMD ["python", "bot.py"]
