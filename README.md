# FastAPI Интернет-магазин

Простой интернет-магазин с API на FastAPI и фронтендом на Vue 3.

## Что умеет проект

- **Пользователи** — регистрация, вход, JWT-токены, роли (buyer/seller/admin)
- **Товары** — создание, просмотр, поиск, пагинация и фильтрация
- **Категории** — древовидная структура с подкатегориями
- **Отзывы** — оценки (1–5) и комментарии к товарам
- **Корзина** — добавление и управление товарами

## Технологии

**Backend:** FastAPI, SQLAlchemy, PostgreSQL (async), Alembic, JWT

**Frontend:** Vue 3, TypeScript, Tailwind CSS, Pinia, Vue Router, Vite

## Быстрый старт

### Backend

```bash
# Создай виртуальное окружение и установи зависимости
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Примени миграции
alembic upgrade head

# Запусти сервер
uvicorn app.main:app --reload
```

API будет доступен на `http://localhost:8000`, документация — на `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Фронтенд откроется на `http://localhost:5173`.

## Структура проекта

```
├── app/                 # Backend на FastAPI
│   ├── main.py          # Точка входа
│   ├── auth.py          # JWT-аутентификация
│   ├── config.py        # Настройки
│   ├── database.py      # Подключение к БД
│   ├── schemas.py       # Pydantic-схемы
│   ├── models/          # SQLAlchemy-модели
│   ├── routers/         # API-эндпоинты
│   └── migrations/      # Alembic-миграции
├── frontend/            # Фронтенд на Vue 3
│   └── src/
│       ├── views/       # Страницы
│       ├── components/  # Компоненты
│       ├── stores/      # Хранилища Pinia
│       ├── api/         # API-клиенты
│       └── router/      # Маршрутизация
└── ecommerce.db         # SQLite (для разработки)
```

## Переменные окружения

Создай файл `.env` в корне:

```
SECRET_KEY=твой_секретный_ключ
```
