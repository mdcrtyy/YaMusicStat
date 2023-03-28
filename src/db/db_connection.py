import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

user = os.getenv('USER')
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')


def connect():
    """
    Подключение к базе данных
    :return:
    """
    try:
        conn = psycopg2.connect(
            user=user,
            host=host,
            port=port,
            database=database
        )
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to database: ", e)
