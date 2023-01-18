import dataclasses
from psycopg2 import OperationalError
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch


class PGUploader:
    def __init__(self, connection: _connection):
        self.cursor = connection.cursor()

    def upload_to_pg(self, table: str, data: list):
        data_dict = [dataclasses.asdict(d) for d in data]
        table_cols = (data_dict[0].keys())
        arg_str = '(' + ', '.join(['%s'] * len(table_cols)) + ')'
        exclude_data = ', '.join(['{}=EXCLUDED.{}'.format(col, col) for col in table_cols])
        try:
            execute_batch(self.cursor,
                          """
                              INSERT INTO content.{table_name} ({cols})
                              VALUES {args}
                              ON CONFLICT (id) DO UPDATE SET {exclude}
                          """.format(table_name=table, cols=', '.join(table_cols), exclude=exclude_data, args=arg_str),
                          (tuple(data.values()) for data in data_dict))
        except OperationalError as error:
            print('Insertion error {err}'.format(err=error))
