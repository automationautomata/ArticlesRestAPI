# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение в контейнер
COPY /app .
COPY .env .env

# Открываем порт 8000
EXPOSE 8000

# Указываем команду для запуска приложения
ENTRYPOINT ["python3", "main.py"]

