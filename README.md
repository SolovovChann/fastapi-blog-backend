# fastapi-blog-backend

Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователями.

## Установка через docker

Создание образа

```cmd
docker build -t fastapi-blog:$(date +%Y-%m-%d) -t fastapi-blog:latest .
```

Запуск контейнера

```cmd
docker run -d --port 8000:8000 --env SECRET_KEY=<Your secret key> fastapi-blog:latest
```

## Установка для разработки

Установите зависимости

```cmd
pip install -r requirements.txt
```

Запустите сервер для разработки

```cmd
fastapi run main.py
```
