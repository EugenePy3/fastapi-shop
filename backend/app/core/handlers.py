from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from app.core.exceptions import AppError


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> Response:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": str(exc)
        },
    )
