import hashlib
import secrets


class TokenHelper:
    def generate_session_token(self) -> tuple[str, str]:
        """Создает сессионный токен и возвращает пару (сырой, хэш)."""
        token = secrets.token_urlsafe(32)
        return token, self.hash_session_token(token)

    def hash_session_token(self, token: str) -> str:
        """Хэширует сессионный токен через SHA-256."""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()


tokens = TokenHelper()
