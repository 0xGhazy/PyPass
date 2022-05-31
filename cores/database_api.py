import os
import sqlite3
class Database:


    def __init__(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.db_name = "PyPassdb.sqlite3"
        self.db_connection = self.db_connect()
        self.create_tables()
        self.response_data = ""

    def db_connect(self) -> sqlite3:
        try:
            connection = sqlite3.connect(self.db_name)
        except Exception as error:
            print(f"[-] Error message: {error}")
        finally:
            return connection

    def create_tables(self):
        try:
            cursor = self.db_connection.cursor()
            UserPass = """
            CREATE TABLE IF NOT EXISTS Accounts (
                ID integer PRIMARY KEY AUTOINCREMENT,
                ApplicationName TEXT not null,
                Account TEXT not null,
                EncryptedPassword TEXT not null,
                unique (ApplicationName, Account)
            );
            """

            users_table = """
            CREATE TABLE IF NOT EXISTS Users(
                UID integer PRIMARY KEY AUTOINCREMENT,
                UserName TEXT NOT NULL,
                UserPass TEXT NOT NULL,
                unique (UserName, UserPass)
            );
            """
            self.response_data = cursor.execute(UserPass)
            self.response_data = cursor.execute(users_table)
            self.db_connection.commit()
        except Exception as error:
            print(f"[-] Erro Message:\n{error}\n")

    def db_query(self, query: str) -> str:
        try:
            connector = self.db_connect()
            cursor = connector.cursor()
            self.response_data = cursor.execute(f"""{query}""")
            connector.commit()
        except Exception as error:
            return f"Error: {error}"
        finally:
            return self.response_data

if __name__ == "__main__":
    x = Database()
    x.db_connect()
