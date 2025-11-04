# Базовый образ
FROM python:3.11-slim

# Установка системных зависимостей для WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libcairo2 libgdk-pixbuf-xlib-2.0-0 shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements и устанавливаем Python‑пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend в /app
COPY . .

# Открываем порт 8003
EXPOSE 8003

# Запуск приложения
CMD ["python", "app.py"]