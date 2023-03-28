from src.db.db_connection import connect
from src.logger.logger import *
import datetime
import os
import sys

filename = os.path.basename(sys.argv[0])
migration_name = f'migration_{filename}_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log'
logger = setup_logger(migration_name)

logger.info(f'Starting migration {migration_name}')

try:
    conn = connect()
except Exception as e:
    logger.error(f'Error connecting to database: {e}')
    raise

try:
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE artists
    (
        id INTEGER PRIMARY KEY,
        artist_name varchar(64) not null,
        artist_description varchar (512)
    );
    
    CREATE TYPE federal_district AS ENUM  ('Центральный', 'Северо-Западный', 'Южный', 'Приволжский', 'Уральский', 'Сибирский', 'Дальневосточный', 'Северо-Кавказский');
    
    CREATE TABLE regions
    (
        id serial primary key,
        region_name varchar(64) not null,
        population integer,
        federal_district federal_district,
        CHECK (population >= 0)
    );
    
    CREATE TABLE genres
    (
        id serial primary key,
        genre_name varchar(64) not null,
        genre_description varchar (512)
    );
    
    CREATE TABLE artist_genres
    (
        fk_artist_id integer references artists,
        fk_genre_id serial references genres,
        UNIQUE (fk_artist_id, fk_genre_id)
    );
    
    CREATE TABLE artists_data
    (
        id serial primary key,
        fk_data_artist_id integer references artists,
        listeners integer,
        likes integer,
        date date not null ,
        UNIQUE (fk_data_artist_id, date),
        CHECK ( listeners >= 0 and likes >= 0)
    );
    
    CREATE TABLE regions_artists
    (
        fk_region_id serial references regions,
        fk_artist_id integer references artists,
        region_listeners integer,
        date date not null,
        UNIQUE (fk_region_id, fk_artist_id, date),
        CHECK ( region_listeners >= 0 )
    );
    ''')
    cur.close()
    conn.commit()
except Exception as e:
    logger.error(f'Error executing migration: {e}')
    conn.rollback()
    raise
finally:
    conn.close()

logger.info(f'Migration {migration_name} completed successfully')
