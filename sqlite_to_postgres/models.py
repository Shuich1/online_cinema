import uuid
from dataclasses import dataclass, fields, field
import dataclasses
from datetime import datetime


@dataclass
class FilmWork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = field(default='')
    description: str = field(default='')
    creation_date: datetime = field(default_factory=datetime.now)
    type: str = field(default='')
    rating: float = field(default=0.0)
    file_path: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if getattr(self, field.name) is None:
                if not isinstance(field.default, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default)
                if not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default_factory())


@dataclass
class Person:
    full_name: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if getattr(self, field.name) is None:
                if not isinstance(field.default, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default)
                if not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default_factory())


@dataclass
class Genre:
    name: str = field(default='')
    description: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if getattr(self, field.name) is None:
                if not isinstance(field.default, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default)
                if not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default_factory())


@dataclass
class PersonFilmWork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if getattr(self, field.name) is None:
                if not isinstance(field.default, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default)
                if not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                    setattr(self, field.name, field.default_factory())


@dataclass()
class GenreFilmWork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if getattr(self, field.name) is None and not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                setattr(self, field.name, field.default_factory())
