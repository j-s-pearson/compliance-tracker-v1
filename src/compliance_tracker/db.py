import sqlite3
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

    def __up(self) -> None:
        con = self.__get_connection()
        cur = con.cursor()
        document_cmd = """
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            notify_at TEXT NOT NULL,
            status TEXT NOT NULL,
            last_notified TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );"""
        cur.execute(document_cmd)
        con.close()
