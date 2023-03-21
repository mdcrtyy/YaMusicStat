"""
Модуль, вовзращающий список жанров на русском
"""

import re
import requests
from bs4 import BeautifulSoup as bs


def get_all_genres(url='https://music.yandex.ru/genres'):
    genres_list = []
    request = requests.get(url)
    soup = bs(request.text, "html.parser")

    genres_block = soup.find('div',
                             class_='page-main__metatags-line page-main__metatags-line_deep '
                                    'page-main__metatags-line_columns page-main__metatags-line_columns-c4')
    genres = genres_block.find_all('a', class_='d-link deco-link page-main__metatags-link')
    for genre in genres:
        genres_list.append(genre.text.lower())
        print(genre.text.lower())
    return genres_list


print(get_all_genres())
