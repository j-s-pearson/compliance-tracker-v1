import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path


class Database:
    def __init__(self, connection_string: str) -> None:
        self.__connection_string = connection_string
        self.__create_db_path()
        self.__up()

    def __get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.__connection_string)

    def __create_db_path(self) -> None:
        connection_path = Path(self.__connection_string)
        connection_path.parent.mkdir(exist_ok=True)

    @contextmanager
    def __transaction(self):
        with closing(self.__get_connection()) as con, con:
            yield con

    @contextmanager
    def __read(self):
        with closing(self.__get_connection()) as con:
            yield con

    def __up(self) -> None:
        document_stmt = """
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            notify_at INTEGER NOT NULL,
            status TEXT NOT NULL,
            last_notified TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );"""
        with self.__transaction() as con:
            con.execute(document_stmt)

    def add(self, title: str, expires: str, notify: int, status: str, now: str) -> None:
        add_stmt = """
        INSERT INTO documents (
            title, expires_at, notify_at, status, created_at, updated_at
        ) VALUES(
            ?, ?, ?, ?, ?, ?
        );"""

        with self.__transaction() as con:
            con.execute(add_stmt, (title, expires, notify, status, now, now))

    def list(self) -> list:
        select_stmt = "SELECT id, title, expires_at, notify_at, status FROM documents"

        with self.__read() as con:
            cur = con.execute(select_stmt)
            return cur.fetchall()

    def update(self, id: int, title: str|None, expires_at: str|None, notify_at: str|None, status: str|None, updated_at: str) -> None:
        update_stmt = "UPDATE documents SET\n"
        params = ()

        if title:
            update_stmt += "\ttitle = ?,\n"
            params += (title,)

        if expires_at:
            update_stmt += "\texpires_at = ?,\n"
            params += (expires_at,)

        if notify_at:
            update_stmt += "\tnotify_at = ?,\n"
            params += (notify_at,)

        if status:
            update_stmt += "\tstatus = ?,\n"
            params += (status,)

        update_stmt += "\tupdated_at = ?\n"
        update_stmt += "WHERE id = ?;"
        params += (updated_at, id)

        with self.__transaction() as con:
            con.execute(update_stmt, params)

    def delete(self, id:int) -> None:
        delete_stmt = "DELETE FROM documents WHERE id = ?"

        with self.__transaction() as con:
            con.execute(delete_stmt, (id,))
