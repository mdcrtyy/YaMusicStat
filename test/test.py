import json

genre_list = []

with open("../data/output/artists_2023-03-27_['альтернатива', 'инди', 'рок-музыка', 'метал'].json", 'r', encoding="utf-8") as f:
    data_1 = json.load(f)

with open("../data/output/artists_2023-03-26_['поп', 'рэп%20и%20хип-хоп', 'танцевальная%20музыка', 'электроника'].json", 'r', encoding="utf-8") as f:
    data = json.load(f)

with open("../data/input/all_genres.json", 'r', encoding="utf-8") as f:
    exist_data = json.load(f)

for artist_id, artist_data in data_1.items():
    genre = artist_data.get('Genres', '')
    for _ in genre:
        genre_list.append(_)
        genre_list = list(set(genre_list))

for artist_id, artist_data in data.items():
    genre = artist_data.get('Genres', '')
    for _ in genre:
        genre_list.append(_)
        genre_list = list(set(genre_list))

for values in exist_data.values():
    genre_list.append(values)
    genre_list = list(set(genre_list))



print(genre_list)