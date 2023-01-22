import logging


def transformer(data: list, index_name) -> list:
    transformed_data = list()
    for row in data:
        if index_name == 'movies':
            row_data = {
                'id': row.id,
                'imdb_rating': row.rating,
                'title': row.title,
                'description': row.description,
                'genre': [g['genre_name'] for g in row.genres],
                'genres': [{'id': g['genre_id'], 'name': g['genre_name']} for g in row.genres],
                'director': [p['person_name'] for p in row.persons if p['person_role'] == 'director'],
                'actors': [{'id': p['person_id'],
                            'name': p['person_name']} for p in row.persons if p['person_role'] == 'actor'],
                'writers': [{'id': p['person_id'],
                            'name': p['person_name']} for p in row.persons if p['person_role'] == 'writer'],
                'actors_names': [p['person_name'] for p in row.persons if p['person_role'] == 'actor'],
                'writers_names': [p['person_name'] for p in row.persons if p['person_role'] == 'writer'],
            }
        elif index_name == 'genres':
            row_data = {
                'id': row.id,
                'name': row.name,
            }
        elif index_name == 'persons':
            row_data = {
                'id': row.id,
                'full_name': row.full_name,
                'roles': row.roles,
                'film_ids': row.film_ids[1:-1].split(',')
            }
        transformed_data.append(row_data)
    logging.info('Data for ES has been transformed.')
    return transformed_data
