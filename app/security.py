from passlib.context import CryptContext

# Налаштовуємо контекст хешування з алгоритмом Bcrypt
# deprecated="auto" — якщо колись зміниш алгоритм, старі хеші автоматично позначаться як застарілі
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хешує пароль через Bcrypt.
    Кожного разу генерує РІЗНИЙ хеш (через унікальну сіль),
    але verify_password() завжди правильно перевірить будь-який з них.
    
    Приклад: hash_password("qwerty") -> "$2b$12$abc123..."
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє чи відповідає введений пароль збереженому хешу.
    
    plain_password  — пароль який ввів користувач
    hashed_password — хеш з бази даних
    
    Повертає True якщо пароль правильний, False якщо ні.
    """
    return pwd_context.verify(plain_password, hashed_password)