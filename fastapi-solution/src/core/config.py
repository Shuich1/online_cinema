import os

from pydantic import BaseSettings, Field


class TracerSettings(BaseSettings):
    TRACER_ENABLED: bool = Field(True, env='TRACER_ENABLED')
    CONSOLE_TRACING_ENABLED: bool = Field(False, env='CONSOLE_TRACING_ENABLED')
    TRACER_HOST: str = Field('localhost', env='TRACER_HOST')
    TRACER_PORT: int = Field(6831, env='TRACER_PORT')


class Settings(BaseSettings):
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    elastic_host: str = Field(..., env='ELASTIC_HOST')
    elastic_port: int = Field(9200, env='ELASTIC_PORT')

    fastapi_host: str = Field('0.0.0.0', env='FASTAPI_HOST')
    fastapi_port: int = Field(..., env='FASTAPI_PORT')

    project_name: str = Field('Online-cinema', env='PROJECT_NAME')

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    logging_level: str = Field('INFO', env='LOGGING_LEVEL')

    tracer = TracerSettings()
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
