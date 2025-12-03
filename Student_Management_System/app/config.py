import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT 配置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))


settings = Settings()