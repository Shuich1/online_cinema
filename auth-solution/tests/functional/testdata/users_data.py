from pydantic import BaseModel
from faker import Faker
from ..settings import test_settings

class User(BaseModel):
    email: str
    password: str


faker = Faker()

test_user = User(
    email=faker.email(),
    password=faker.password()
)

unregistered_email = faker.email()

superuser = User(
    email=test_settings.admin_email,
    password=test_settings.admin_password
)

invalid_refresh_token = 'aWF0IjoxNTE2MNNpdsixgA'