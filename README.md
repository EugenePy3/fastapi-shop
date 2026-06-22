
# FastAPI Shop

Полнофункциональный backend для интернет-магазина на **FastAPI**, **PostgreSQL** и **Docker**.  
Проект демонстрирует подход к построению backend-приложений с использованием многослойной архитектуры, паттернов Repository, Service и Unit of Work, доменных исключений, eager loading и сессионной аутентификации.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

## 🚀 Ключевые особенности

- **Многослойная архитектура** (Routes → Services → Repositories → Models)
- **Собственное дерево доменных ошибок** с маппингом на HTTP-статусы и глобальным обработчиком
- **Асинхронная работа с БД** через SQLAlchemy 2.0 (async) и PostgreSQL
- **Строгая типизация** и валидация через Pydantic V2
- **Сессионная аутентификация** с разделением прав (admin / user)
- **Защита от N+1** с помощью `selectinload` / `joinedload` на уровне репозиториев
- **Пагинация** и корректный подсчёт общего количества записей (`skip/limit`)
- **Контейнеризация** (Docker Compose) и лёгкий запуск одной командой

## 📁 Структура проекта


```text
app/
├── core/            # Конфигурация, безопасность, обработчики ошибок, токены, DBManager
├── database.py      # Настройка SQLAlchemy, подключение к PostgreSQL
├── dependencies.py  # FastAPI зависимости и авторизация

├── enums/           # Перечисления домена (статусы заказов и др.)

├── models/          # ORM-модели SQLAlchemy
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   ├── cart.py
│   └── order.py

├── repositories/    # Работа с базой данных (CRUD и SQL-запросы)
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── category_repository.py
│   ├── cart_repository.py
│   ├── order_repository.py
│   └── session_repository.py

├── services/        # Бизнес-логика приложения
│   ├── auth_service.py
│   ├── user_service.py
│   ├── product_service.py
│   ├── category_service.py
│   ├── cart_service.py
│   ├── order_service.py
│   └── session_service.py

├── schemas/         # DTO-схемы Pydantic для запросов и ответов API
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   ├── cart.py
│   └── order.py

├── routes/          # HTTP endpoints FastAPI
│   ├── users.py
│   ├── products.py
│   ├── categories.py
│   ├── cart.py
│   ├── order.py
│   └── session.py

└── utils/           # Вспомогательные функции и утилиты
    ├── cookies.py
    └── session_utils.py
```

### Архитектурный поток

```text
Request
   ↓
Routes
   ↓
Services
   ↓
Repositories
   ↓
PostgreSQL
```


## 📚 Ответственность слоёв

| Слой            | Назначение                                                      |
|-----------------|-----------------------------------------------------------------|
| **Routes**      | Принимают HTTP-запросы и возвращают ответы                     |
| **Schemas**     | Валидируют входящие и исходящие данные (Pydantic)              |
| **Services**    | Содержат бизнес-логику приложения                              |
| **Repositories**| Изолируют работу с базой данных (только запросы)               |
| **Models**      | ORM-модели SQLAlchemy                                          |
| **Core**        | Инфраструктурный код: конфигурация, безопасность, обработка ошибок |
| **Utils**       | Вспомогательные функции без бизнес-логики                      |

Проект построен по принципам **Layered Architecture** с чётким разделением ответственности между слоями. Это упрощает поддержку, тестирование и дальнейшее развитие приложения.


## 🔧 Технологии

| Технология        | Назначение                             |
|-------------------|----------------------------------------|
| **FastAPI**       | Веб-фреймворк, асинхронный API        |
| **PostgreSQL 16** | База данных                            |
| **SQLAlchemy 2.0**| Асинхронный ORM, строгий стиль        |
| **Pydantic V2**   | Валидация данных, схемы ответов/запросов |
| **Alembic**       | Миграции (в плане)                     |
| **Docker**        | Контейнеризация приложения и БД        |
| **Redis**         | Кэширование (в плане)                  |

## 🛠️ Запуск

### Требования
- Docker и Docker Compose (актуальные версии)
- (опционально) Python 3.12 для локальной разработки

### Быстрый старт (Docker)
1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/your-username/fastapi-shop.git
   cd fastapi-shop
   
2. Запустите контейнеры:

    ```bash
    docker-compose up -d

   Приложение будет доступно по адресу: http://localhost:8000

   Swagger-документация: http://localhost:8000/api/docs
   
📡 API (основные эндпоинты)

| Метод  | Эндпоинт                              | Описание                          | Доступ |
|--------|---------------------------------------|-----------------------------------|--------|
| POST   | `/auth/register`                      | Регистрация пользователя          | All    |
| POST   | `/auth/login`                         | Вход в систему (создание сессии)  | All    |
| POST   | `/auth/logout`                        | Выход из системы (удаление сессии)| User   |
| GET    | `/auth/me`                            | Получить текущего пользователя    | User   |
| GET    | `/api/products`                       | Список товаров (с пагинацией)     | All    |
| POST   | `/api/products`                       | Создать товар                     | Admin  |
| GET    | `/api/products/{product_id}`          | Получить товар по ID              | All    |
| PATCH  | `/api/products/{product_id}`          | Обновить товар                    | Admin  |
| DELETE | `/api/products/{product_id}`          | Удалить товар                     | Admin  |
| GET    | `/api/products/category/{category_id}`| Товары по категории               | All    |
| GET    | `/api/categories`                     | Список категорий                  | All    |
| POST   | `/api/categories`                     | Создать категорию                 | Admin  |
| GET    | `/api/categories/{category_id}`       | Получить категорию по ID          | All    |
| PATCH  | `/api/categories/{category_id}`       | Обновить категорию                | Admin  |
| DELETE | `/api/categories/{category_id}`       | Удалить категорию                 | Admin  |
| GET    | `/api/cart`                           | Получить корзину текущего юзера   | User   |
| DELETE | `/api/cart`                           | Очистить корзину                  | User   |
| POST   | `/api/cart/items`                     | Добавить товар в корзину          | User   |
| PATCH  | `/api/cart/items/{product_id}`        | Изменить количество товара        | User   |
| DELETE | `/api/cart/items/{product_id}`        | Удалить товар из корзины          | User   |
| POST   | `/api/order`                          | Создать заказ из корзины          | User   |
| GET    | `/api/order`                          | Список заказов пользователя       | User   |
| GET    | `/api/order/{order_id}/status`        | Получить заказ по ID              | User   |
| PATCH  | `/api/order/{order_id}/status`        | Изменить статус заказа            | Admin  |  

## 🏗️ Архитектурные решения

* **Repository Pattern** — каждый репозиторий отвечает за работу с конкретной сущностью и инкапсулирует SQLAlchemy-запросы. Бизнес-логика в репозиториях отсутствует.

* **Service Layer** — содержит бизнес-правила приложения, координирует работу репозиториев, выполняет проверки и управляет доменными сценариями.

* **Unit of Work (DBManager)** — единая точка доступа к репозиториям и транзакциям. Управляет жизненным циклом сессии SQLAlchemy и обеспечивает атомарность операций.

* **Domain Exceptions** — собственная иерархия исключений (`AppError`, `NotFoundError`, `ConflictError` и др.) с централизованной обработкой через глобальные exception handlers. Это позволяет отделить бизнес-логику от HTTP-слоя.

* **Eager Loading** — для предотвращения проблемы N+1 запросов используются `selectinload()` и `joinedload()` в репозиториях.

* **Session-Based Authentication** — аутентификация реализована через серверные сессии с хранением хеша токена в базе данных.

* **Decimal для денежных значений** — цены товаров хранятся в `Decimal`, что исключает ошибки округления, характерные для `float`.

---

## 🧪 Тестирование

В проекте присутствует файл `test_commands.md` с набором curl-команд для проверки основных пользовательских сценариев:

* регистрация и авторизация;
* работа с категориями;
* работа с товарами;
* управление корзиной;
* оформление заказа;
* завершение сессии.

---

## 🚧 Планы по развитию

* [x] CRUD для товаров и категорий
* [x] Корзина покупателя
* [x] Оформление заказов
* [x] Сессионная аутентификация
* [ ] Миграции через Alembic
* [ ] Redis для кэширования
* [ ] Unit-тесты (pytest + httpx)
* [ ] Фоновые задачи
* [ ] Административная панель
* [ ] Docker-ready production deployment

---

## 👤 Автор

**Евгений Гребенюк**

Telegram: 
```bash
@Maine_Coon_1



