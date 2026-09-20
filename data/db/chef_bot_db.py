from asyncpg import Pool

from data.config import db_data
import asyncpg

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_pool():
    connection_pool = None
    try:
        connection_pool = await asyncpg.create_pool(
            host=db_data['host'],
            port=db_data['port'],
            database=db_data['database'],
            user=db_data['user'],
            password=db_data['password'],
            min_size=1,
            max_size=20,
            command_timeout=60,
            timeout=30,
            max_inactive_connection_lifetime=300.0,
            statement_cache_size=0,
        )

    except Exception as err_:
        logger.error(f"Ошибка подключения: {err_}")

    return connection_pool


class PoolConnection:

    def __init__(self, pool: Pool):
        self.pool = pool


    async def _execute(self, operation: str, sql_query: str, *args):
        """
        Функция выполнения sql-запроса
        :param operation: операция выполнения запроса
        "execute" - выполнить запрос на изменение в таблице
        "fetch" - получение данных из таблицы
        :param sql_query: sql-запрос
        :param args: дополнительные аргументы для вставки значений
        :return:
        """
        conn = None
        data = None

        try:
            conn = await self.pool.acquire()

            if operation == "execute":
                await conn.execute(sql_query, *args,)
            elif operation == "fetch":
                data = await conn.fetch(sql_query, *args)

        except Exception as err_:
            logger.error(f"Ошибка выполнения sql-запроса: {err_}")
        finally:
            await conn.close()
        return data


    async def add_user(self, user_id, username, fullname):
        query = """INSERT INTO public.users (userid, username, fullname)
                    VALUES ($1, $2, $3);"""

        await self._execute("execute", query, user_id, username, fullname)


    async def get_user(self, user_id):
        query = """SELECT (userid, username, fullname) FROM public.users
                                    WHERE "userid"=$1"""

        data_row = await self._execute("fetch", query, user_id)
        if not data_row:
            return None
        values = data_row[0][0]
        data = {"userid": values[0], "username": values[1], "fullname": values[2]}

        return data


    async def del_user(self, user_id):
        query = """DELETE FROM public.users
                    WHERE "userid"=$1;"""

        await self.del_all_saves(user_id)
        await self._execute("execute", query, user_id)


    async def saves_add(self, user_id, title, content):
        query = """INSERT INTO public.saved (userid, title, content)
                    VALUES ($1, $2, $3);"""

        await self._execute("execute", query, user_id, title, content)


    async def get_save(self, user_id, save_id):
        query = """SELECT (saveid, userid, title, content) FROM public.saved
                    WHERE "saveid"=$1 AND "userid"=$2;"""

        data_row = await self._execute("fetch", query, save_id, user_id)
        values = data_row[0][0]
        data = {"saveid": values[0], "userid": values[1], "title": values[2], "content": values[3]}

        return data


    async def get_all_saves(self, user_id):
        query = """SELECT (saveid, userid, title, content) FROM public.saved
                   WHERE "userid"=$1;"""

        data_rows = await self._execute("fetch", query, user_id)

        if not data_rows:
            return None

        data = {}

        for row in data_rows:
            row_data = row[0]
            saveid = str(row_data[0])
            userid = row_data[1]
            title = row_data[2]
            content = row_data[3]

            data[saveid] = {
                "saveid": saveid,
                "userid": userid,
                "title": title,
                "content": content
            }
        return data


    async def del_save(self, user_id, save_id):
        query = """DELETE FROM public.saved
                    WHERE "saveid"=$1 AND "userid"=$2;"""

        await self._execute("execute", query, save_id, user_id)


    async def del_all_saves(self, user_id):
        query = """DELETE FROM public.saved
                            WHERE "userid"=$1;"""

        await self._execute("execute", query, user_id)


    async def close_pool_connection(self):
        await self.pool.close()

__all__ = ['create_pool', 'PoolConnection']