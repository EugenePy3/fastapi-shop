class AppError(Exception):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class UnauthorizedError(AppError):
    status_code = 401


class ForbiddenError(AppError):
    status_code = 403


# --- 400 Bad Request ---
class EmptyCartError(AppError):
    """Cart is empty."""


class RepositoryNotInitializedError(AppError):
    """Repository is not initialized in DBManager."""


# --- 401 Unauthorized ---
class InvalidCredentialsError(UnauthorizedError):
    """Invalid username or password. Неверная пара логин/пароль."""


class SessionExpiredError(UnauthorizedError):
    """Session has expired."""


class MissingSessionCookieError(UnauthorizedError):
    """Session cookie not found."""


# --- 403 Forbidden ---
class PermissionDeniedError(ForbiddenError):
    """Permission denied."""


# --- 404 Not Found ---
class ProductNotFoundError(NotFoundError):
    """Product not found."""


class CategoryNotFoundError(NotFoundError):
    """Category not found."""


class OrderNotFoundError(NotFoundError):
    """Order not found."""


class CartNotFoundError(NotFoundError):
    """Cart not found."""


class CartItemNotFoundError(NotFoundError):
    """Cart Item not found."""


class UserNotFoundError(NotFoundError):
    """User not found."""


class SessionNotFoundError(NotFoundError):
    """Session not found."""


# --- 409 Conflict ---
class UserAlreadyExistsError(ConflictError):
    """User already exists."""


class CategoryAlreadyExistsError(ConflictError):
    """Category already exists."""


class CategoryDeleteError(ConflictError):
    """Category cannot be deleted."""
