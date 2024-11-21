from os.path import isfile
from datetime import datetime, timedelta
from sqlite3 import connect, Connection, Cursor
from config import DATABASE_PATH

if isfile(DATABASE_PATH):
    database: Connection = connect(DATABASE_PATH)
else:
    database: Connection = connect(DATABASE_PATH)
    database.execute(
        """CREATE TABLE USERDATA"""
        """("""
        """ id INT PRIMARY KEY  NOT NULL,"""
        """ datetime TEXT       NOT NULL,"""
        """ score INT           NOT NULL,"""
        """ field TEXT          NOT NULL,"""
        """ result INT          NOT NULL"""
        """);"""
    )
cursor: Cursor = database.cursor()


def get_data(select: str, where: str | None = None):
    if where is None:
        return cursor.execute(
            f"""SELECT {select} FROM USERDATA"""
        ).fetchall()
    return cursor.execute(
        f"""SELECT {select} FROM USERDATA WHERE {where}"""
    ).fetchall()


def add_data(score: timedelta, field: str, result: int):
    cursor.execute(
        """INSERT INTO USERDATA("""
        """ id, datetime, score, field, result"""
        """) VALUES ("""
        f"""{datetime().now().strptime('%H:%M %d.%m.%y')},"""
        f"""{get_data('id')[-1] + 1}, {str(score)}, {field}, {result}"""
        """)"""
    )
