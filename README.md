# backend-project

Бекенд-проєкт для лабораторних робіт:

- **ЛР1** — запуск локально, Docker, деплой (Render), tooling (black/ruff/pytest/pre-commit)
- **ЛР2** — базове REST API для обліку витрат (in-memory)

---

## Структура проєкту
backend-project/
app/
init.py
views.py
models.py
schemas.py
user_routes.py
category_routes.py
record_routes.py
tests/
test_smoke.py
Dockerfile
docker-compose.yml
requirements.txt
.pre-commit-config.yaml
.gitignore
.dockerignore

---

## Тести

У `tests/test_smoke.py` є перевірки:

- `GET /healthcheck` повертає `200` та JSON з `"status": "ok"`.
- `GET /record` без query-параметрів **повинен** повертати `400`.

Фрагмент логіки тестів:
py
from app import create_app

def test_healthcheck():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthcheck")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"

def test_record_requires_filters():
    app = create_app()
    client = app.test_client()
    resp = client.get("/record")
    assert resp.status_code == 400
ЛР1. Запуск локально (без Docker)
1) Віртуальне середовище
   python -m venv env
env\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
2) Запуск Flask
У проєкті використовується фабрика create_app.
flask --app "app:create_app" run --host 0.0.0.0 -p 8080
Відкрити:
http://127.0.0.1:8080/
http://127.0.0.1:8080/healthcheck
ЛР1. Tooling (black / ruff / pytest / pre-commit)
Встановлення та підключення хуків
pip install black ruff pytest pre-commit
pre-commit install
pre-commit install --hook-type pre-push
Запуск перевірок вручну
pre-commit run --all-files

Запуск тестів
pytest -q

ЛР1. Docker
1) Білд образу
docker build -t backend-project:latest .

2) Запуск контейнера
docker run -it --rm -e PORT=8080 -p 8080:8080 backend-project:latest


Відкрити:

http://127.0.0.1:8080/

http://127.0.0.1:8080/healthcheck

3) Docker Compose
docker compose up --build

ЛР1. Деплой (Render / Docker-based Web Service)

Загальна логіка:

Репозиторій на GitHub

Render → New Web Service → підключити GitHub repo

Тип деплою: Docker

Порт: Render дає свій $PORT, сервіс має слухати його

Команда запуску всередині контейнера (приклад):

flask --app "app:create_app" run -h 0.0.0.0 -p $PORT


Після деплою перевірити:

GET /healthcheck → {"status":"ok", ...}

ЛР2. REST API “Облік витрат”
Базові правила

Дані in-memory (в пам’яті процеса). Після перезапуску деплою/контейнера дані скидаються.

Повертаємо JSON.

Основні сутності:

User: {id, name}

Category: {id, name}

Record: {id, user_id, category_id, created_at, sum}

Endpoints
Health / Core

GET / — тестовий ендпоінт

GET /healthcheck — перевірка, що сервіс живий

Users

GET /users — список користувачів

POST /user — створити користувача
Body:

{ "name": "Misha" }


GET /user/<user_id> — отримати користувача

DELETE /user/<user_id> — видалити користувача

Categories

GET /category — список категорій

POST /category — створити категорію
Body:

{ "name": "Food" }


DELETE /category?category_id=1 — видалити категорію (через query param)

Records

POST /record — створити запис витрат
Body (підтримується sum або amount):

{ "user_id": 1, "category_id": 2, "sum": 120.5 }


GET /record/<record_id> — отримати запис

DELETE /record/<record_id> — видалити запис

GET /record?user_id=1 — записи користувача

GET /record?category_id=2 — записи категорії

GET /record?user_id=1&category_id=2 — записи за двома фільтрами

Важливо: GET /record без параметрів повертає 400 (це перевіряється тестом).

Приклади запитів (curl)
Створити користувача
curl -X POST http://127.0.0.1:8080/user -H "Content-Type: application/json" -d "{\"name\":\"Misha\"}"

Створити категорію
curl -X POST http://127.0.0.1:8080/category -H "Content-Type: application/json" -d "{\"name\":\"Food\"}"

Створити запис витрати
curl -X POST http://127.0.0.1:8080/record -H "Content-Type: application/json" -d "{\"user_id\":1,\"category_id\":1,\"sum\":99.9}"

Отримати записи користувача
curl "http://127.0.0.1:8080/record?user_id=1"

Postman (для здачі ЛР2)

Рекомендовано зробити:

Environment зі змінною base_url

local: http://127.0.0.1:8080

render: https://<your-service>.onrender.com

Collection з усіма запитами з розділу “Endpoints”

Експортувати:

collection.json

environment.json

Що здати

Посилання на GitHub репозиторій

Посилання на деплой (Render)

Postman collection + environment (.json)

Перевірка, що:

/healthcheck працює

/record без параметрів повертає 400

---
Якщо хочеш — скинь мені **твій поточний README з GitHub** (прямо текстом або файлом), і я зроблю **мінімальний диф**: що саме додати/прибрати, щоб було “як треба для здачі” і без зайвого.
::contentReference[oaicite:0]{index=0}
