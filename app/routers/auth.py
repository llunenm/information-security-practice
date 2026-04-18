from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.security import hash_password, verify_password

# Роутер — це група ендпоінтів з однаковим префіксом
# Всі маршрути тут будуть починатись з /auth
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Реєстрація нового користувача"
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Створює нового користувача з хешованим паролем.
    
    1. Перевіряємо що username ще не зайнятий
    2. Перевіряємо що email ще не зайнятий
    3. Хешуємо пароль через Bcrypt
    4. Зберігаємо в БД
    5. Повертаємо дані користувача (без пароля!)
    """
    # Перевірка унікальності username
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Користувач '{user_data.username}' вже існує"
        )

    # Перевірка унікальності email
    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user_data.email}' вже зареєстровано"
        )

    # Створюємо користувача — пароль хешується тут!
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password),  # ← Bcrypt хеш
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Вхід користувача"
)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Аутентифікація за логіном та паролем.
    
    1. Знаходимо користувача за username
    2. Перевіряємо пароль через bcrypt.verify
    3. Повертаємо інформацію про користувача та ролі
    """
    # Шукаємо користувача в БД
    user = db.query(User).filter(
        User.username == credentials.username
    ).first()

    # ВАЖЛИВО: однакове повідомлення для двох випадків!
    # Якщо написати різні — хакер дізнається які логіни існують (enumeration attack)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний логін або пароль"
        )

    # Перевіряємо чи акаунт активний
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Акаунт деактивовано"
        )

    # Збираємо список ролей користувача
    user_roles = [role.name for role in user.roles]

    return LoginResponse(
        message="Вхід успішний",
        user_id=user.id,
        username=user.username,
        roles=user_roles
    )