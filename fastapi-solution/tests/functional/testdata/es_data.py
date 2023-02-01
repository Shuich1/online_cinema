import uuid

movies_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'genres': [
            {'id': '111', 'name': 'Action'},
            {'id': '222', 'name': 'Sci-Fi'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
    } for _ in range(15)] + [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 9.5,
        'genre': ['Comedy', 'Drama'],
        'genres': [
            {'id': '333', 'name': 'Comedy'},
            {'id': '444', 'name': 'Drama'}
        ],
        'title': 'Gentelmen of Fortune',
        'description': 'Old World',
        'director': ['Sery'],
        'actors_names': ['Leonov', 'Vitsin'],
        'writers_names': ['Daneliya', 'Tokareva'],
        'actors': [
            {'id': '333', 'name': 'Leonov'},
            {'id': '444', 'name': 'Vitsin'}
        ],
        'writers': [
            {'id': '555', 'name': 'Daneliya'},
            {'id': '666', 'name': 'Tokareva'}
        ],
    } for _ in range(15)] + [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 7.5,
        'genre': ['Action', 'Drama'],
        'genres': [
            {'id': '111', 'name': 'Action'},
            {'id': '444', 'name': 'Drama'}
        ],
        'title': 'The Avengers',
        'description': 'At any cost',
        'director': ['Russo'],
        'actors_names': ['Robert', 'Chris'],
        'writers_names': ['Stan', 'Jack'],
        'actors': [
            {'id': '777', 'name': 'Robert'},
            {'id': '888', 'name': 'Chris'}
        ],
        'writers': [
            {'id': '999', 'name': 'Stan'},
            {'id': '000', 'name': 'Jack'}
        ],
    } for _ in range(15)] + [{
        'id': '1',
        'imdb_rating': 7.9,
        'genre': ['Comedy', 'Sci-Fi'],
        'genres': [
            {'id': '333', 'name': 'Comedy'},
            {'id': '222', 'name': 'Sci-Fi'}
        ],
        'title': 'The Worlds End',
        'description': 'The end of the world',
        'director': ['Edgar Wright'],
        'actors_names': ['Simon Pegg', 'Nick Frost'],
        'writers_names': ['Edgar Wright', 'Simon Pegg'],
        'actors': [
            {'id': '1110', 'name': 'Simon Pegg'},
            {'id': '2220', 'name': 'Nick Frost'}
        ],
        'writers': [
            {'id': '3330', 'name': 'Edgar Wright'},
            {'id': '4440', 'name': 'Simon Pegg'}
        ],
    }]


persons_data = [{
    'id': str(uuid.uuid4()),
    'full_name': 'Ann Smith',
    'roles': ['Actor', 'Writer'],
    'film_ids': [movie['id'] for movie in movies_data]
} for _ in range(15)] + [{
    'id': str(uuid.uuid4()),
    'full_name': 'Bob Johnson',
    'roles': ['Actor', 'Director'],
    'film_ids': [movie['id'] for movie in movies_data]
} for _ in range(15)] + [{
    'id': str(uuid.uuid4()),
    'full_name': 'Ben Williams',
    'roles': ['Writer', 'Director'],
    'film_ids': [movie['id'] for movie in movies_data]
} for _ in range(15)]

genres_data = [{
    'id': str(uuid.uuid4()),
    'name': 'Action',
} for _ in range(15)] + [{
    'id': str(uuid.uuid4()),
    'name': 'Sci-Fi',
} for _ in range(15)] + [{
    'id': str(uuid.uuid4()),
    'name': 'Comedy',
} for _ in range(15)] + [{
    'id': str(uuid.uuid4()),
    'name': 'Drama',
} for _ in range(15)]