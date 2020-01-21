## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Brendan Kristiansen
## Worked on by Dan Bachler
## ws_gui.py
## GUI Wrapper for Work Scheduler

# TODO:
#   NewUserGUI: if not edited dont have save option, just close
#       AddProjectUI: labels for windows, cancel button
#   NewProjectGUI: Fix crash, add forms
#   Overall: Master Project list not tied to database for testing, add to main UI
#   MainUI: Add switching between view modes

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from lib import object

from lib import CONSTANTS as K


class Main_UI(QMainWindow):

    userList = []
    newUserWindow = ""
    newProjectWindow = ""

    def __init__(self, userList):
        super().__init__()
        self.userList = userList
        self.newUserWindow = NewUserGUI()
        self.newProjectWindow = NewProjectGUI()

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
        return server_addr, username, password

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

        switchViewUser = QAction("Switch to User View Mode", self)
        switchViewUser.triggered.connect(self.switch_user_view)

        # Actions for project menu
        newProjectAction = QAction('Add New Project', self)
        newProjectAction.triggered.connect(self.makeNewProject)

        switchViewProject = QAction("Switch to Project View Mode", self)
        switchViewProject.triggered.connect(self.switch_project_view)

        # Add actions to file menu
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # Add actions to user menu
        userMenu.addAction(newUserAction)
        userMenu.addAction(switchViewUser)

        # Add actions to project menu
        projectMenu.addAction(newProjectAction)
        projectMenu.addAction(switchViewProject)

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
        employees = QListWidget()
        for i in range(0, len(self.userList)):
            employees.addItem(self.userList[i].name)
        vboxL.addWidget(employees)

        # Pane Right
        employee = QTextEdit()
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
        name = item.text()
        selected_user = ""
        for user in self.userList:
            if user.name == name:
                selected_user = user
        self.centralWidget().findChild(QTextEdit).setText(selected_user.print_user())

    # makeNewUser: Creates a new user object and adds them to the database
    # ARGS: self (QMainWindow)
    # RETURNS: None, user object is added to local database instead
    def makeNewUser(self):
        # New popup window with ability to create new local user, push to database on close?
        self.newUserWindow = NewUserGUI()
        self.newUserWindow.initUI(self)
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
        self.newProjectWindow = NewProjectGUI()
        self.newProjectWindow.initUI(self)
        self.newProjectWindow.setWindowTitle(QIcon('icon.png'))

    # updateUserList: updates the QListWidget when new user is added or user is edited
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def updateUserList(self):
        templist = self.findChild(QListWidget)
        templist.clear()
        for i in range(0, len(self.userList)):
            templist.addItem(self.userList[i].name)

    # switch_user_view: changes the main UI to show users
    # ARGS: self (QMainWindow),
    # RETURNS: None
    def switch_user_view(self):
        print("Switch to user view")

    # switch_project_view: changes the main UI to show projects
    # ARGS: self (QMainWindow)
    # RETURNS:
    def switch_project_view(self):
        print("Switch to project view")


class NewUserGUI(QWidget):
    # Temp var to hold made user
    made_user = ""

    # Saved bool
    saved = False

    # Close from save bool
    close_from_save = False

    # Parent window
    parent_window = ""

    project_window = ""

    def __init__(self):
        super().__init__()

    def initUI(self, parent):
        self.parent_window = parent
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

        # Desired hours label and editor LEFT
        hbox_desired_hours = QHBoxLayout()
        desired_hours_label = QLabel("Desired Hours:")
        desired_hours_edit = QLineEdit()
        desired_hours_edit.setObjectName("user_desired_hours")
        hbox_desired_hours.addWidget(desired_hours_label)
        hbox_desired_hours.addWidget(desired_hours_edit)

        # Actual hours label and editor RIGHT
        hbox_actual_hours = QHBoxLayout()
        actual_hours_label = QLabel("Actual Hours:")
        actual_hours_edit = QLineEdit()
        actual_hours_edit.setObjectName("user_actual_hours")
        hbox_actual_hours.addWidget(actual_hours_label)
        hbox_actual_hours.addWidget(actual_hours_edit)

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
        leftColumnBox.addLayout(hbox_desired_hours)
        leftColumnBox.addLayout(hbox_id)
        leftColumnBox.addLayout(hbox_project)

        # Box for right side column
        rightColumnBox = QVBoxLayout()
        rightColumnBox.addLayout(hbox_pay)
        rightColumnBox.addLayout(hbox_team)
        rightColumnBox.addLayout(hbox_actual_hours)
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
        self.setGeometry(300, 300, 300, 500)
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
        desired_hours = self.findChild(QLineEdit, "user_desired_hours").text()
        actual_hours = self.findChild(QLineEdit, "user_actual_hours").text()
        # Place holder for projects, needs more fleshing out
        projects = []
        self.made_user = object.User(name, pay, rank, team, mentor, employee_id, projects, desired_hours, actual_hours)
        self.parent_window.userList.append(self.made_user)
        self.parent_window.updateUserList()
        self.saved = True
        self.close_from_save = True
        self.close()

    # closeEvent: changes the default closing behavior by overriding the base method
    # ARGS: self (QWidget), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: None
    def closeEvent(self, event):
        if self.close_from_save:
            event.accept()
        else:
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
        self.project_window = AddProjectsGUI()
        self.project_window.initUI()


class NewProjectGUI(QWidget):
    main_window = ""

    def __init__(self):
        super().__init__()

    def initUI(self, main_window):
        self.main_window = main_window

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('New Project Form')
        self.setWindowIcon(QIcon("icon.png"))
        self.show()


class AddProjectsGUI(QWidget):
    # Default init, inits super
    def __init__(self):
        super().__init__()

    # initUI: creates the inital UI for Add Projects window
    # ARGS: self (QWidget)
    # RETURNS: None
    def initUI(self):
        # Left Top Panel displaying existing projects
        existing_projects_label = QLabel("All Projects")
        existing_projects = QListWidget()
        existing_projects.setObjectName("existing_projects")

        # Box for panel and label
        existing_projects_box = QVBoxLayout()
        existing_projects_box.addWidget(existing_projects_label)
        existing_projects_box.addWidget(existing_projects)

        # Left Bottom panel displaying selected project info
        existing_selected_label = QLabel("Selected Projects")
        existing_selected = QTextEdit()
        existing_selected.setObjectName("existing_selected")

        # Box for panel and label
        existing_selected_box = QVBoxLayout()
        existing_selected_box.addWidget(existing_selected_label)
        existing_selected_box.addWidget(existing_selected)

        # V Box for left panels
        left_panel_box = QVBoxLayout()
        left_panel_box.addLayout(existing_projects_box)
        left_panel_box.addLayout(existing_selected_box)

        # Right panel displaying projects owned by current user
        assigned_projects_label = QLabel("Projects Assigned to User")
        assigned_projects = QListWidget()
        assigned_projects.setObjectName("assigned_projects")

        # Box for top right panel
        assigned_projects_box = QVBoxLayout()
        assigned_projects_box.addWidget(assigned_projects_label)
        assigned_projects_box.addWidget(assigned_projects)

        # Right bottom panel displaying selected project info
        assigned_selected_label = QLabel("Details of Selected Project")
        assigned_selected = QTextEdit()
        assigned_selected.setObjectName("assigned_selected")

        # Box for bottom right panel and label
        assigned_selected_box = QVBoxLayout()
        assigned_selected_box.addWidget(assigned_selected_label)
        assigned_selected_box.addWidget(assigned_selected)

        # V Box for right panels
        right_panel_box = QVBoxLayout()
        right_panel_box.addWidget(assigned_projects_box)
        right_panel_box.addWidget(assigned_selected_box)

        # H Box for panel boxes
        panel_box = QHBoxLayout()
        panel_box.addLayout(left_panel_box)
        panel_box.addLayout(right_panel_box)

        # Button for adding project to user
        add_to_user = QPushButton("Add")
        add_to_user.clicked.connect(self.addToUser)

        # Button to cancel window
        cancel_window = QPushButton("Cancel")
        # cancel_window.clicked.connect(self.close)

        # Button for removing project from user
        remove_from_user = QPushButton("Remove")
        remove_from_user.clicked.connect(self.removeFromUser)

        # H Box for buttons
        button_box = QHBoxLayout()
        button_box.addWidget(add_to_user)
        button_box.addWidget(cancel_window)
        button_box.addWidget(remove_from_user)

        # Box to hold everything
        main_box = QVBoxLayout()
        main_box.addLayout(panel_box)
        main_box.addLayout(button_box)

        # Set layout to main layout
        self.setLayout(main_box)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Add Project to User')
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    # addToUser: adds the currently selected project of existing_projects to the user
    # ARGS: self (QWidget)
    # RETURNS:
    def addToUser(self):
        print("Add to user")

    # removeFromUser: removes the selected project in assigned_projects from the user
    # ARGS: self (QWidget)
    # RETURNS:
    def removeFromUser(self):
        print("Remove from user")
