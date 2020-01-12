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

        #self.initUI()

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
        size = (600, 600)
        # Setup main display, needs: Pane of worker names to chose (left), pane showing selected worker info (right),
        # menu: exit, edit selected worker?,

        # Create menu bar for options
        menubar = self.menuBar()
        # Exit submenu
        exitMenu = menubar.addMenu('Exit')

        # Actions for exit menu
        # Setup exit action
        exitAction = QAction('Exit Application', self)
        exitAction.triggered.connect(self.close)

        saveAction = QAction('Save', self)
        # Add actions to menu
        exitMenu.addAction(exitAction)
        exitMenu.addAction(saveAction)

        # Create contents of window
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        vboxL = QVBoxLayout()

        vboxC = QVBoxLayout()

        vboxR = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)

        # Panes
        # Pane left
        employees = QLineEdit()
        employees.setFixedSize(80, 80)
        employees.setAlignment(Qt.AlignRight)
        employees.setReadOnly(True)
        #employees.move(50, 50)
        employees.setText("Employees List")
        vboxL.addWidget(employees)

        # Pane Right
        employee = QLineEdit()
        employee.setFixedSize(80, 80)
        employee.setAlignment(Qt.AlignRight)
        employee.setReadOnly(True)
        employee.setText("Employee")
        vboxR.addWidget(employee)

        # Search

        # Finalize box
        hbox.addLayout(vboxL)
        hbox.addLayout(vboxC)
        hbox.addLayout(vboxR)

        centralWidget.setLayout(hbox)

        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, size[0], size[1])
        self.setWindowTitle('Worker Scheduler')
        self.show()

    def closeEvent(self, event):
        temp = QMessageBox.question(self, 'Exit Confirmation', 'Are you sure you want to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if temp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
