from pydantic import BaseSettings, Field

from .testdata.es_mapping import index_mappings


class TestSettings(BaseSettings):
    es_url: str = Field('http://elastic_test:9200', env='ES_TEST_URL')
    es_index: str = Field('movies', env='ES_INDEX')
    es_id_field: str = Field('id', env='ES_ID_FIELD')
    es_index_mapping: dict = Field(index_mappings)

    redis_host: str = Field('redis_test', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    service_url: str = Field('http://127.0.0.1:80', env='FASTAPI_URL')


test_settings = TestSettings()