<div align="center">

# FastAPI Shop

Production-oriented e-commerce backend built with FastAPI, PostgreSQL and layered architecture.

Features:
- Session-based authentication
- Role-based access control
- Layered architecture
- Repository & Service patterns
- Domain exceptions & global handlers
- Dockerized environment
- PostgreSQL integration

</div>

## 📁 Структура проекта

```
fastapi-shop/
│
├── app/
│   │
│   ├── core/                     # Core infrastructure & shared logic
│   │   ├── config.py             # Application settings & environment variables
│   │   ├── db_manager.py         # Database session manager (Unit of Work style)
│   │   ├── exceptions.py         # Domain exceptions
│   │   ├── auth_exceptions.py    # Authentication-related exceptions
│   │   ├── handlers.py           # Global exception handlers
│   │   ├── security.py           # Password hashing & verification
│   │   └── tokens.py             # Session token generation & hashing
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── user.py               # User & session models
│   │   ├── category.py           # Category model
│   │   └── product.py            # Product model
│   │
│   ├── schemas/                  # Pydantic validation schemas
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── cart.py
│   │
│   ├── repositories/             # Database access layer
│   │   ├── user_repository.py
│   │   ├── category_repository.py
│   │   └── product_repository.py
│   │
│   ├── services/                 # Business logic layer
│   │   ├── auth_service.py
│   │   ├── category_service.py
│   │   ├── product_service.py
│   │   └── cart_service.py
│   │
│   ├── routes/                   # API endpoints
│   │   ├── users.py
│   │   ├── session.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── cart.py
│   │
│   ├── database.py               # SQLAlchemy engine & session setup
│   ├── dependencies.py           # FastAPI dependencies
│   └── main.py                   # FastAPI application entrypoint
│
├── static/
│   └── images/                   # Product images & static assets
│
├── docker-compose.yml            # Docker services configuration
├── requirements.txt              # Python dependencies
├── run.py                        # Local development server runner
├── seed_data.py                  # Database seeding script
├── test_commands.md              # API testing examples
└── README.md                     # Project documentation
```

