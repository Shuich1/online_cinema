import asyncio

import pytest

pytest_plugins = [
    'functional.fixtures.elasticsearch',
    'functional.fixtures.redis',
    'functional.fixtures.fastapi',
]

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
