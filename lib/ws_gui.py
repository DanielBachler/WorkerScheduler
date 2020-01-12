## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Brendan Kristiansen
## ws_gui.py
## GUI Wrapper for Work Scheduler

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lib import CONSTANTS as K

class Main_UI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def login(self):
        server_addr, okPressed = QInputDialog.getText(self, "Enter Server Address", "Server:", QLineEdit.Normal, "")
        if okPressed and server_addr != '':
            pass
        username, okPressed = QInputDialog.getText(self, "Enter Database Username", "Username:", QLineEdit.Normal, "")
        if okPressed and server_addr != '':
            pass
        password, okPressed = QInputDialog.getText(self, "Enter Password", "Password:", QLineEdit.Normal, "")
        if okPressed and server_addr != '':
            pass
        return (server_addr, username, password)

    def initUI(self):
        # Setup main display, needs: Pane of worker names to chose (left), pane showing selected worker info (right),
        # buttons (bottom): exit, edit selected worker?,

        # Create objects
        exitButton = QPushButton("Exit", self)
        editButton = QPushButton("Edit")

        # Create spacing boxes
        # Create horizontal box
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # Add buttons to horizontal box
        hbox.addWidget(exitButton)
        hbox.addWidget(editButton)

        # Create vertical box
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        # Add panes to vbox

        # Add hbox to vbox
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Finalize box
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Worker Scheduler')
        self.show()
