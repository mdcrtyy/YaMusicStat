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
    ALTER TABLE genres ADD CONSTRAINT UniGenres UNIQUE (genre_name);
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
