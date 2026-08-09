import psycopg2
from psycopg2 import Error
from data.config import db_data
from psycopg2 import pool

class PoolConnection:
    def __init__(self):
        self.connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            host=db_data['host'],
            port=db_data['port'],
            database=db_data['database'],
            user=db_data['user'],
            password=db_data['password']
        )


    def add_user(self, user_id, username, fullname):
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO public.users
                                    VALUES (%s, %s, %s);""", (user_id, username, fullname,))


    def get_user(self, user_id):
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM public.users
                                    WHERE "userid"=%s""", (user_id,))
                data = cursor.fetchall()
        return data

    def del_user(self, user_id):
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""DELETE FROM public.saved
                    WHERE "userid"=%s""", (user_id,))
                cursor.execute("""DELETE FROM public.users
                    WHERE "userid"=%s""", (user_id,))

    def saves_add(self, user_id, title, content):
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO public.saved (userid, title, content)
                            VALUES (%s, %s, %s);""", (user_id, title, content,))

    def del_save(self, save_id):
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""DELETE FROM public.saved
                    WHERE "saveid"=%s""", (save_id,))