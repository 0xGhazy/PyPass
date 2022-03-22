# PyPass Documentation

## Table os content
- Introduction
    - What is PyPass project?
    - How it works?
- Technolgies in use
    - Requirements
    - Technolgies
- How to use?
    - Adding Account
    - Update Account
    - Delete Account
    - Copying plaintext password

# [+] Introduction
In this section we will talk about an introduction to what is the PyPass project is and how it works.

## [-] What is PyPass project?
`PyPass` project is FOSS (Free Open Source Software) that cares about all your passwords  and save them encrypted in one place, Which you can easily and safely access them later.

## [-] How it works?

<div align="center">

![home](https://user-images.githubusercontent.com/60070427/159330222-42201e5d-072b-4abc-a1d5-40c8dde501a8.png)
</div>

The application comes with a simple and easy interface consisting of three sections:
Home, View Accounts, Edit Accounts. The View Accounts tab -Second tab- contains the `copy password button`,
which copies the password for the selected account from the list of accounts after decrypting the password.
Using the `decrypt` function in the `cores/encryption.py` file.
<div align="center">

![copy](https://user-images.githubusercontent.com/60070427/159330215-923004b8-363b-4466-acea-d4ea4f3d9923.png)
</div>

After clicking on `Copy Password` you will get a notification informing you that it did successfully without errors, `if you enable Priority Only feature in your windows machine it will not be displayed on screen` :)

<div align="center">

![copy notifi](https://user-images.githubusercontent.com/60070427/159330219-5d44d64c-9cb2-4341-8c7e-2ade225d1e81.png)
</div>

The edit accounts tab contains 4 buttons and 4 text inputs fields, at first in updating or deleting account,
The user have to select the account by its corresponding `id` as it appears on photo below. with out this step the user can't
perform edit (update/delete) actions on database.

<div align="center">

![delete](https://user-images.githubusercontent.com/60070427/159330212-cda8cc4f-d4bd-41c2-9e86-d5d61c54120c.png)
</div>

It also contains the `Add` button which make teh user able to add a new account to the database, in this case, the user doesn't have to select account id, it's added automatically.

PyPass project support the following platforms and websites
```python
# change this when you wanna add new platform, append it in lower case :)
SUPPORTED_PLATFORMS = ["facebook", "codeforces", "github",
                       "gmail", "hackerranck", "medium",
                       "outlook", "quora", "twitter",
                       "udacity", "udemy", "university", "wordpress"]
```
If you try to add an unsupported platform it'll have no special icon for it. will take a user icon such as the first account in the photo above.



In each event in the application (copying password, add, update, delete) a windows notification will appear after completing the invoked event/button-function.
Before any windows notification is appear there is an log evend has appended to `cores/Log.txt` file That contains 

[ Event-Status(Warning/Info/Error) User:(Whoami) --- Time:(EVENT-TIME) --- Event: (Event message explaination)] the Python code below dexplain it

```python
f"[{status}] User: {self.user_name} --- Time: {self.time_now} --- Event: {message}\n"
```

# [+] Technolgies in use
In this section, I will talk about the techniques and tools used in application development.

## [-] Requirements
```
cryptography        # for Generating en/decryption-key + encryption and decryption process
win10toast          # For windows 10 notification
PyQt5               # For GUI design
pyperclip           # for copyign to the clipboard
```

## [-] Technolgies
### - PyQt5 + QtDesigner
PyPass project uses `Qt Designer` instead of writing all designs in `PyQt5` lib, in the case of editing specific properties I use `PyQt5 syntax` in source code to perform what needs to be done.

```python
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic, QtGui

# --snip--
# --snip--
uic.loadUi(r"ui\mainUI.ui", self) 
        # hide tabwidget
        self.tabWidgets = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabWidgets.tabBar().setVisible(False)
# --snip--
```

### - SQLite3 + DB Browser (SQLite)
