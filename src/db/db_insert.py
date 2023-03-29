import psycopg2
import json
from db_connection import connect


def insert_regions_data():
    """
    Вставка данных о регионах в таблицу regions
    :return:
    """
    conn = connect()

    try:
        with open('../../data/input/info_about_regions.json', 'r') as f:
            info_about_regions = json.load(f)

        regions = []
        for region_id, region_data in info_about_regions.items():
            region_name = region_data.get('name', '')
            population = region_data.get('population', '')
            regions.append((region_name, population))

        cur = conn.cursor()

        sql_regions = """INSERT INTO regions(region_name, population)
                     VALUES (%s, %s)"""

        cur.executemany(sql_regions, regions)
        conn.commit()

    except (psycopg2.Error, FileNotFoundError) as e:
        print("Error inserting regions data: ", e)
    finally:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")


def insert_genres_data():
    """
    Вставка данных о жанрах в таблицу genres
    :return:
    """
    conn = connect()

    try:
        with open('../../data/input/genres.json', 'r') as f:
            genres = json.load(f)

        cur = conn.cursor()

        sql_genres = """INSERT INTO genres(genre_name)
                     VALUES (%s)
                     ON CONFLICT (genre_name) DO NOTHING"""

        for genre in genres:
            cur.execute(sql_genres, (genre,))
        conn.commit()
    except (psycopg2.Error, FileNotFoundError) as e:
        print("Error inserting genres data: ", e)
    finally:
        conn.close()
        cur.close()
        print("PostgreSQL connection is closed")


def insert_artist_id_name(path):
    """
    Вставка данных об артисте в таблицу artist
    :param path:
    :return:
    """
    conn = connect()

    try:
        with open(f'{path}', 'r') as f:
            info_about_artist = json.load(f)

        artists = []
        for artist_id, artist_data in info_about_artist.items():
            artist_name = artist_data.get("Name", '')
            artists.append((artist_id, artist_name))

        cur = conn.cursor()

        sql_artists = """INSERT INTO artists(id, artist_name)
                         VALUES (%s, %s)
                         ON CONFLICT (id) DO NOTHING"""

        cur.executemany(sql_artists, artists)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting data to table artists: {error}")

    finally:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")


def insert_artist_data_listeners(path):
    """
    Вставка количества слушателей, лайков и даты в таблицу artists_data
    :param path:
    :return:
    """
    conn = connect()

    try:
        cur = conn.cursor()

        with open(f'{path}', 'r') as f:
            info_about_artist = json.load(f)

        artists_count_of_list = []
        for artist_id, artist_data in info_about_artist.items():
            artist_listeners = artist_data.get("Listeners", '')
            artist_likes = artist_data.get("Likes", '')
            if type(artist_listeners) != int:
                artist_listeners = 0
            if type(artist_likes) != int:
                artist_likes = 0
            date = artist_data.get("date", '')
            artists_count_of_list.append((artist_id, artist_listeners, artist_likes, date))

        sql_artists_data = """INSERT INTO artists_data(fk_data_artist_id, listeners, likes, date)
                         VALUES (%s, %s, %s, %s)
                         ON CONFLICT (fk_data_artist_id, date) DO NOTHING
                         """
        cur.executemany(sql_artists_data, artists_count_of_list)
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting data to table artists_data: {error}")
    finally:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")


def insert_artists_genres(path) -> None:
    """
    Функция для вставки данных в таблицу artists_genres. На вход подается файл с информацией об артистах
    :param path:
    :return:
    """
    conn = connect()

    try:
        cur = conn.cursor()
        with open(f'{path}', 'r') as f:
            info_about_artist = json.load(f)

        with open('../../data/input/all_genres.json', 'r') as f:
            genres_data = json.load(f)

        artists_genres_list = []
        for artist_id, artist_data in info_about_artist.items():
            artist_genres = artist_data.get("Genres", '')
            for genre in artist_genres:
                artist_genre = None
                for key, value in genres_data.items():
                    if genre == value:
                        artist_genre = value
                artists_genres_list.append((artist_id, artist_genre))

        sql_artists_genres = """INSERT INTO artist_genres (fk_artist_id, fk_genre_id)
                            SELECT %s, id FROM genres WHERE genre_name = %s
                            ON CONFLICT (fk_artist_id, fk_genre_id) DO NOTHING
                         """

        cur.executemany(sql_artists_genres, [(artist_id, genre_name) for artist_id, genre_name in artists_genres_list])

        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting data to table artists_data: {error}")
    finally:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")


def insert_regions_artists(path) -> None:
    """
    Функция для вставки данных в таблицу regions_artists. На вход подается файл с информацией об артистах
    :param path:
    :return:
    """
    conn = connect()

    try:
        cur = conn.cursor()
        with open(f'{path}', 'r') as f:
            info_about_artist = json.load(f)

        with open('../../data/input/info_about_regions.json', 'r') as f:
            info_about_regions = json.load(f)

        regions_names_list = []
        for region_id, region_data in info_about_regions.items():
            region_name = region_data.get('name', '')
            regions_names_list.append(region_name)

        artists_regions_list = []
        for artist_id, artist_data in info_about_artist.items():
            date = artist_data.get("date", '')
            artist_regions = artist_data.get('Regions', '')

            if type(artist_regions) != str:
                for region_name, region_listeners in artist_regions.items():
                    if region_name in regions_names_list:
                        artists_regions_list.append((region_name, artist_id, region_listeners, date))
                    else:
                        continue

            else:
                continue

        sql_artists_data = """
                    INSERT INTO regions_artists(fk_region_id, fk_artist_id, region_listeners, date)
                    VALUES ((SELECT id FROM regions WHERE region_name = %s), %s, %s, %s)
                    ON CONFLICT (fk_region_id, fk_artist_id, date) DO NOTHING
                """

        cur.executemany(sql_artists_data, [(artist_region, artist_id, artist_region_listeners, date) for
                                           artist_region, artist_id, artist_region_listeners, date in
                                           artists_regions_list])

        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting data to table artists_regions: {error}")
    finally:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")


def all_insert(path):
    """
    Функция, выполняющая все функции для вставки данных, связанных с артистами
    :param path:
    :return:
    """

    insert_regions_artists(path)
