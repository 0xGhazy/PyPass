import os
import sys
from pathlib import Path
from PyQt5.QtCore import *
from .css_parser import parssing_css
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import json

# Reading UI
ThemeEditor_UI = Path(__file__).parent.parent / 'ui' / 'editThemesUI.ui'
json_path = Path(__file__).parent.parent / 'ui' / "themes" / "mycss.json"
class ThemeScreenEdit(QtWidgets.QDialog):
    """ Provide a login screen to uncrease the user privacy """

    def __init__(self: "ThemeScreenEdit") -> None:
        """ initialize the application with it's UI and utility methods """
        super(ThemeScreenEdit, self).__init__()
        os.chdir(os.path.dirname(__file__))
        # loading .ui design file.
        uic.loadUi(ThemeEditor_UI, self)
        self.show()
        self.get_css_code()
        self.handleButtons()
        if os.path.isfile(json_path):
            self.fill_QLines(self.load_current_css())
        else:
            pass


    def handleButtons(self) -> None:
        self.importTheme.clicked.connect(self.import_theme)
        self.saveTheme.clicked.connect(self.save)
        self.Restore.clicked.connect(self.restore)


    def save(self) -> None:
        """ Writing the css style from QLineEdits to mycss.json file. """

        theme_css = self.get_css_code()
        # writing/overwrite css jsonfile
        json_path = Path(__file__).parent.parent / 'ui' / 'themes'
        os.chdir(json_path)
        with open("mycss.json", "w") as json_file:
            json.dump(theme_css, json_file)
        self.show_messgae("Done", "Your Theme is saved successfully <3")



    def import_theme(self) -> None:
        """_summary_
        """
        theme_file, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'All Files (*.*)')
        if len(theme_file) < 1:
            pass
        else:
            parsed = parssing_css(theme_file)
            self.fill_QLines(parsed)
        
        self.show_messgae("Done", "Your Theme is imported successfully <3")

    # restore
    def restore(self) -> None:

        default_theme = Path(__file__).parent.parent / 'ui' / 'themes' / "default.css"
        parsed_data = parssing_css(default_theme)
        self.fill_QLines(parsed_data)

        self.show_messgae("Done", "Defalut Theme is restored successfully <3")

                        ####################
                        # Utility methods #
                        ###################

    def load_current_css(self) -> dict:
        json_path = Path(__file__).parent.parent / 'ui' / "themes" / "mycss.json"
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data


    # CSS Parser
    def get_css_code(self) -> dict:
        """ Read all editLine in the application and return it in dict.

        Returns:
            css_code (dict): all the edit line fields text
        """
        css_code = {
            # [+] Main Application
            "mainQt": self.mainWindowEdit.text(),
            "tabWidget": self.tabwidgetEdit.text(),

            # [+] Accounts tabe
            "accountsList": self.editAccountList.text(),
            "editQRColor": self.editQRColor.text(),
            "editQRButton": self.editQRButton.text(),
            "editCopyButton": self.editCopyButton.text(),

            # [+] Edit Accounts tabe
            # Select/Add/Update buttons :)
            "editInputFields": self.editInputFields.text(),
            "editManubuttons": self.editManubuttons.text(),
            "editShowButton": self.editShowButton.text(),
            "editDeleteButton": self.editDeleteButton.text(),
            "editLabels": self.editLabels.text(),
            "ediGroup": self.ediGroup.text(),
            "editAccountsList_2": self.editAccountsList_2.text(),
            
            # [+] settings tabe
            "editHeaders": self.editHeaders.text(),
            "editNormalLabels": self.editNormalLabels.text(),
            "editSecFields": self.editSecFields.text(),
            "editSecButtons": self.editSecButtons.text(),
        }
        return css_code


    def fill_QLines(self, theme_file: dict) -> None:
        parsed_data = theme_file
        ## Set New CSS To QLineEDIT
        self.mainWindowEdit.setText(parsed_data["mainQt"]),
        self.tabwidgetEdit.setText(parsed_data["tabWidget"]),
            # [+] Accounts tabe
        self.editAccountList.setText(parsed_data["accountsList"]),
        self.editQRColor.setText(parsed_data["editQRColor"]),
        self.editQRButton.setText(parsed_data["editQRButton"]),
        self.editCopyButton.setText(parsed_data["editCopyButton"]),
            # [+] Edit Accounts tabe
            # Select/Add/Update buttons :)
        self.editInputFields.setText(parsed_data["editInputFields"]),
        self.editManubuttons.setText(parsed_data["editManubuttons"]),
        self.editShowButton.setText(parsed_data["editShowButton"]),
        self.editDeleteButton.setText(parsed_data["editDeleteButton"]),
        self.editLabels.setText(parsed_data["editLabels"]),
        self.ediGroup.setText(parsed_data["ediGroup"]),
        self.editAccountsList_2.setText(parsed_data["editAccountsList_2"]),
            # # [+] settings tabe
        self.editHeaders.setText(parsed_data["editHeaders"]),
        self.editNormalLabels.setText(parsed_data["editNormalLabels"]),
        self.editSecFields.setText(parsed_data["editSecFields"]),
        self.editSecButtons.setText(parsed_data["editSecButtons"])

    def show_messgae(self, title, message) -> None:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(f"""{message}""")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()
        self.accept()


if __name__ == "__main__":
    # Calling our application :)
    app = QtWidgets.QApplication(sys.argv)
    window = ThemeScreenEdit()
    app.exec_()