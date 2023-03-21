"""
Модуль, содержащий функцию, возвращающую словарь, включающий число слушателей,
число лайков и статистику по регоинам. На вход функции дается ссылка на артиста
'Listeners': listenersCount, 'Likes': likesCount, 'Regions': DictOfRegions
"""
import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup as bs


async def get_artists_data(url):
    await asyncio.sleep(1)
    info = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()

                soup = bs(html, "html.parser")

                # получаю число слушателей
                listeners_count = soup.find('div', {'class': 'page-artist__summary typo deco-typo-secondary'}).find(
                    'span', {
                        'class': False}).text.replace(' ', '')

                # получаю число лайков
                likes_count = soup.find('span', {'class': 'd-button__label'}).text.replace(' ', '')

                # получаю словарь для регионов, где ключ - регион, значение - количество слушателей
                reg_dict = {}
                regions = soup.find_all('span', class_='page-artist__region-caption typo')
                count = soup.find_all('span', class_='page-artist__region-count typo')

                if len(regions) != len(count):
                    raise Exception("Number of regions and counts do not match")

                for i in range(min(10, len(regions))):
                    reg_dict[regions[i].text] = int(count[i].text.replace(' ', ''))
                info = {'Listeners': int(listeners_count), 'Likes': int(likes_count), 'Regions': reg_dict}

    except Exception as e:
        print(f'Error: {e}')
        print(url)
    return info
