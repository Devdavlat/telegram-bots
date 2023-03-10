import psycopg2

from environs import Env


def connect():
    env = Env()
    env.read_env()
    return psycopg2.connect(
        dbname=env('DB_NAME'),
        dbuser=env('DB_USER'),
        dbhost=env('DB_HOST'),
        dbport=env('DB_PORT')
    )


connection = connect()
