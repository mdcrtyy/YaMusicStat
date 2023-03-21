import asyncio
import time
import json
import datetime

from src.parser.artist_data_parser import *
from src.parser.genre_page_data_parser import *


async def main():
    start_time = time.time()
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    tasks = []

    genre_list = ['инди', 'рок']

    data = get_all_data_for_all_pages_and_genres(genre_list)
    ids = list(set(data.keys()))

    # TODO: Вынести в отдельную функцию
    for idd in ids:
        tasks.append(asyncio.create_task(get_artists_data(f'https://music.yandex.ru/artist/{idd}/info')))
        await asyncio.sleep(0.05)
        time.sleep(0.01)
    results = await asyncio.gather(*tasks)

    for idd, result in zip(ids, results):
        result['date'] = date_today
        data[idd].update(result)

    final_data = {}

    for key, value in data.items():
        final_data[key] = value

    # TODO: Доделать наименования файлов в соответствии с собранными жанрами и количеством страниц

    with open(f'../data/output/artists_{date_today}_{genre_list[0]}.json', 'w', encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    end_time = time.time()

    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} сек.')


if __name__ == '__main__':
    asyncio.run(main())
