## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Brendan Kristiansen
## Worked on by Dan Bachler
## ws_gui.py
## GUI Wrapper for Work Scheduler

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from lib import CONSTANTS as K

class Main_UI(QMainWindow):

    def __init__(self):
        super().__init__()

    def login(self):
        server_addr, okPressed = QInputDialog.getText(self, "Enter Server Address", "Server:", QLineEdit.Normal, "")
        if okPressed and server_addr != '':
            pass
        username, okPressed = QInputDialog.getText(self, "Enter Database Username", "Username:", QLineEdit.Normal, "")
        if okPressed and server_addr != '':
            pass
        password, okPressed = QInputDialog.getText(self, "Enter Password", "Password:", QLineEdit.Password, "")
        if okPressed and server_addr != '':
            pass
        return (server_addr, username, password)

    def initUI(self):
        size = (600, 600)
        # Setup main display: Pane of worker names to chose (left), pane showing selected worker info (right),
        # menu: exit, add new user (new window),
        # Buttons: delete selected user (prompt), edit selected user (new window)

        ## Create menu bar for options
        menubar = self.menuBar()
        # Menu bar tabs
        fileMenu = menubar.addMenu('File')
        userMenu = menubar.addMenu('Users')

        # Actions for file menu
        exitAction = QAction('Exit Application', self)
        exitAction.triggered.connect(self.close)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.save)

        # Actions for user menu
        newUserAction = QAction('Add New User', self)
        newUserAction.triggered.connect(self.makeNewUser)

        # Add actions to file menu
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # Add actions to user menu
        userMenu.addAction(newUserAction)

        ## Contents of central widget

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
        testEmployees = ("Dan", "Jesse", "Brendan", "Ed")
        employees = QListWidget()
        for i in range(0, len(testEmployees)):
            employees.addItem(testEmployees[i])
        vboxL.addWidget(employees)

        # Pane Right
        employee = QLineEdit()
        # employee.setFixedSize(80, 80)
        employee.setFixedHeight(employees.height())
        employee.setAlignment(Qt.AlignLeft)
        employee.setReadOnly(True)
        vboxR.addWidget(employee)

        # Update box when new employee selected
        employees.itemClicked.connect(self.newSelected)

        # Search

        # New hbox for buttons under selected user pane
        employeeHBox = QHBoxLayout()
        # Buttons under right pane for selected employee
        deleteSelectedUser = QPushButton('Delete User')
        deleteSelectedUser.setToolTip('This button will permanently delete the selected employee from the database')
        deleteSelectedUser.clicked.connect(self.deletedSelectedUserFunc)
        employeeHBox.addWidget(deleteSelectedUser)

        # Edit user button
        editUserButton = QPushButton('Edit User')
        editUserButton.setToolTip('This will allow editing of the selected employee if you have permissions')
        editUserButton.clicked.connect(self.editSelectedUser)
        employeeHBox.addWidget(editUserButton)

        # Add button box to vboxR
        vboxR.addLayout(employeeHBox)

        # Finalize box
        hbox.addLayout(vboxL)
        hbox.addLayout(vboxC)
        hbox.addLayout(vboxR)

        centralWidget.setLayout(hbox)

        self.center()
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, size[0], size[1])
        self.setWindowTitle('Worker Scheduler')
        self.show()

    # closeEvent: changes the default closing behavior by overriding the base method
    # ARGS: self (QMainWindow), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: none
    def closeEvent(self, event):
        temp = QMessageBox.question(self, 'Exit Confirmation', 'Are you sure you want to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if temp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # newSelected: changes the displayed text in right side panel of QMainWindow
    # ARGS: self (QMainWindow), item (a QListWidget List item)
    # RETURNS: None
    def newSelected(self, item):
        self.centralWidget().findChild(QLineEdit).setText(item.text())

    # makeNewUser: Creates a new user object and adds them to the database
    # ARGS: self (QMainWindow)
    # RETURNS: None, user object is added to local database instead
    def makeNewUser(self):
        # New popup window with ability to create new local user, push to database on close?
        self.newUserWindow = NewUserGUI()
        self.newUserWindow.initUI()
        self.newUserWindow.setWindowIcon(QIcon('icon.png'))

    # save: saves the current state of local database to database server
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def save(self):
        pass

    # deleteSelectedUserFunc: deletes the user passed to it, called by the delete button on main GUI panel
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def deletedSelectedUserFunc(self):
        currentUser = self.centralWidget().findChild(QListWidget).currentItem().text()
        print("Deleting " + currentUser)

    # editSelectedUser:
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def editSelectedUser(self):
        currentUser = self.centralWidget().findChild(QListWidget).currentItem().text()
        print("Editing " + currentUser)

    # center: centers the window on the screen
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class NewUserGUI(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

    def initUI(self):
        # Create save button
        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveUser)

        # Create cancel button
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.close)

        # Box for buttons
        buttonBox = QHBoxLayout()

        # Add buttons to box
        buttonBox.addWidget(saveButton)
        buttonBox.addWidget(cancelButton)

        # Create inputs and text displays each in own hbox


        # Box for left side column
        leftColumnBox = QVBoxLayout()

        # Box for right side column
        rightColumnBox = QVBoxLayout()

        # Box to hold columns
        columnBox = QHBoxLayout()
        columnBox.addLayout(leftColumnBox)
        columnBox.addLayout(rightColumnBox)

        # Put boxes into main box
        mainVertBox = QVBoxLayout()
        mainVertBox.addLayout(columnBox)
        mainVertBox.addLayout(buttonBox)

        # Add to the main widget
        self.setLayout(mainVertBox)

        # Finalize self
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('New User Form')
        self.show()

    # saveUser: Saves the user currently being created, makes sure that all req fields are filled
    # ARGS: self (QWidget)
    # RETURNS: None
    def saveUser(self):
        # Save the entered user in the fields, checks?
        print("Save the created user")

    # closeEvent: changes the default closing behavior by overriding the base method
    # ARGS: self (QWidget), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: none
    def closeEvent(self, event):
        temp = QMessageBox.question(self, 'Cancel Confirmation', 'Are you sure you want to cancel?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if temp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

