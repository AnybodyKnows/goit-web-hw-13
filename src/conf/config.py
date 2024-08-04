from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY_JWT: str
    ALGORITHM: str
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str
    CLD_API_KEY: int
    CLD_API_SECRET: str

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, value):
        if value not in ["HS256", "HS512"]:
            raise ValueError("Invalid algorithm. Choose either HS256 or RS256.")
        return value


    model_config = ConfigDict(extra='ignore', env_file = ".env", env_file_encoding = "utf-8")  # noqa


config = Settings()







