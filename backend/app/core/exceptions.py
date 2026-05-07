class AppError(Exception):
    """Базовая ошибка приложения."""


class RepositoryNotInitializedError(AppError):
    """Репозиторий не инициализирован в DBManager."""


class InvalidCredentialsError(AppError):
    """Неверная пара логин/пароль."""


class UserAlreadyExistsError(AppError):
    """Пользователь уже существует."""


class UserNotFoundError(AppError):
    """Пользователь не найден."""


# SHOP
class CategoryNotFoundError(AppError):
    """Category not found"""


class CategoryAlreadyExistsError(AppError):
    """Category already exists"""


class CategoryDeleteError(AppError):
    """Category cannot be deleted"""
