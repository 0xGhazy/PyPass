import os
import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic, QtGui
from cores.database_api import Database
from cores.logsystem import LogSystem
from threading import Thread


signin_UI = Path(__file__).parent.parent / 'ui' / 'signin_screen.ui'

class LoginScreen(QtWidgets.QDialog):
    """ Provide a login screen to uncrease the user privacy """

    def __init__(self: "LoginScreen") -> None:
        """ initialize the application with it's UI and utility methods """
        super(LoginScreen, self).__init__()
        os.chdir(os.path.dirname(__file__))
        # loading .ui design file.
        uic.loadUi(signin_UI, self)
        self.db_obj = Database()
        self.login_user_line.setText(self.get_first_user())
        self.log_obj = LogSystem()
        self.login_button.clicked.connect(self.login)
        self.show()

    def get_first_user(self):
        db_response = self.db_obj.db_query(f"SELECT * FROM Users")
        if db_response != None:
            username = list(db_response)[0][1]
            return username


    def login(self):
        """ Validate the provided username and password and call the main application. """
        
        # [+] Connecting to database
        login_username = self.login_user_line.text()
        login_password = self.login_password_line.text()

        # check for empty text
        if len(login_password) < 1 or len(login_username) < 1:
            self.status.setText("Can't let Username or Password empty !!")
        else:
            # Validate username and password.
            db_response = self.db_obj.db_query(f"SELECT * FROM Users")
            for record in list(db_response):
                user_id, user_name, password = record
                if login_username == user_name and login_password == password:
                    # Add log record to Logs.txt
                    self.log_obj.write_into_log("+", f"Login successfully with user id {user_id} from User table")
                    self.accept()
                else:
                    pass
                    self.status.setText("Invalid Username or Password !!")


if __name__ == "__main__":
    # Calling our application :)
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    app.exec_()