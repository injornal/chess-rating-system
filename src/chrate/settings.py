from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_path: str = "sqlite:///database.db"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        env_prefix = 'CHRATE__'


settings = Settings()
