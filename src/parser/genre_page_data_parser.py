"""
Модуль, который содержит функцию, возвращающую словарь
вида {'id': {'Name': 'name, 'Genre': list_of_artist_genres}}
"""
import re
import requests
from bs4 import BeautifulSoup as bs
import aiohttp


# Функция, получающая айди и имя артистов, пробегая по страницам жанра

async def get_id_name_genres_of_artist(url):
    data = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = bs(text, "html.parser")

        artist_content = soup.find_all('div', class_='artist__content')
        # Общий жанр (Главный жанр)
        main_genre = soup.find('h1', class_='d-header__title-text typo typo-h1_big').text
        for artist in artist_content:
            artist_name = artist.find('a', class_='d-link deco-link', href=True).text
            artist_id = int(
                re.findall(r'^/artist/\s*(.*)', str(artist.find('a', class_='d-link deco-link', href=True)['href']))[0])
            artist_genres = artist.find_all('a', class_='d-link deco-link d-link_muted deco-link_muted')
            list_of_genres = [main_genre.lower()]
            for genre in artist_genres:
                if genre.text != main_genre.lower():
                    list_of_genres.append(genre.text)
            data[artist_id] = {'Name': artist_name, 'Genres': list_of_genres}

    except aiohttp.ClientConnectorError as e:
        print(f'Request failed: {e}')
    except bs.exceptions.BeautifulSoup as e:
        print(f'Failed to parse HTML: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
    finally:
        return data



# Функция, возвращающая жанр страницы
def get_page_genre(url):
    try:
        request = requests.get(url)
        soup = bs(request.text, "html.parser")
        main_genre = soup.find('h1', class_='d-header__title-text typo typo-h1_big').text.replace(' ', '_')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    except bs.exceptions.BeautifulSoup as e:
        print(f'Failed to parse HTML: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
    finally:
        return main_genre


# TODO: Добавить асинхронность вместо цикла
async def get_all_data_for_all_pages_and_genres(list_of_genres):
    data = {}
    for genre in list_of_genres:
        for i in range(101):
            if i == 0:
                url = f'https://music.yandex.ru/genre/{genre}/artists'
                artist_data = await get_id_name_genres_of_artist(url)
                for key, value in artist_data.items():
                    data[key] = value
            else:
                url = f'https://music.yandex.ru/genre/{genre}/artists?page={i}'
                artist_data = await get_id_name_genres_of_artist(url)
                for key, value in artist_data.items():
                    data[key] = value
        print('Информация по страницам жанра собрана \n')
    print('Функция отработала, айди собраны')
    return data

