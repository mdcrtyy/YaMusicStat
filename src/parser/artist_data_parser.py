"""
Модуль, содержащий функцию, возвращающую словарь, включающий число слушателей,
число лайков и статистику по регоинам. На вход функции дается ссылка на артиста
'Listeners': listenersCount, 'Likes': likesCount, 'Regions': DictOfRegions
"""
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

# TODO: обработать все возможные ошибки, чтобы все работало автономно, починить Error: invalid literal for int() with
#  base 10: 'Отключитьрекламу'
semaphore = asyncio.Semaphore(25)


async def get_artists_data(url, semaphore):
    """
    Функция, заполняющая детальную информацию об артисте - количество слушателей, лайков и статистику по регионам.
    :param url: URL-адрес страницы артиста на music.yandex.ru.
    :param semaphore: семафор для ограничения количества одновременных запросов.
    :return: словарь с информацией об артисте.
    """
    info = {}
    max_attempts = 2  # Максимальное количество попыток
    retry_delay = 1  # Задержка перед повторной попыткой (в секундах)
    try:
        async with semaphore:
            for attempt in range(1, max_attempts + 1):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            html = await response.text()
                            break  # Успешный запрос, выходим из цикла попыток
                except aiohttp.ClientConnectorError as e:
                    if attempt == max_attempts:
                        print(f'Error: {e} after {attempt} attempts')
                        return info  # Возвращаем пустой словарь info после последней попытки
                    else:
                        print(f'Error: {e} on attempt {attempt}, retrying...')
                        await asyncio.sleep(retry_delay)  # Ждем перед следующей попыткой

            soup = bs(html, "html.parser")

            # получаю число слушателей
            listeners_element = soup.find('div', {'class': 'page-artist__summary typo deco-typo-secondary'})
            if listeners_element is not None:
                listeners_count_text = listeners_element.find('span', {'class': False}).text.replace(' ', '')
                listeners_count = int(listeners_count_text) if listeners_count_text.isdigit() else 0
            else:
                print("Ошибка: элемент listeners_count не найден")
                listeners_count = 0

            # получаю число лайков
            likes_element = soup.find('span', {'class': 'd-button__label'})
            if likes_element is not None:
                likes_count_text = likes_element.text.replace(' ', '')
                likes_count = int(likes_count_text) if likes_count_text.isdigit() else 0
            else:
                print("Ошибка: элемент likes_count не найден")
                likes_count = 0

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
        print(listeners_count)
        print(likes_count)
    return info


async def get_data_by_ids(ids):
    """
    Функция для получения информации об артистах по их идентификаторам.
    :param ids: список идентификаторов артистов.
    :param semaphore: семафор для ограничения количества одновременных запросов.
    :return: список словарей с информацией об артистах.
    """
    tasks = []
    for idd in ids:
        tasks.append(asyncio.create_task(get_artists_data(f'https://music.yandex.ru/artist/{idd}/info', semaphore)))
        # await asyncio.sleep(0.05)
    results = await asyncio.gather(*tasks)
    return results
