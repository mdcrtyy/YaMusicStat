import asyncio
import time
import json
import datetime
import nest_asyncio

from src.parser.artist_data_parser import *
from src.parser.genre_page_data_parser import *

nest_asyncio.apply()


async def main():
    start_time = time.time()
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")

    genre_list = ['поп', 'рэп%20и%20хип-хоп', 'танцевальная%20музыка', 'электроника']
    genre_list_2 = ['альтернатива', 'инди', 'рок-музыка', 'метал']

    data = get_all_data_for_all_pages_and_genres(genre_list_2)
    ids = list(set(data.keys()))

    results = await get_data_by_ids(ids)

    for idd, result in zip(ids, results):
        result['date'] = date_today
        data[idd].update(result)

    final_data = {}

    for key, value in data.items():
        final_data[key] = value

    # TODO: Доделать наименования файлов в соответствии с собранными жанрами и количеством страниц

    with open(f'../data/output/artists_{date_today}_{genre_list_2}.json', 'w', encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    end_time = time.time()

    total_time = end_time - start_time
    print(f'Время выполнения: {total_time} сек.')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
