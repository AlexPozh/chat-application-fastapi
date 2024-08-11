from config import JWTConfig

from datetime import datetime, timedelta, UTC

import jwt

import bcrypt


"""СОЗДАНИЕ И РАСШИФРОВКА JWT-ТОКЕНА"""
# создаем ЭК конфига JWT
jwt_config = JWTConfig()

def encode_jwt(
            payload: dict[str, str | int | None], 
            key: str = jwt_config.key, 
            algorithm: str = jwt_config.algorithm
    ):
    # добавляем в нагрузку время жизни токена. Вычисляем как "время сейчас по UTC" + "время жизни токена" 
    payload["exp"] = datetime.now(UTC) + timedelta(minutes=jwt_config.expr_time)

    # добавялем в нагрузку дату и время выпуска токена
    payload["iat"] = datetime.now(UTC)

    # создаем закодированный jwt токен
    encoded_jwt = jwt.encode(payload=payload, key=key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt(
            jwt_token: str | bytes,
            key: str = jwt_config.key, 
            algorithm: str = jwt_config.algorithm
):
    # декодируем полученный jwt токен
    decoded_jwt = jwt.decode(jwt=jwt_token, key=key, algorithms=[algorithm])
    return decoded_jwt


"""ХЕШИРОВАНИЕ И ПРОВЕРКА ПАРОЛЯ"""
def hash_password(
        password: str) -> bytes:
    # перводим строку пароля в байты (ф-ция encode()) и генерируем рандомную соль при помощи bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(
        password: str,
        hashed_password: bytes) -> bool:
    # проверяем на равенство переданный пароль (преобразуем в байты) и захешированный из БД
    return bcrypt.checkpw(password.encode(), hashed_password)