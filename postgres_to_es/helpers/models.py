from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FilmWork:
    id: str = field(default='')
    title: str = field(default='')
    description: str = field(default='')
    rating: float = field(default=0.0)
    type: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    persons: list = field(default_factory=list)
    genres: list = field(default_factory=list)


@dataclass
class Person:
    id: str = field(default='')
    full_name: str = field(default='')
    roles: list = field(default_factory=list)
    film_ids: str = field(default='')
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Genre:
    id: str = field(default='')
    name: str = field(default='')
    updated_at: datetime = field(default_factory=datetime.now)
