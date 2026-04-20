# Wallet Service

REST API сервис для управления кошельками. Позволяет создавать кошельки, пополнять и снимать средства, а также проверять баланс.

## Технологии

FastAPI, PostgreSQL (asyncpg), SQLAlchemy 2.0 (async), Alembic, Docker / Docker Compose, Pytest

## Установка и запуск

### Через Docker (рекомендуется)

```bash
docker-compose up -d
```

Сервис будет доступен по адресу: <http://localhost:8000>

### Локальный запуск

Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Настройте базу данных PostgreSQL и создайте файл .env:
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/wallets_db

Накатите миграции:

```bash
alembic upgrade head
```

Запустите приложение:

```bash
uvicorn app.main:app --reload
```

## API Эндпоинты

- POST /api/v1/wallets/ - Создать новый кошелёк
- GET /api/v1/wallets/{wallet_uuid} - Получить баланс кошелька
- POST /api/v1/wallets/{wallet_uuid}/operation - Пополнение или списание

### Примеры запросов

Создание кошелька:

```bash
curl -X POST <http://localhost:8000/api/v1/wallets/>
```

Ответ:
{"id": "550e8400-e29b-41d4-a716-446655440000", "balance": 0}

Пополнение баланса:

```bash
curl -X POST <http://localhost:8000/api/v1/wallets/550e8400-e29b-41d4-a716-446655440000/operation> -H "Content-Type: application/json" -d '{"operation_type": "DEPOSIT", "amount": 1000}'
```

Снятие средств:

```bash
curl -X POST <http://localhost:8000/api/v1/wallets/550e8400-e29b-41d4-a716-446655440000/operation> -H "Content-Type: application/json" -d '{"operation_type": "WITHDRAW", "amount": 500}'
```

Получение баланса:

```bash
curl <http://localhost:8000/api/v1/wallets/550e8400-e29b-41d4-a716-446655440000>
```

## Тестирование

```bash
pytest tests/ -v
```

## Документация API

Swagger UI: <http://localhost:8000/docs>
ReDoc: <http://localhost:8000/redoc>

## Особенности

- Асинхронная работа с базой данных
- Блокировка строк (SELECT FOR UPDATE) для конкурентных операций
- Автоматическая генерация UUID для кошельков
- Валидация входных данных через Pydantic
- История всех операций в таблице payments
