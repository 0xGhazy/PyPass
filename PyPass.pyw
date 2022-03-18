# PyPass is an open source password manager project
# coded in Python3 by Hossam hamdy.

import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic, QtGui
from cores.logsystem import LogSystem
from cores.encryption import Security
from cores.database_api import Database
from cores.notifications import add_notification, del_notification, edit_notification, copy_notification
import pyperclip
from threading import Thread


# change this when you wanna add new platform, append it in lower case :)
SUPPORTED_PLATFORMS = ["facebook", "codeforces", "github",
                       "gmail", "hackerranck", "medium",
                       "outlook", "quora", "twitter",
                       "udacity", "udemy", "university", "wordpress"]

DB_NAME = "PyPassdb.sqlite3"


class PyPassProject(QtWidgets.QMainWindow):


    def __init__(self: "PyPassProject") -> None:
        super(PyPassProject, self).__init__()
        os.chdir(os.path.dirname(__file__))
        # loading .ui design file.
        uic.loadUi(r"ui\mainUI.ui", self) 
        # hide tabwidget
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.tabBar().setVisible(False)
        # Application Data
        self.database_obj = Database()
        self.security_obj = Security()
        self.log_obj = LogSystem()
        # Starter methods
        self.display_accounts_list()
        self.display_accounts_to_edit()
        self.handleButtons()
        self.show()


    def handleButtons(self: "PyPassProject") -> None:
        """ Handling all buttons in the application """
        self.home_nav.clicked.connect(self.home_page)
        self.accounts_nav.clicked.connect(self.accounts_page)
        self.edit_nav.clicked.connect(self.edit_accounts_page)
        self.decrypt_and_copy_password.clicked.connect(self.copy_plaintext_password)
        self.select_by_id.clicked.connect(self.select_account_id)
        self.insert_account_data.clicked.connect(self.add_new_account)
        self.update_account_data.clicked.connect(self.edit_account)
        self.delete_account_data.clicked.connect(self.delete_account)
        

                    ############################
                    ## Handling right buttons ##
                    ############################

    def home_page(self: "PyPassProject") -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(0)


    def accounts_page(self: "PyPassProject") -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(1)
        # refresh the list in the next click
        self.listWidget.clear()
        self.display_accounts_list()


    def edit_accounts_page(self: "PyPassProject") -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(2)
        # refresh the list in the next click
        self.listWidget_edit_accounts.clear()
        self.display_accounts_to_edit()


                    #######################################
                    ## Handling buttons in accounts page ##
                    #######################################

    def copy_plaintext_password(self: "PyPassProject") -> None:
        """Copy plain text password to clipboard after decrypting it.

        Args:
            self (PyPassProject): PyPassProject instance
        """
        selected_account = self.listWidget.currentItem().text().split(" :: ")
        accound_id = int(selected_account[0])
        db_data = list(self.database_obj.db_query(DB_NAME, f"SELECT * FROM Accounts WHERE id = {accound_id};"))
        plaintext_password = self.security_obj.decrypt(db_data[0][3].encode())
        pyperclip.copy(plaintext_password)
        t1 = Thread(target=copy_notification)
        t1.start()
        # create log event in /cores/Logs.txt
        self.log_obj.write_into_log("+", f"({selected_account}) has been moved to the clipboard")


                    ###################################
                    ## Handling buttons in edit page ##
                    ###################################

    def select_account_id(self: "PyPassProject") -> None:
        """return the selected account data and put them into edit line

        Args:
            self (PyPassProject): PyPassProject instance
        """
        account_id = self.getting_account_id.text()
        try:
            response = list(self.database_obj.db_query(DB_NAME,
                                   f"SELECT * FROM Accounts WHERE id={account_id}"))
            # display result on line edit
            self.edit_account_platform.setText(response[0][1])
            self.edit_account_email.setText(response[0][2])
            self.edit_account_password.setText(self.security_obj.decrypt(response[0][3].encode()))
            # create log event with the selected account information with out password !!
            self.log_obj.write_into_log("+", f"({response[0][0:-1]}) Was selected!")
        except Exception as error_message:
            print(error_message)


    def add_new_account(self: "PyPassProject") -> None:
        """adding new account to database

        Args:
            self (PyPassProject): PyPassProject instance
        """
        plat_name = self.edit_account_platform.text()
        account =  self.edit_account_email.text()
        plain_password = self.edit_account_password.text()
        # Encrypt password
        encrypted_password = self.security_obj.encrypt(plain_password)
        self.database_obj.db_query(DB_NAME, 
        f"INSERT INTO Accounts (ApplicationName, Account, EncryptedPassword) VALUES ('{plat_name}', '{account}', '{encrypted_password}');")
        t1 = Thread(target=add_notification)
        t1.start()
        self.log_obj.write_into_log("+", f"(('{plat_name}', '{account}', '{encrypted_password}')) account was added!")
        t1 = Thread(target=add_notification)
        t1.start()


    def edit_account(self: "PyPassProject") -> None:
        """update selected account on database

        Args:
            self (PyPassProject): PyPassProject instance
        """
        plat_name = self.edit_account_platform.text()
        account =  self.edit_account_email.text()
        plain_password = self.edit_account_password.text()
        encrypted_password = self.security_obj.encrypt(plain_password)
        id = int(self.getting_account_id.text())
        self.database_obj.db_query(DB_NAME, 
            f"UPDATE Accounts SET ApplicationName = '{plat_name}', Account = '{account}', EncryptedPassword = '{encrypted_password}' WHERE id = {id};")
        self.log_obj.write_into_log("+", f"(('{plat_name}', '{account}', '{encrypted_password}')) account was updated!")
        t1 = Thread(target=edit_notification)
        t1.start()



    def delete_account(self: "PyPassProject") -> None:
        """delete selected account from fatabase

        Args:
            self (PyPassProject): PyPassProject instance
        """
        id = int(self.getting_account_id.text())
        self.database_obj.db_query(DB_NAME, f"DELETE FROM Accounts WHERE id = {id};")
        self.log_obj.write_into_log("+", f"({id}) account was deleted!")
        t1 = Thread(target=del_notification)
        t1.start()


                    ######################
                    ## Separate Methods ##
                    ######################

    def reading_database_records(self: "PyPassProject") -> list:
        """retrieve all database accounts

        Args:
            self (PyPassProject): PyPassProject instance

        Returns:
            list: list of datbase accounts
        """
        result = self.database_obj.db_query(DB_NAME,"SELECT * FROM Accounts")
        return list(result)

    
    def display_accounts_list(self: "PyPassProject") -> None:
        """append all database accounts to QListWidget on accounts page.

        Args:
            self (PyPassProject): PyPassProject instance
        """
        icons_path = os.path.join(os.path.dirname(__file__), "ui", "icons", "socialIcons")
        data = self.reading_database_records()
        record_index = 0
        for row in data:
            icon = QtGui.QIcon(os.path.join(icons_path, f"{row[1].lower()}.png"))
            if f"{row[1].lower()}" in SUPPORTED_PLATFORMS:
                item = QtWidgets.QListWidgetItem(icon, f"{row[0]} :: {row[2]}")
                self.listWidget.addItem(item)
            else:
                icon = QtGui.QIcon(os.path.join(icons_path, f"user.png"))
                item = QtWidgets.QListWidgetItem(icon, f"{row[0]} :: {row[1]} :: {row[2]}")
                self.listWidget.addItem(item)
            record_index += 1

    
    def display_accounts_to_edit(self: "PyPassProject") -> None:
        """append all database accounts to QListWidget on edit page.

        Args:
            self (PyPassProject): PyPassProject instance
        """
        icons_path = os.path.join(os.path.dirname(__file__), "ui", "icons", "socialIcons")
        data = self.reading_database_records()
        record_index = 0
        for row in data:
            icon = QtGui.QIcon(os.path.join(icons_path, f"{row[1].lower()}.png"))
            if f"{row[1].lower()}" in SUPPORTED_PLATFORMS:
                item = QtWidgets.QListWidgetItem(icon, f"{row[0]} :: {row[2]}")
                self.listWidget_edit_accounts.addItem(item)
            else:
                icon = QtGui.QIcon(os.path.join(icons_path, f"user.png"))
                item = QtWidgets.QListWidgetItem(icon, f"{row[0]} ::{row[1]} :: {row[2]}")
                self.listWidget_edit_accounts.addItem(item)
            record_index += 1



if __name__ == "__main__":
    # calling our application :)
    app = QtWidgets.QApplication(sys.argv)
    window = PyPassProject()
    app.exec_()
