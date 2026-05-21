class AppError(Exception):
    """Basic application error."""


class RefreshTokenNotFoundError(AppError):
    """Рефреш токен не найден или отозван."""


class RefreshTokenExpiredError(AppError):
    """Рефреш токен истёк."""
