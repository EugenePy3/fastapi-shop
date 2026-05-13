class AppError(Exception):
    """Базовая ошибка приложения."""


class RepositoryNotInitializedError(AppError):
    """Репозиторий не инициализирован в DBManager."""


class InvalidCredentialsError(AppError):
    """Invalid username or password.
    Неверная пара логин/пароль."""


class UserAlreadyExistsError(AppError):
    """User alredy exists."""


class UserNotFoundError(AppError):
    """Пользователь не найден."""


# SHOP
class CategoryNotFoundError(AppError):
    """Category not found."""


class CategoryAlreadyExistsError(AppError):
    """Category already exists."""


class CategoryDeleteError(AppError):
    """Category cannot be deleted."""


class ProductNotFoundError(AppError):
    """Product not found."""


class CartItemNotFoundError(AppError):
    """Cart Item not found."""
