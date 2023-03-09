from pydantic import BaseSettings, Field, PostgresDsn


class Database(BaseSettings):
    db: str = Field(..., env='AUTH_POSTGRES_DB')
    user: str = Field(..., env='AUTH_POSTGRES_USER')
    password: str = Field(..., env='AUTH_POSTGRES_PASSWORD')
    host: str = Field(..., env='AUTH_POSTGRES_HOST')
    port: int = Field('5433', env='AUTH_POSTGRES_PORT')


class TracerSettings(BaseSettings):
    TRACER_ENABLED: bool = Field(True, env='TRACER_ENABLED')
    CONSOLE_TRACING_ENABLED: bool = Field(False, env='CONSOLE_TRACING_ENABLED')
    TRACER_HOST: str = Field('localhost', env='TRACER_HOST')
    TRACER_PORT: int = Field(6831, env='TRACER_PORT')


class CaptchaSettings(BaseSettings):
    RECAPTCHA_ENABLED: bool = Field(True, env='RECAPTCHA_ENABLED')
    RECAPTCHA_SECRET_KEY: str = Field(..., env='RECAPTCHA_SECRET_KEY')
    RECAPTCHA_SITE_KEY:str = Field(..., env='RECAPTCHA_SITE_KEY')


class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    FLASK_ADMIN_MAIL: str = Field(..., env='FLASK_ADMIN_MAIL')
    FLASK_ADMIN_PASS: str = Field(..., env='FLASK_ADMIN_PASS')

    AUTH_REDIS_HOST: str = Field(..., env='AUTH_REDIS_HOST')
    AUTH_REDIS_PORT: str = Field(6380, env='AUTH_REDIS_PORT')

    SECURITY_TOKEN_AUTHENTICATION_HEADER: str = Field(..., env='SECURITY_TOKEN_AUTHENTICATION_HEADER')
    SECURITY_PASSWORD_SALT: str = Field(..., env='SECURITY_PASSWORD_SALT')

    yandex_id: str = Field(..., env='YANDEX_ID')
    yandex_secret: str = Field(..., env='YANDEX_SECRET')

    vk_id: str = Field(..., env='VK_ID')
    vk_secret: str = Field(..., env='VK_SECRET')

    pg_db = Database()
    SQLALCHEMY_DATABASE_URI: PostgresDsn = f'postgresql+psycopg2://{pg_db.user}:{pg_db.password}@{pg_db.host}:{pg_db.port}/{pg_db.db}'

    tracer = TracerSettings()

    DEFAULT_RATE_LIMIT: int = Field(10, env='DEFAULT_RATE_LIMIT')
    DEFAULT_RATE_PERIOD: int = Field(60, env='DEFAULT_RATE_PERIOD')
    MAX_RATE_PENALTY: int = Field(1800, env='MAX_RATE_PENALTY')


    reCAPTCHA = CaptchaSettings()


settings = Settings()
db_config = Database()
