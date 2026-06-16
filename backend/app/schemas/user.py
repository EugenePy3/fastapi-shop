from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50,
        description='Username'
    )

    password: str = Field(
        min_length=6,
        max_length=128,
        description='User password'
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        description='Unique user identifier'
    )
    name: str = Field(
        description='Username'
    )
    created_at: datetime = Field(
        description='Account creation date'
    )


class LoginRequest(BaseModel):
    name: str = Field(
        description='Username'
    )

    password: str = Field(
        description='User password'
    )


class SessionLoginResponse(BaseModel):
    user: UserResponse = Field(
        description='Authenticated user'
    )


class MessageResponse(BaseModel):
    detail: str
