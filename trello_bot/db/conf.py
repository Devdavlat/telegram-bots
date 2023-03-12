import psycopg2

from psycopg2.extras import RealDictCursor
from environs import Env
import queries


def connect():
    env = Env()
    env.read_env()

    return psycopg2.connect(
        dbname=env('DB_NAME'),
        user=env('DB_USER'),
        password=env('DB_PASSWORD'),
        host=env('DB_HOST'),
        port=env('DB_PORT')
    )


conn = connect()
with conn.cursor(cursor_factory=RealDictCursor) as cur:
    cur.execute(query=queries.ALL_USERS)
    data = cur.fetchall()
    print(data)
