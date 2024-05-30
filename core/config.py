import os

# TODO: we can use a env file to define production creds
# from dotenv import load_dotenv
# load_dotenv()


class Settings:
    PROJECT_NAME: str = "Banking System"
    PROJECT_VERSION: str = "1.0.0"

    DB_USER: str = os.getenv("POSTGRES_USER", "root")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    DB_SERVER: str = os.getenv("POSTGRES_SERVER", "bank_db")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME: str = os.getenv("POSTGRES_DB", "banking_db")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "enigma")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300


settings = Settings()
