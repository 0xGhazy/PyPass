import os
import sys
import getpass
from cores.database_api import Database
from platform import platform

def check_python_version():
    # check if python 3 is installed
    if sys.version_info[0] != 3:
        print("[-] Python 3.x is required.")
        return 0
    else:
        return 1

def install_reqs():
    # install requirements from req.txt
    if platform() == 'Windows':
        os.system("pip install -r req.txt")
        os.system("cls")
    else:
        os.system("pip3 install -r req.txt")
        os.system("clear")
    print("\n Requirements installed successfully \n")

def user_account_setup():
    # create database object
    db_obj = Database()
    # use existing username from os as Account Username
    user_name = os.getlogin()
    print("Your user name is: " + user_name)

    # allow user to create a unique Account Password
    print("Your Account Password: ", end = "")
    user_pass = getpass.getpass()
    db_obj.db_query("PyPassdb.sqlite3", f"INSERT INTO Users (User_name, User_pass) VALUES ('{user_name}', '{user_pass}');")
    print("User Account Created!")

if __name__ == '__main__':
    # change cwd to the setup.py script directory
    os.chdir(os.path.dirname(__file__))
    if check_python_version():
        try:
            install_reqs()
            user_account_setup()
        except Exception as error_message:
            print(f"[-] Error Massage:\n{error_message}\n")
    else:
        exit()
