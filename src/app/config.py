from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAX_UPLOAD_SIZE_MB: int = 100
    MAX_UPLOAD_SIZE_BYTES: int = 100 * 1024 * 1024

    class Config:
        env_file = ".env"

settings = Settings()
