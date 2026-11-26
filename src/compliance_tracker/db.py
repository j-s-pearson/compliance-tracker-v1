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

    def __up(self) -> None:
        document_cmd = """
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
            con.execute(document_cmd)

    def add(self, title: str, expires: str, notify: int, status: str, now: str) -> None:
        add_smt = """
        INSERT INTO documents (
            title, expires_at, notify_at, status, created_at, updated_at
        ) VALUES(
            ?, ?, ?, ?, ?, ?
        );"""

        with self.__transaction() as con:
            con.execute(add_smt, (title, expires, notify, status, now, now))
