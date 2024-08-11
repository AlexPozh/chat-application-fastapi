from pydantic import BaseModel, EmailStr, Field



class UserAuth(BaseModel):
    login: EmailStr
    password: bytes | str


class UserRegistration(BaseModel):
    login: EmailStr
    password: str = Field(min_length=8)
    username: str = Field(min_length=2, max_length=20)
    phone_number: str | None = None


class TokenInfo(BaseModel):
    access_token: str
    token_type: str