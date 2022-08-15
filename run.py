from flask import Flask
from db_queries import get_film_by_title, get_films_in_year_range, get_films_by_rating, get_films_by_genre


app = Flask(__name__)


@app.route('/movie/<title>/')
def film_by_title(title):
    """Поиск по названию фильма"""
    return get_film_by_title(title)


@app.route('/movie/<int:from_year>/to/<int:to_year>')
def films_in_year_range(from_year, to_year):
    """Поиск фильмов по периоду дат создания"""
    return get_films_in_year_range(from_year, to_year)


@app.route('/rating/<rating>')
def films_by_rating(rating):
    """Поиск фильмов по категориям: для детей, семейного просмотра или взрослых"""
    if rating == 'children':
        rating_list = ['G']
    if rating == 'family':
        rating_list = ['G', 'PG', 'PG-13']
    if rating == 'adult':
        rating_list = ['R', 'NC-17']
    return get_films_by_rating(rating_list)


@app.route('/genre/<genre>')
def films_by_genre(genre):
    """Поиск по жанру"""
    return get_films_by_genre(genre)


if __name__ == "__main__":
    app.run()
