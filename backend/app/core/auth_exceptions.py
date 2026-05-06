class AppError(Exception):
    """Базовая ошибка приложения."""


class RefreshTokenNotFoundError(AppError):
    """Рефреш токен не найден или отозван."""


class RefreshTokenExpiredError(AppError):
    """Рефреш токен истёк."""
