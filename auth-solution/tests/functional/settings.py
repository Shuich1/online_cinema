from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_host: str = Field(..., env='FLASK_HOST')
    service_port: str = Field(..., env='FLASK_PORT')
    
    service_url: str = Field(..., env='FLASK_URL')

    admin_email: str = Field(..., env='FLASK_ADMIN_MAIL')
    admin_password: str = Field(..., env='FLASK_ADMIN_PASS')

test_settings = TestSettings()