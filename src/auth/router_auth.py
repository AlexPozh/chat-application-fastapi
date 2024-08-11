from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from datetime import datetime, timedelta

from jwt.exceptions import InvalidTokenError

from auth.schemas import TokenInfo, UserAuth, UserRegistration
from auth.auth_exception import InvalidData, InvalidToken
from auth.utils import encode_jwt, decode_jwt, hash_password, check_password

from typing import Annotated


router = APIRouter(prefix="/auth", tags=["Auth"])


http_bearer = HTTPBearer()
# oauth2_pswd = OAuth2PasswordBearer(
#     tokenUrl="/auth/login/"
# )


fake_db = [
    UserAuth(login="pozhsasha@gmail.com", password=hash_password("123456789")), 
    UserAuth(login="natasha@gmail.com", password=hash_password("1234567891")),
    UserAuth(login="PavelPupil@mail.ru", password=hash_password("1234567899"))
]


def check_user_data(login: Annotated[str, Form()], password: Annotated[str, Form()]):
    #TODO здесь будет вызываться метод для получения пользователя из БД.
    print(f"login: {login}\npassword: {password}")

    user = [user for user in fake_db if user.login == login]
    if user == []:
        raise InvalidData(detail="Invalid data. Check your login and try again or login up.")
    
    # user[0].password имеет захешированный пароль, т.к. мы достаем эту запись из БД
    if check_password(password, user[0].password):
        return user[0]
    raise InvalidData(detail="Invalid data. Check your password and try again or login up.")


@router.post("/login/", response_model=TokenInfo)
async def login_user(user: UserAuth = Depends(check_user_data)):
    # создаем полезную нагрузку для jwt токена
    jwt_payload = {
        "sub": user.login,
        "role": "user" if "admin" not in user.login else "admin",
    }

    jwt_token = encode_jwt(payload=jwt_payload)
    return TokenInfo(
        access_token=jwt_token,
        token_type="Bearer"
    )

# Проврка токена на валидность
def check_jwt_token(
        cred: HTTPAuthorizationCredentials = Depends(http_bearer)
        # token: str = Depends(oauth2_pswd)
    ) -> UserAuth:

    try:
        token = cred.credentials # для bearer
        # print(token)
        
        payload = decode_jwt(jwt_token=token)
        user = [user for user in fake_db if user.login == payload["sub"]]
        if user == []:
            raise InvalidData(detail="Invalid data. Check your login and try again or login up.")
        else:
            return user[0]

    except InvalidTokenError as error:
        # FOR TEST EXCEPTION INFO raise InvalidToken(detail=f"Invalid token.\n{error}")
        raise InvalidToken(detail=f"Invalid token.")


@router.get("/main_page")
async def get_main_page(
    user: UserAuth = Depends(check_jwt_token)) -> dict:
    
    return {
            "message": "This is the main page",
            "greeting": f"Hello, {user.login}"
        }
