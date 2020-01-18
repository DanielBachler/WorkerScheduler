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
from lib import object

from lib import CONSTANTS as K

class Main_UI(QMainWindow):
    userList = ()
    newUserWindow = ""
    def __init__(self, userList):
        super().__init__()
        self.userList = userList
        self.newUserWindow = NewUserGUI()

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
        projectMenu = menubar.addMenu("Projects")

        # Actions for file menu
        exitAction = QAction('Exit Application', self)
        exitAction.triggered.connect(self.close)

        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.save)

        # Actions for user menu
        newUserAction = QAction('Add New User', self)
        newUserAction.triggered.connect(self.makeNewUser)

        # Actions for project menu
        newProjectAction = QAction('Add New Project')
        newProjectAction.triggered.connect(self.makeNewProject)

        # Add actions to file menu
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # Add actions to user menu
        userMenu.addAction(newUserAction)

        # Add actions to project menu
        projectMenu.addAction(newProjectAction)

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
            if not self.newUserWindow.isEnabled():
                self.newUserWindow.close()
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

    def makeNewProject(self):
        print("Open new project window")


class NewUserGUI(QWidget):
    # Temp var to hold made user
    made_user = ""

    # Saved bool
    saved = False

    def __init__(self):
        super().__init__()

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

        # Name label and editor LEFT
        hbox_name = QHBoxLayout()
        name_label = QLabel("User Name:")
        name_edit = QLineEdit()
        name_edit.setObjectName("user_name")
        hbox_name.addWidget(name_label)
        hbox_name.addWidget(name_edit)

        # Pay label and editor RIGHT
        hbox_pay = QHBoxLayout()
        pay_label = QLabel("Pay:")
        pay_edit = QLineEdit()
        pay_edit.setObjectName("user_pay")
        hbox_pay.addWidget(pay_label)
        hbox_pay.addWidget(pay_edit)

        # Rank label and editor LEFT
        hbox_rank = QHBoxLayout()
        rank_label = QLabel("Rank:")
        rank_edit = QLineEdit()
        rank_edit.setObjectName("user_rank")
        hbox_rank.addWidget(rank_label)
        hbox_rank.addWidget(rank_edit)

        # Team label and editor RIGHT
        hbox_team = QHBoxLayout()
        team_label = QLabel("Team:")
        team_edit = QLineEdit()
        team_edit.setObjectName("user_team")
        hbox_team.addWidget(team_label)
        hbox_team.addWidget(team_edit)

        # Maybe popup window using calendar widget?
        # Desired hours label and editor LEFT

        # Actual hours label and editor RIGHT

        # Projects (drop down box?) maybe new window with qlist and clicking to add? LEFT
        hbox_project = QHBoxLayout()
        project_button = QPushButton("Projects")
        project_button.clicked.connect(self.projectMenu)
        hbox_project.addWidget(project_button)

        # Mentor label and editor RIGHT
        hbox_mentor = QHBoxLayout()
        mentor_label = QLabel("Mentor:")
        mentor_edit = QLineEdit()
        mentor_edit.setObjectName("user_mentor")
        hbox_mentor.addWidget(mentor_label)
        hbox_mentor.addWidget(mentor_edit)

        # Employee ID label and editor LEFT
        hbox_id = QHBoxLayout()
        id_label = QLabel("Employee ID:")
        id_edit = QLineEdit()
        id_edit.setObjectName("user_id")
        hbox_id.addWidget(id_label)
        hbox_id.addWidget(id_edit)

        # Box for left side column
        leftColumnBox = QVBoxLayout()
        leftColumnBox.addLayout(hbox_name)
        leftColumnBox.addLayout(hbox_rank)
        # Desired hours place holder
        leftColumnBox.addLayout(hbox_project)
        leftColumnBox.addLayout(hbox_id)

        # Box for right side column
        rightColumnBox = QVBoxLayout()
        rightColumnBox.addLayout(hbox_pay)
        rightColumnBox.addLayout(hbox_team)
        # Actual hours placeholder
        rightColumnBox.addLayout(hbox_mentor)

        # Box to hold columns
        columnBox = QHBoxLayout()
        columnBox.addLayout(leftColumnBox)
        columnBox.addLayout(rightColumnBox)

        # Put boxes into main box
        mainVertBox = QVBoxLayout()
        mainVertBox.addLayout(columnBox)
        mainVertBox.addStretch(1)
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
        name = self.findChild(QLineEdit, "user_name").text()
        pay = self.findChild(QLineEdit, "user_pay").text()
        rank = self.findChild(QLineEdit, "user_rank").text()
        team = self.findChild(QLineEdit, "user_team").text()
        mentor = self.findChild(QLineEdit, "user_mentor").text()
        employee_id = self.findChild(QLineEdit, "user_id").text()
        # Place holder for projects, needs more fleshing out
        projects = ()
        self.made_user = object.User(name, pay, rank, team, mentor, employee_id, projects)
        print(self.made_user.print_user())
        self.close()

    # closeEvent: changes the default closing behavior by overriding the base method
    # ARGS: self (QWidget), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: None
    def closeEvent(self, event):
        to_exit = False
        if self.saved:
            to_exit = QMessageBox.question(self, 'Cancel Confirmation', 'Are you sure you want to cancel?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            temp_mbox = QMessageBox()
            temp_mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.Save | QMessageBox.No)
            temp_mbox.setDefaultButton(QMessageBox.Save)
            temp_mbox.setWindowTitle('Cancel Confirmation')
            temp_mbox.setInformativeText("You haven't saved, are you sure you want to cancel?")
            to_exit = temp_mbox.exec()

        if to_exit == QMessageBox.Yes:
            event.accept()
        elif to_exit == QMessageBox.Save:
            self.saveUser()
        else:
            event.ignore()

    def projectMenu(self):
        print("Open Project Menu")

