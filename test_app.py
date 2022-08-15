import pytest
import run
from db_queries import get_actors, get_films_by_type_year_genre


@pytest.fixture()
def test_client():
    app = run.app
    return app.test_client()


def test_film_by_title(test_client):
    response = test_client.get('/movie/A 3 Minute Hug/', follow_redirects=True)
    assert response.status_code == 200, "Статус-код запроса не ок"
    data = response.get_json()
    assert type(data) == dict
    assert set(data.keys()) == set(['country', 'description', 'genre', 'release_year', 'title'])


def test_films_in_year_range(test_client):
    from_year = 2018
    to_year = 2021
    response = test_client.get(f'/movie/{from_year}/to/{to_year}')
    assert response.status_code == 200, "Статус-код запроса не ок"
    data = response.get_json()
    assert type(data) == list
    assert set(data[0].keys()) == set(['release_year', 'title'])
    assert len(data) == 100


def test_films_by_rating(test_client):
    ratings = ['children', 'family', 'adult']
    for rating in ratings:
        if rating == 'children':
            rating_list = ['G']
        if rating == 'family':
            rating_list = ['G', 'PG', 'PG-13']
        if rating == 'adult':
            rating_list = ['R', 'NC-17']
        response = test_client.get(f'/rating/{rating}')
        assert response.status_code == 200, "Статус-код запроса не ок"
        data = response.get_json()
        assert type(data) == list
        for item in data:
            assert item['rating'] in rating_list
        assert set(data[0].keys()) == set(['rating', 'title', 'description'])


def test_films_by_genre(test_client):
    response = test_client.get('/genre/Thriller')
    assert response.status_code == 200, "Статус-код запроса не ок"
    data = response.get_json()
    assert type(data) == list
    assert set(data[0].keys()) == set(['title', 'description'])


actors_list = [('Jack Black', 'Dustin Hoffman', ['David Cross', 'Seth Rogen']),
               ('Rose McIver', 'Ben Lamb', ['Alice Krige', 'Honor Kneafsey'])]


@pytest.mark.parametrize('first_actor, second_actor, co_actors', actors_list)
def test_get_actors(first_actor, second_actor, co_actors):
    result = get_actors(first_actor, second_actor)
    assert set(result) == set(co_actors)


def test_get_films_by_type_year_genre():
    result = get_films_by_type_year_genre('Movie', 2020, 'Thriller')
    assert type(result) == list
    assert set(result[0].keys()) == set(['title', 'description'])

