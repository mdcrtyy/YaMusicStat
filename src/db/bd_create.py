import psycopg2
from bd_insert import connect

conn = connect()

cur = conn.cursor()
cur.execute('''
CREATE TABLE federal_districts
(
    id varchar primary key,
    district_name varchar(64) not null
);

CREATE TABLE regions
(
    id varchar primary key,
    region_name varchar(64) not null,
    population integer not null,
    fk_federal_dist varchar references federal_districts
);

CREATE TABLE artists
(
    id INTEGER PRIMARY KEY,
    artist_name varchar(64) not null,
    artist_description varchar (512)
);

CREATE TABLE genres
(
    id varchar primary key,
    genre_name varchar(64) not null,
    genre_description varchar (512)
);

CREATE TABLE artist_genres
(
    id serial primary key,
    fk_artist_id integer references artists,
    fk_genre_id varchar references genres,
    UNIQUE (fk_artist_id, fk_genre_id)
);

CREATE TABLE artists_data
(
    id serial primary key,
    fk_data_artist_id integer references artists,
    listeners integer not null,
    likes integer not null,
    date date,
    UNIQUE (fk_data_artist_id, date),
    CHECK ( listeners >= 0 and likes >= 0)
);

CREATE TABLE regions_artists
(
    id serial primary key,
    fk_region_id varchar references regions,
    fk_artist_id integer references artists,
    region_listeners integer,
    date date,
    UNIQUE (fk_region_id, fk_artist_id, date),
    CHECK ( region_listeners >= 0 )
);
''')


cur.close()
conn.commit()
conn.close()

