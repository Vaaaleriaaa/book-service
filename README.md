# Book Service - REST API на Python + FastAPI

Микросервис для управления книгами с использованием FastAPI и PostgreSQL.

## Как запустить

1. Склонируйте репозиторий.
2. Убедитесь, что Docker Desktop запущен.
3. Соберите и запустите контейнеры:

```bash
docker compose up --build -d
```

(Чтобы остановить сервисы, используйте команду `docker compose down`)

**Ссылки:**
API: http://localhost:8000
Swagger UI: http://localhost:8000/docs
Корневой endpoint (Health check): http://localhost:8000/

## REST API

1. Создать книгу

```bash
curl -i -X POST http://localhost:8000/api/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Война и мир","author":"Лев Толстой","year":1869,"description":"Роман-эпопея"}'
```

2. Получить список всех книг

```bash
curl -i http://localhost:8000/api/books
```

Поиск по автору:

```bash
curl -i 'http://localhost:8000/api/books/search/author/Лев%20Толстой'
```

3. Получить одну книгу

```bash
curl -i http://localhost:8000/api/books/1
```

4. Полностью обновить книгу (PUT)

```bash
curl -i -X PUT http://localhost:8000/api/books/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Война и мир (новое изд.)","author":"Лев Толстой","year":1870,"description":"Обновленное описание"}'
```

5. Частично обновить книгу (PATCH)

```bash
curl -i -X PATCH http://localhost:8000/api/books/1 \
  -H 'Content-Type: application/json' \
  -d '{"year":1871}'
```

6. Удалить книгу

```bash
curl -i -X DELETE http://localhost:8000/api/books/1
```

При некорректных данных микросервис возвращает JSON и соответствующий HTTP-код.

1. Ошибка валидации (400 Bad Request)

Попытка создать книгу с пустым названием и некорректным годом:

```bash
curl -i -X POST http://localhost:8000/api/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"","year":1000}'
```

Ответ сервера:

```json
{
  "timestamp": "2026-11-23T12:00:00.000000",
  "status": 400,
  "error": "Bad Request",
  "message": "Ошибки валидации",
  "details": {
    "title": "String should have at least 1 character",
    "author": "Field required",
    "year": "Input should be greater than or equal to 1800"
  },
  "path": "http://localhost:8000/api/books"
}
```

2. Ресурс не найден (404 Not Found)

Попытка получить несуществующую книгу по `id`:

```bash
curl -i http://localhost:8000/api/books/999
```

Ответ сервера:

```json
{
  "detail": "Книга не найдена с ID: 999"
}
```

## Тестирование через Postman

Для тестирования в корень репозитория включен файл `Book Service API.postman_collection.json`.

**Как использовать:**

1. Откройте desktop версию Postman.
2. Нажмите кнопку **Import** в левом верхнем углу.
3. Перетащите файл `Book Service API.postman_collection.json` в окно импорта или выберите его через проводник.
4. После импорта вы получите готовую коллекцию со всеми запросами и тестами.
