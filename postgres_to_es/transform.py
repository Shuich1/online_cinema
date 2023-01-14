import logging


def transformer(data: list) -> list:
    transformed_data = list()
    for row in data:
        transformed_data.append({
            'id': row[0],
            'imdb_rating': row[3],
            'title': row[1],
            'description': row[2],
            'genre': row[8],
            'director': [p['person_name'] for p in row[7] if p['person_role'] == 'director'],
            'actors': [{'id': p['person_id'],
                        'name': p['person_name']} for p in row[7] if p['person_role'] == 'actor'],
            'writers': [{'id': p['person_id'],
                        'name': p['person_name']} for p in row[7] if p['person_role'] == 'writer'],
            'actors_names': [p['person_name'] for p in row[7] if p['person_role'] == 'actor'],
            'writers_names': [p['person_name'] for p in row[7] if p['person_role'] == 'writer'],
        })
    logging.info('Data for ES has been transformed.')
    return transformed_data
