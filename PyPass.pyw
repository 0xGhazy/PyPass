import os
import sys
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QMenu, QAction, QFileDialog
from cores.logsystem import LogSystem
from cores.encryption import Security
from cores.database_api import Database
from cores.QR_handler import QRHandler
from cores.password import Password
from cores.login_screen_handler import LoginScreen
from cores.css_parser import parssing_css
import pyperclip


BASE_DIR = Path(__file__).resolve().parent

main_UI = BASE_DIR / "ui" / "mainUI.ui"


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
        uic.loadUi(main_UI, self) 
        # hide tabwidget
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.tabBar().setVisible(False)
        self.app_path = Path(__file__).resolve().parent
        # Application Data
        self.database_obj   = Database()
        self.security_obj   = Security()
        self.log_obj        = LogSystem()
        self.signin_window  = LoginScreen()
        self.password_obj = Password()
        self.is_clicked = True      # if show password is clicked
        
        ## calling the sign in window/Dialog
        if self.signin_window.exec_() == QtWidgets.QDialog.Accepted:
            # Starter methods
            self.display_accounts_list()
            self.display_accounts_to_edit()
            self.handleButtons()
            self.display_menus()
            # show our application
            self.show()


    def handleButtons(self) -> None:
        """ Handling all buttons in the application """
        self.home_nav.clicked.connect(self.home_page)
        self.accounts_nav.clicked.connect(self.accounts_page)
        self.edit_nav.clicked.connect(self.edit_accounts_page)
        self.settings_nav.clicked.connect(self.setting_page)
        self.decrypt_and_copy_password.clicked.connect(self.copy_plaintext_password)
        self.select_by_id.clicked.connect(self.select_account_id)
        self.insert_account_data.clicked.connect(self.add_new_account)
        self.update_account_data.clicked.connect(self.edit_account)
        self.delete_account_data.clicked.connect(self.delete_account)
        self.show_password.clicked.connect(self.is_plain)
        self.display_qr_btn.clicked.connect(self.show_qr_image)
        self.import_key_btn.clicked.connect(self.import_key)
        self.export_key_btn.clicked.connect(self.export_key)
        

    
    def display_menus(self):
        menubar = self.menuBar()

        # [+] Creating Edit menu
        edit_menu = menubar.addMenu('&Edit')
        # [+] `Change theme` submenu
        theme_menu = QMenu('Change Theme', self)
        self.theme0 = QAction('0- Default Theme', self)
        self.theme1 = QAction('1- GitHub Dark', self)
        self.theme2 = QAction('2- GitHub Light', self)
        self.theme3 = QAction('3- Black Gold', self)
        theme_menu.addAction(self.theme0)
        theme_menu.addAction(self.theme1)
        theme_menu.addAction(self.theme2)
        theme_menu.addAction(self.theme3)
        edit_menu.addMenu(theme_menu)
        
        # [+] Handling change theme actions/invocations
        self.theme0.triggered.connect(lambda i = None : self.change_theme("default.css"))
        self.theme1.triggered.connect(lambda i = None : self.change_theme("Github-dark.css"))
        self.theme2.triggered.connect(lambda i = None : self.change_theme("Github-light.css"))
        self.theme3.triggered.connect(lambda i = None : self.change_theme("Black-Gold.css"))
    

    def change_theme(self, theme_name):
        themes_path = self.app_path / "ui" / "themes" / theme_name
        css_style = parssing_css(themes_path)
        
        # Setting new theme data.
        self.setStyleSheet(css_style["self"])
        self.tabWidget.setStyleSheet(css_style["tabWidget"])
        self.listWidget.setStyleSheet(css_style["listWidget"])
        self.display_qr_btn.setStyleSheet(css_style["display_qr_btn"])
        self.decrypt_and_copy_password.setStyleSheet(css_style["decrypt_and_copy_password"])
        self.getting_account_id.setStyleSheet(css_style["getting_account_id"])
        self.select_by_id.setStyleSheet(css_style["select_by_id"])
        self.listWidget_edit_accounts.setStyleSheet(css_style["listWidget_edit_accounts"])
        self.edit_account_platform.setStyleSheet(css_style["edit_account_platform"])
        self.edit_account_email.setStyleSheet(css_style["edit_account_email"])
        self.edit_account_password.setStyleSheet(css_style["edit_account_password"])
        self.show_password.setStyleSheet(css_style["show_password"])
        self.insert_account_data.setStyleSheet(css_style["insert_account_data"])
        self.update_account_data.setStyleSheet(css_style["update_account_data"])
        self.delete_account_data.setStyleSheet(css_style["delete_account_data"])


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

    def setting_page(self) -> None:
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.setCurrentIndex(3)
        # Display the currant key path
        key_path = self.app_path / "cores" / "security_key.key"
        self.enc_key_edit.setText(f" {str(key_path)}")

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
        return plaintext_password

    def show_qr_image(self):
        
        # [+] Generate the photo for selected account
        self.qr_handle = QRHandler()
        self.plain_password = self.copy_plaintext_password()
        self.qr_handle.generate_qr(self.plain_password, "photo.png")

        # [+] Display the image
        # Reading qr photo in Pixmap
        self.pixmap = QPixmap("photo.png")
        # Append the pixmap to QLable
        self.qr_image_obj.setPixmap(self.pixmap)
        self.qr_image_obj.setScaledContents(True)

        # [+] Remove the image from the path.
        os.remove("photo.png")
        


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

        # Check for the password strength
        if (self.password_obj.check_strength(plain_password) < 3):
            generated_password = self.password_obj.generate_password()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Password Tip!")
            msgBox.setText(f"""
            Your password seems to be weak one :(
            Let me help you with powerful random password\n\n
            Your password will be: {generated_password}
            """)
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            user_response = msgBox.exec()
            if user_response == QMessageBox.Ok:
                plain_password = generated_password
        
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


    def is_plain(self):
        if self.is_clicked:
            self.edit_account_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password.setText("Hide")
            self.is_clicked = False
        elif self.is_clicked == False:
            self.edit_account_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password.setText("Show")
            self.is_clicked = True


    def delete_account(self) -> None:
        """delete selected account from fatabase"""
        id = int(self.getting_account_id.text())
        self.database_obj.db_query(DB_NAME, f"DELETE FROM Accounts WHERE id = {id};")
        self.log_obj.write_into_log("+", f"({id}) account was deleted!")
        self.statusBar().showMessage("[+] The account has been removed successfully!")


                    ######################################
                    ## Handling Methods in setting page ##
                    ######################################

    def import_key(self):
        key_file, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'All Files (*.*)')
        if len(key_file) < 1:
            pass
        else:
             # Read the key.
            with open(key_file, "rb") as k_file:
                content = k_file.read()
            # Write The new key.
            key_path = self.app_path / "cores" / "security_key.key"
            with open(key_path, "wb") as k_file:
                k_file.write(content)
        self.log_obj.write_into_log("+", f"A new key has been imported")
        self.statusBar().showMessage("[+] Your new key is imported successfully!")

    def export_key(self):
        exported_key_path, _ = QFileDialog.getSaveFileName(self, "Save File", "security_key.key")
        key_file = self.app_path / "cores" / "security_key.key"
        # Read the key.
        with open(key_file, "rb") as k_file:
            content = k_file.read()
        # Write The new key.
        with open(exported_key_path, "wb") as k_file:
            k_file.write(content)
        self.log_obj.write_into_log("+", f"The key is exported at {exported_key_path}")
        self.statusBar().showMessage(f"[+] Your key is Exported successfully! @ {exported_key_path}")

                    ######################
                    ## Separate Methods ##
                    ######################

    def reading_database_records(self) -> list:
        """retrieve all database accounts

        Returns:
            list: list of database accounts
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
