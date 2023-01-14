from django.contrib import admin
from .models import *


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # Фильтрация в списке
    list_filter = ('type',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    search_fields = ['full_name']
