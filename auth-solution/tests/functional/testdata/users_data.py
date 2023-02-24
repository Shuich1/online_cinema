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

test_user_change = User(
    email=faker.email(),
    password=faker.password()
)

unregistered_email = faker.email()

superuser = User(
    email=test_settings.admin_email,
    password=test_settings.admin_password
)

invalid_refresh_token = 'aWF0IjoxNTE2MNNpdsixgA'

test_auth_history = {
    "auth_data": "Fri, 24 Feb 2023 10:52:57 GMT",
    "created": "Fri, 24 Feb 2023 10:48:41 GMT",
    "host": "127.0.0.1:5000",
    "id": "fe77ca98-3ec1-4e42-86ef-f47b36e749c5",
    "user_agent": "PostmanRuntime/7.29.2",
    "user_id": "557adf51-ff0e-4dce-8706-d7da61795067"
}
