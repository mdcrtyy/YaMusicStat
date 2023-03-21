import json

path = '../data/output/artists_2023-03-18_танцевальная%20музыка.json'

with open(f'{path}', 'r') as f:
    info_about_artist = json.load(f)

with open('../data/input/all_genres.json', 'r') as f:
    genres_data = json.load(f)

artists_genres_list = []
for artist_id, artist_data in info_about_artist.items():
    artist_genres = artist_data.get("Genres", '')
    for genre in artist_genres:
        for key, value in genres_data.items():
            if genre == value:
                artist_genre = key
        artists_genres_list.append((artist_id, artist_genre))

print(artists_genres_list)