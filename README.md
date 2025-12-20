Тести

У tests/test_smoke.py є перевірки:

GET /healthcheck повертає 200 та JSON з "status": "ok".

GET /record без query-параметрів повинен повертати 400.

Фрагмент логіки тестів:

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


Запуск тестів:

pytest -q

ЛР1. Запуск локально (без Docker)
1) Віртуальне середовище (Windows, cmd)
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

ЛР2. REST API “Облік витрат” (in-memory)
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

Створити користувача:

curl -X POST http://127.0.0.1:8080/user -H "Content-Type: application/json" -d "{\"name\":\"Misha\"}"


Створити категорію:

curl -X POST http://127.0.0.1:8080/category -H "Content-Type: application/json" -d "{\"name\":\"Food\"}"


Створити запис витрати:

curl -X POST http://127.0.0.1:8080/record -H "Content-Type: application/json" -d "{\"user_id\":1,\"category_id\":1,\"sum\":99.9}"


Отримати записи користувача:

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

ЛР3. Валідація, обробка помилок, ORM + база даних
Мета / що зроблено

Додано валідацію вхідних даних (body/query params) через схеми.

Додано уніфіковану обробку помилок (повертаємо JSON, а не HTML).

Додано ORM і збереження в БД (дані зберігаються між перезапусками).

Додано новий функціонал згідно варіанту (описати тут, що саме у твоєму варіанті).

Примітка: ЛР2 була in-memory, а в ЛР3 використовується БД через ORM.

Змінні середовища (ENV)

Потрібно задати змінну БД:

DATABASE_URL — рядок підключення до БД
Приклади:

SQLite (локально): sqlite:///app.db

Render/Postgres: Render дає готовий DATABASE_URL

(Опціонально, якщо використовується в проєкті)

SECRET_KEY — секретний ключ для Flask

PORT — порт (на Render автоматично)

Міграції БД (якщо у проєкті є Alembic/Flask-Migrate)

Якщо міграції використовуються — виконати:

flask --app "app:create_app" db upgrade


Якщо міграцій ще нема, базова ініціалізація:

flask --app "app:create_app" db init
flask --app "app:create_app" db migrate -m "init db"
flask --app "app:create_app" db upgrade

Запуск локально (ЛР3)

Windows (cmd) приклад з SQLite:

env\Scripts\activate
pip install -r requirements.txt

set DATABASE_URL=sqlite:///app.db
flask --app "app:create_app" run --host 0.0.0.0 -p 8080

Docker запуск (ЛР3)
docker build -t backend-project:latest .
docker run -it --rm -e PORT=8080 -e DATABASE_URL=sqlite:///app.db -p 8080:8080 backend-project:latest

Валідація та помилки (приклади)
400/422 — помилка валідації

POST /user

{}


Очікувано: помилка у форматі JSON (приклад):

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": { "name": ["required"] }
  }
}

404 — сутність не знайдена

GET /user/9999

409 — конфлікт (якщо є унікальні обмеження)

Наприклад, повторне створення категорії з тим самим name (якщо це налаштовано).

Деплой (Render) для ЛР3

Repo на GitHub підключений до Render (Docker Web Service)

Render сам передає $PORT

Для БД потрібно додати DATABASE_URL в Render → Environment

Після деплою перевірити:

GET /healthcheck працює

основні endpoint-и працюють і повертають JSON

дані зберігаються (не зникають після перезапуску сервісу)
