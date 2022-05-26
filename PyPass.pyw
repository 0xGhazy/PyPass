import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic, QtGui
from cores.logsystem import LogSystem
from cores.encryption import Security
from cores.database_api import Database
from cores.login_screen_handler import LoginScreen
import pyperclip

# change this when you wanna add new platform, append it in lower case :)
SUPPORTED_PLATFORMS = ["facebook", "codeforces", "github",
                       "gmail", "hackerranck", "medium",
                       "outlook", "quora", "twitter",
                       "udacity", "udemy", "university", "wordpress"]

DB_NAME = "PyPassdb.sqlite3"


class PyPass(QtWidgets.QMainWindow):


    def __init__(self) -> None:
        super(PyPass, self).__init__()
        os.chdir(os.path.dirname(__file__))
        # loading .ui design file.
        uic.loadUi(r"ui\mainUI.ui", self) 
        # hide tabwidget
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.tabBar().setVisible(False)
        # Application Data
        self.database_obj   = Database()
        self.security_obj   = Security()
        self.log_obj        = LogSystem()
        self.signin_window  = LoginScreen()
        
        ## calling the sign in window/Dialog
        if self.signin_window.exec_() == QtWidgets.QDialog.Accepted:
            # Starter methods
            self.display_accounts_list()
            self.display_accounts_to_edit()
            self.handleButtons()
            # show our application
            self.show()


    def handleButtons(self) -> None:
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

    def home_page(self) -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(0)

    def accounts_page(self) -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(1)
        # refresh the list in the next click
        self.listWidget.clear()
        self.display_accounts_list()

    def edit_accounts_page(self) -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(2)
        # refresh the list in the next click
        self.listWidget_edit_accounts.clear()
        self.display_accounts_to_edit()


                    #######################################
                    ## Handling buttons in accounts page ##
                    #######################################

    def copy_plaintext_password(self) -> None:
        """Copy plain text password to clipboard after decrypting it."""
        selected_account = self.listWidget.currentItem().text().split(" :: ")
        accound_id = int(selected_account[0])
        db_data = list(self.database_obj.db_query(DB_NAME, f"SELECT * FROM Accounts WHERE id = {accound_id};"))
        plaintext_password = self.security_obj.decrypt(db_data[0][3].encode())
        pyperclip.copy(plaintext_password)
        # create log event in /cores/Logs.txt
        self.log_obj.write_into_log("+", f"({selected_account}) has been moved to the clipboard")
        self.statusBar().showMessage("[+] Copy the selected account.")

                    ###################################
                    ## Handling buttons in edit page ##
                    ###################################

    def select_account_id(self) -> None: # 11
        """return the selected account data and put them into edit line"""
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


    def add_new_account(self) -> None:
        """adding new account to database"""
        plat_name = self.edit_account_platform.text()
        account =  self.edit_account_email.text()
        plain_password = self.edit_account_password.text()
        # Encrypt password
        encrypted_password = self.security_obj.encrypt(plain_password)
        self.database_obj.db_query(DB_NAME, 
        f"INSERT INTO Accounts (ApplicationName, Account, EncryptedPassword) VALUES ('{plat_name}', '{account}', '{encrypted_password}');")
        self.statusBar().showMessage("[+] A new account has been added to database.")
        self.log_obj.write_into_log("+", f"(('{plat_name}', '{account}', '{encrypted_password}')) account was added!")


    def edit_account(self) -> None:
        """update selected account on database"""
        plat_name = self.edit_account_platform.text()
        account =  self.edit_account_email.text()
        plain_password = self.edit_account_password.text()
        encrypted_password = self.security_obj.encrypt(plain_password)
        id = int(self.getting_account_id.text())
        self.database_obj.db_query(DB_NAME, 
            f"UPDATE Accounts SET ApplicationName = '{plat_name}', Account = '{account}', EncryptedPassword = '{encrypted_password}' WHERE id = {id};")
        self.log_obj.write_into_log("+", f"(('{plat_name}', '{account}', '{encrypted_password}')) account was updated!")
        self.statusBar().showMessage("[+] The account has been updated successfully!")



    def delete_account(self) -> None:
        """delete selected account from fatabase"""
        id = int(self.getting_account_id.text())
        self.database_obj.db_query(DB_NAME, f"DELETE FROM Accounts WHERE id = {id};")
        self.log_obj.write_into_log("+", f"({id}) account was deleted!")
        self.statusBar().showMessage("[+] The account has been removed successfully!")


                    ######################
                    ## Separate Methods ##
                    ######################

    def reading_database_records(self) -> list:
        """retrieve all database accounts

        Returns:
            list: list of datbase accounts
        """
        result = self.database_obj.db_query(DB_NAME,"SELECT * FROM Accounts")
        return list(result)

    
    def display_accounts_list(self) -> None:
        """append all database accounts to QListWidget on accounts page."""
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

    
    def display_accounts_to_edit(self) -> None:
        """append all database accounts to QListWidget on edit page."""
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
    window = PyPass()
    app.exec_()
