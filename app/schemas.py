from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re


# ══════════════════════════════════════════
# СХЕМИ ДЛЯ РЕЄСТРАЦІЇ
# ══════════════════════════════════════════

class UserCreate(BaseModel):
    """Що користувач надсилає при реєстрації."""
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Логін (латиниця, цифри, підкреслення)"
    )
    email: EmailStr = Field(
        ...,
        description="Email-адреса"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Пароль (мінімум 8 символів)"
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Повне ім'я"
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """Перевірка складності пароля."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль має містити хоча б одну велику літеру")
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль має містити хоча б одну малу літеру")
        if not re.search(r"[0-9]", v):
            raise ValueError("Пароль має містити хоча б одну цифру")
        return v


class UserResponse(BaseModel):
    """Що сервер повертає про користувача (БЕЗ пароля!)."""
    
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ══════════════════════════════════════════
# СХЕМИ ДЛЯ ВХОДУ
# ══════════════════════════════════════════

class LoginRequest(BaseModel):
    """Що користувач надсилає при вході."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Що сервер повертає при успішному вході."""
    message: str
    user_id: int
    username: str
    roles: list[str] = []

# ══════════════════════════════════════════
# СХЕМИ ДЛЯ JWT (нові — практична №5)
# ══════════════════════════════════════════

class TokenResponse(BaseModel):
    """Відповідь при успішному вході — містить обидва токени."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    """Запит на оновлення токена."""
    refresh_token: str


class UserInfo(BaseModel):
    """Інформація про поточного користувача."""
    id: int
    username: str
    email: str
    full_name: str
    role: str

    model_config = {"from_attributes": True}