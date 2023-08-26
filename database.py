from http.client import FOUND
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import MySQLCursor


class AssistantDatabase:
    __slots__ = ("connector", "cursor")
    
    def __init__(self) -> None:
        self.connector: MySQLConnection = connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            database="assistant"
        )
        self.cursor: MySQLCursor = self.connector.cursor()
    
    def add_user(self, user: str, password: str) -> None:
        self.cursor.execute("select U_ID from users where user_name = %s", (user,))
        found = self.cursor.fetchone()

        if found:
            return

        self.cursor.execute("insert into users (User_Name, PWD) values (%s, %s)", (user, password))
        self.connector.commit()
    
    def recognize_user(self, user: str, password: str) -> bool:
        self.cursor.execute("SELECT 1 FROM users WHERE User_Name = %s AND PWD = %s", (user, password))
        found = bool(self.cursor.fetchone())

        return found
