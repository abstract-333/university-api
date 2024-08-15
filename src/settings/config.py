import os

from dotenv import load_dotenv

# If .env.local exists it will load it.
# if os.path.exists(".env.local"):
#     load_dotenv(".env.local")
# else:
#     # Otherwise load .env.prod
#     load_dotenv(".env.prod")

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

AUTH_JWT_KEY = os.environ.get("JWT_SECRET_KEY")

SENTRY_URL = os.environ.get("SENTRY_URL")

REDIS_HOST: str | None = os.environ.get("REDIS_HOST")
REDIS_PORT: str | None = os.environ.get("REDIS_PORT")

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST")

YANDEX_API = os.environ.get("YANDEX_API")
