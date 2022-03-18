import os
import sqlite3

class Database:
    """DESCRIPTION:

        Class for handling all Methods and interaction with database.

    DATA:

        self.database_name = "PyPassdb.sqlite3"
        self.response_data = ""
        log_obj = log_system class object


    FUNCTIONS:

        db_connect(self: "Database", database_file: str) -> sqlite3
            Connect to database and return sqlite3 connection object.


        db_query(self: "Database", database_file: str, query: str) -> str
            execute the given sql query and return the result

    """

    def __init__(self: "Database") -> None:
        os.chdir(os.path.dirname(__file__))
        self.database_name = "PyPassdb.sqlite3"
        self.response_data = ""


    def db_connect(self: "Database", database_file: str) -> sqlite3:
        try:
            connection = sqlite3.connect(database_file)
        except Exception as error_message:
            print(f"[-] Error message: {error_message}")
        finally:
            return connection


    def db_query(self: "Database", database_file: str, query: str) -> str:
        try:
            connector = self.db_connect(database_file)
            cursor = connector.cursor()
            self.response_data = cursor.execute(f"""{query}""")
            connector.commit()
        except Exception as error_message:
            print(f"[-] Error Message: \n{error_message}\n")
            quit()
        finally:
            return self.response_data