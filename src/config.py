from dataclasses import dataclass

from environs import Env

env = Env()    # создаем ЭК Env()
env.read_env() # читаем переменное окружение


@dataclass
class JWTConfig:
    __secret_key: str = env("SECRET_KEY") # секретный ключ для шифрования
    __algorithm: str = env("ALGORITHM")   # алгоритм шифрования
    _expiration_time: int = int(env("EXPIRATION_TIME"))   # время работы токена (в минутах)

    @property
    def key(self):
        return self.__secret_key
    
    @property
    def algorithm(self):
        return self.__algorithm
    
    @property
    def expr_time(self):
        return self._expiration_time


@dataclass
class DatabaseConfig:
    __db_name: str = env("DB_NAME")
    __db_user: str = env("DB_USER")
    __db_password: str = env("DB_PASSWORD")
    __db_host: str = env("DB_HOST")
    __db_port: int = env("DB_PORT")

    @property
    def DSN(self):
        return f"postgresql+asyncpg://{self.__db_user}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"


