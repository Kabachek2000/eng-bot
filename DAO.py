from datetime import datetime
import sqlite3 as SQLite
from sqlite3 import Connection, Cursor
from typing import Any as Unit


class DAO:
    def __init__(self, path: str):
        self.__path: str = path
        self.__ensureCreated()

    def addUser(
            self,
            id_: int,
            score: int = 0,
            lastActivity: datetime = datetime.now()
    ) -> Unit:
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO users VALUES "
                       f"({id_}, {score}, \"{lastActivity.timestamp()}\", {0});")
        connection.commit()
        connection.close()

    def getScore(self, id_: int):
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        q = cursor.execute(f"SELECT score FROM users WHERE id={id_};")
        try:
            return list(q)[0][0]
        except IndexError:
            return None
        finally:
            connection.close()

    def getEnglishLevel(self, id_: int):
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        q = cursor.execute(f"SELECT english_level FROM users WHERE id={id_};")
        try:
            return list(q)[0][0]
        except IndexError:
            return None
        finally:
            connection.close()

    def getLastActivity(self, id_: int):
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        q = cursor.execute(f"SELECT last_activity FROM users WHERE id={id_};")
        try:
            return datetime.fromtimestamp(float(list(q)[0][0]))
        except IndexError:
            return None
        finally:
            connection.close()

    def setScore(self, id_: int, score: int):
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET score={score} WHERE id={id_};")
        connection.commit()
        connection.close()

    def setEnglishLevel(self, id_: int, english_level: int):
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET english_level={english_level} WHERE id={id_};")
        connection.commit()
        connection.close()

    def setLastActivity(self, id_: int, lastActivity: datetime):
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        cursor.execute(f"UPDATE users SET last_activity=\"{str(lastActivity.timestamp())}\" WHERE id={id_};")
        connection.commit()
        connection.close()

    def __ensureCreated(self) -> Unit:
        connection: Connection = SQLite.connect(self.__path)
        cursor: Cursor = connection.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER UNIQUE, 
    "score" INTEGER, 
    "last_activity" TEXT, 
    "english_level" INTEGER,
    PRIMARY KEY("id")
);""".strip())
        connection.commit()
        connection.close()
