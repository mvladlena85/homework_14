import sqlite3
from flask import jsonify, Response


def db_request(query: str) -> list:
    """
    Выполнение запроса к БД
    :param query: str
        SQL запрос
    :return: list
        Результат выполнения запроса
    """
    with sqlite3.connect('netflix.db') as con:
        cursor = con.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_film_by_title(title: str) -> Response:
    """
    Поиск по названию фильма. Если таких фильмов несколько, выведите самый свежий.
    :param title: str
        Название фильма
    :return: Response
        JSON вида:
            {"title": "title",
                "country": "country",
                "release_year": 2021,
                "genre": "listed_in",
                "description": "description"
            }
    """
    query_by_title = f'''SELECT title, country, release_year, listed_in, description 
                                FROM netflix 
                                WHERE title LIKE "{title}" 
                                ORDER BY release_year DESC 
                                LIMIT 1'''
    result = db_request(query_by_title)
    return jsonify({
        "title": result[0][0],
        "country": result[0][1],
        "release_year": result[0][2],
        "genre": result[0][3],
        "description": result[0][4]
    })


def get_films_in_year_range(from_year: int, to_year: int) -> Response:
    """
    Поиск по диапазону лет выпуска.
    :param from_year: int
        Начало диапазона
    :param to_year: int
        Конец диапазона
    :return: Response
        JSON вида:
            [{"title":"title",
                "release_year": 2021},...]
    """
    query = f'''SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {from_year} AND {to_year}
                        LIMIT 100'''
    res = db_request(query)
    result_list = []
    for row in res:
        result_list.append({"title": row[0],
                            "release_year": row[1]})
    return jsonify(result_list)


def get_films_by_rating(rating_list: list) -> Response:
    """
    Поиск по рейтингу
    :param rating_list: list
        Список спец. обозначений рейтингов
    :return: Response
        JSON вида:
            [{"title":"title",
            "rating": "rating",
            "description":"description"
            },...]
    """
    rating = "', '".join(rating_list)
    query = f'''SELECT title, rating, description
                FROM netflix
                WHERE rating IN ('{rating}')'''
    res = db_request(query)
    result_list = []
    for row in res:
        result_list.append({"title": row[0],
                            "rating": row[1],
                            "description": row[2]})
    return jsonify(result_list)


def get_films_by_genre(genre: str) -> Response:
    """
    Получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов в формате json.
    :param genre: str
        название жанра
    :return: Response
        JSON вида:
            [{"title":"title",
                "description":"description"}]
    """
    query = f'''SELECT title, description, listed_in
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10'''
    # print(query)
    res = db_request(query)
    result_list = []
    for row in res:
        result_list.append({"title": row[0],
                            "description": row[1]})
    return jsonify(result_list)


def get_actors(first_actor: str, second_actor: str) -> list:
    """
    Получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз.
    :param first_actor: str
        Имя актера
    :param second_actor: str
        Имя актера
    :return: list
        Список тех, кто играет с ними в паре больше 2 раз.
    """
    query = f'''SELECT netflix.cast
                    FROM netflix
                    WHERE netflix.cast LIKE ('%{first_actor}%')
                        AND netflix.cast LIKE ('%{second_actor}%')'''
    res = db_request(query)
    actor_list = []
    costars = []
    for row in res:
        actor_list.extend(row[0].split(", "))
        actor_list.remove(first_actor)
        actor_list.remove(second_actor)
    actor_set = set(actor_list)
    for actor in actor_set:
        # print(f'{actor}: {actor_list.count(actor)}')
        if actor_list.count(actor) > 2:
            costars.append(actor)
    # print(costars)
    return costars


def get_films_by_type_year_genre(type_: str, year: int, genre: str) -> list:
    """
    Поиск по типу картины (фильм или сериал), году выпуска и ее жанру
    :param type_: str
        тип картины
    :param year: int
        год выпуска
    :param genre: str
        жанр картины
    :return: list
        JSON вида:
            [{"title":"title",
                "description":"description"}]
    """
    query = f'''SELECT type, title, release_year, listed_in, description
                        FROM netflix
                        WHERE type = '{type_}'
                            AND release_year = {year}
                            AND listed_in LIKE \'%{genre}%\''''
    res = db_request(query)
    result = []
    for row in res:
        result.append({"title": row[1],
                       "description": row[4]})
    print(result)
    return result


# get_films_by_type_year_genre('Movie', 2020, 'Thriller')
# get_actors('Jack Black', 'Dustin Hoffman')
# get_actors('Rose McIver', 'Ben Lamb')
