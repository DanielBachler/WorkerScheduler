# The Work Scheduler
# Montana State University senior design project
#
# Copyright 2019
#
# Created: 2019-10-19 by Brendan Kristiansen
# Written by Dan Bachler
# ws_gui.py
# GUI Wrapper for Work Scheduler

# TODO:
#   NewUserGUI:
#   NewProjectGUI:
#   EditUserUI:
#   EditProjectUI: add functionality to info form
#   MainUI: Fix closing behavior for other type prompts
#   Projects:
#   Users:
#   Overall: Tie in database

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from lib import object
import copy

from lib import CONSTANTS as K


# findItem: Finds the given item in the given list
# ARGS: objectName (T), objectList (List[T])
# RETURNS:  object_current (T)
def findItem(objectName, objectList):
    for object_current in objectList:
        if objectName == object_current.name:
            return object_current


class Main_UI(QMainWindow):
    # Class global vars for users and projects
    userList = []
    projectList = []
    # Class global vars for sub windows
    newUserWindow = ""
    newProjectWindow = ""
    # List of available ranks pulled from database
    rank_list = []

    # If current user is admin, debug set to TRUE
    admin = True

    # View variable, F = users, T = projects
    view = False

    # __init__: Initializes the main UI
    # ARGS: self (QMainWindow)
    # RETURNS: QMainWindow
    def __init__(self):
        super().__init__()
        self.newUserWindow = NewUserGUI()
        self.newProjectWindow = NewProjectGUI()

    # login: Takes the login information and connects the database as a user
    # ARGS: self (QMainWindow)
    # RETURNS: server_addr (String), username (String), password (String)
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

    # initUI: Creates the UI for the main UI
    # ARGS: self (QMainWindow), userList (List[User]), projectList (List[Project])
    # RETURNS: None
    def initUI(self, userList, projectList, rank_list):
        # Init global vars
        self.userList = userList
        self.projectList = projectList
        self.rank_list = rank_list

        size = (600, 600)
        # Setup main display: Pane of worker names to chose (left), pane showing selected worker info (right),
        # menu: exit, add new user (new window),
        # Buttons: delete selected user (prompt), edit selected user (new window)

        # Create menu bar for options
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

        # Admin menu, only create if user is admin rank
        if self.admin:
            # Menu bar item
            adminMenu = menubar.addMenu("Admin")
            # Actions
            add_rank = QAction("Add new rank", self)
            add_rank.triggered.connect(self.addRank)
            # Add actions
            adminMenu.addAction(add_rank)

        # Contents of central widget

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
        left_view = QListWidget()
        left_view.setObjectName("left_view")
        vboxL.addWidget(left_view)

        # Pane Right
        right_view = QTextEdit()
        right_view.setObjectName("right_view")
        right_view.setFixedHeight(left_view.height())
        right_view.setAlignment(Qt.AlignLeft)
        right_view.setReadOnly(True)
        vboxR.addWidget(right_view)

        # Update box when new employee selected
        left_view.itemClicked.connect(self.newSelected)

        # Search

        # New hbox for buttons under selected user pane
        employeeHBox = QHBoxLayout()
        # Buttons under right pane for selected employee
        deleteSelectedUser = QPushButton('Delete')
        deleteSelectedUser.setToolTip('This button will permanently delete the selected item from the database')
        deleteSelectedUser.clicked.connect(self.deletedSelectedFunc)
        employeeHBox.addWidget(deleteSelectedUser)

        # Edit user button
        editButton = QPushButton('Edit Item')
        editButton.setToolTip('This will allow editing of the selected employee if you have permissions')
        editButton.clicked.connect(self.editSelected)
        employeeHBox.addWidget(editButton)

        # Add button box to vboxR
        vboxR.addLayout(employeeHBox)

        # Finalize box
        hbox.addLayout(vboxL)
        hbox.addLayout(vboxC)
        hbox.addLayout(vboxR)

        centralWidget.setLayout(hbox)

        self.change_view()
        self.center()
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, size[0], size[1])
        self.setWindowTitle('Worker Scheduler')
        self.show()

    # closeEvent: Changes the default closing behavior by overriding the base method
    # ARGS: self (QMainWindow), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: none
    def closeEvent(self, event):
        temp = QMessageBox.question(self, 'Exit Confirmation', 'Are you sure you want to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if temp == QMessageBox.Yes:
            self.newUserWindow.parent_closing = True
            self.newProjectWindow.parent_closing = True
            event.accept()
        else:
            event.ignore()

    # newSelected: Changes the displayed text in right side panel of QMainWindow
    # ARGS: self (QMainWindow), item (a QListWidget List item)
    # RETURNS: None
    def newSelected(self, item):
        # Get right_view object
        right_view = self.centralWidget().findChild(QTextEdit, "right_view")
        name = item.text()
        selected_object = ""
        if self.view:
            for project in self.projectList:
                if project.name == name:
                    selected_object = project
            right_view.setText(selected_object.print_project())
        else:
            for user in self.userList:
                if user.name == name:
                    selected_object = user
            right_view.setText(selected_object.print_user())

    # makeNewUser: Creates a new user object and adds them to the database
    # ARGS: self (QMainWindow)
    # RETURNS: None, user object is added to local database instead
    def makeNewUser(self):
        # New popup window with ability to create new local user, push to database on close?
        self.newUserWindow = NewUserGUI()
        self.newUserWindow.initUI(self)
        self.newUserWindow.setWindowIcon(QIcon('icon.png'))

    # save: Saves the current state of local database to database server
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def save(self):
        pass

    # deleteSelectedUserFunc: Deletes the user passed to it, called by the delete button on main GUI panel
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def deletedSelectedFunc(self):
        try:
            current_object = self.centralWidget().findChild(QListWidget).currentItem().text()
            if self.view:
                # Project
                project = findItem(current_object, self.projectList)
                self.projectList.remove(project)
            else:
                # User
                user = findItem(current_object, self.userList)
                self.userList.remove(user)
            self.updateUserList()
        except:
            QMessageBox.question(self, 'Error', 'Selected item is already deleted',
                                    QMessageBox.Close, QMessageBox.Close)

    # editSelected: Edits the currently highlighted item
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def editSelected(self):
        # Get the item as its object type
        currentItem = self.centralWidget().findChild(QListWidget).currentItem().text()
        current_object = findItem(currentItem, self.projectList if self.view else self.userList)

        if self.view:
            # Project
            try:
                self.newProjectWindow = NewProjectGUI()
                self.newProjectWindow.editing = True
                self.newProjectWindow.initUI(self)
                self.newProjectWindow.edit(current_object)
                self.newProjectWindow.setWindowIcon(QIcon("icon.png"))
            except Exception as e:
                print(e)
        else:
            # User
            try:
                self.newUserWindow = NewUserGUI()
                self.newUserWindow.editing = True
                self.newUserWindow.initUI(self)
                self.newUserWindow.editUser(current_object)
                self.newUserWindow.setWindowIcon(QIcon("icon.png"))
            except Exception as e:
                print(e)

    # center: Centers the window on the screen
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # makeNewProject: Opens new project creation UI
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def makeNewProject(self):
        try:
            self.newProjectWindow = NewProjectGUI()
            self.newProjectWindow.initUI(self)
            self.newProjectWindow.setWindowIcon(QIcon("icon.png"))
        except Exception as e:
            print(e)

    # updateUserList: Updates the QListWidget when a new item is added or item is edited
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def updateUserList(self):
        # Get right_view object
        left_view = self.findChild(QListWidget)
        left_view.clear()

        # Add item based on which view is selected
        if self.view:
            for project in self.projectList:
                left_view.addItem(project.name)
        else:
            for user in self.userList:
                left_view.addItem(user.name)

    # switch_user_view: Changes the main UI to show users
    # ARGS: self (QMainWindow),
    # RETURNS: None
    def switch_user_view(self):
        self.view = False
        self.change_view()

    # switch_project_view: Changes the main UI to show projects
    # ARGS: self (QMainWindow)
    # RETURNS:
    def switch_project_view(self):
        self.view = True
        self.change_view()

    # change_view: Changes the currently displayed items in Main UI based on view var
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def change_view(self):
        # Get the left_view object
        left_view = self.centralWidget().findChild(QListWidget, "left_view")
        if self.view:
            left_view.clear()
            for project in self.projectList:
                left_view.addItem(project.name)
        else:
            left_view.clear()
            for user in self.userList:
                left_view.addItem(user.name)

    # addRank: adds a new rank to the rank list
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def addRank(self):
        rank, okPressed = QInputDialog.getText(self, "Enter New Rank", "Rank:", QLineEdit.Normal, "")
        if okPressed and rank != "":
            self.rank_list.append(rank)


class NewUserGUI(QWidget):
    # Temp var to hold made user
    made_user = ""

    # Saved bool
    saved = False

    # Close from save bool
    close_from_save = False

    # Parent window
    parent_window = ""

    # Var for whether box has been edited
    box_edited = False

    # If Editing vars
    editing = False
    editing_user = object.User

    # Closing behavior vars
    parent_closing = False

    # __init__: Initializes the NewUserGUI window
    # ARGS: self (QWidget)
    # RETURNS: QWidget
    def __init__(self):
        super().__init__()

    # initUI: Creates the UI for the NewUserGUI
    # ARGS: self (QWidget), parent (QMainWindow)
    # RETURNS: None
    def initUI(self, parent):
        self.parent_window = parent
        # Create save button
        saveButton = QPushButton
        if not self.editing:
            saveButton = QPushButton('Save')
            saveButton.clicked.connect(self.saveUser)
        else:
            saveButton = QPushButton('Update')
            saveButton.clicked.connect(self.updateUser)

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
        name_edit.textChanged.connect(self.boxEdited)
        name_edit.setObjectName("user_name")
        hbox_name.addWidget(name_label)
        hbox_name.addWidget(name_edit)

        # Pay label and editor RIGHT
        hbox_pay = QHBoxLayout()
        pay_label = QLabel("Pay:")
        pay_edit = QLineEdit()
        pay_edit.textEdited.connect(self.boxEdited)
        pay_edit.setObjectName("user_pay")
        hbox_pay.addWidget(pay_label)
        hbox_pay.addWidget(pay_edit)

        # Rank Combo box: LEFT
        hbox_rank = QHBoxLayout()
        try:
            rank_label = QLabel("Rank:")
            rank_edit = QComboBox()
            rank_edit.setObjectName("user_rank")
            # Set changed command
            rank_edit.activated.connect(self.boxEdited)
            hbox_rank.addWidget(rank_label)
            hbox_rank.addWidget(rank_edit)
        except Exception as e:
            print(e)

        # Team label and editor RIGHT
        hbox_team = QHBoxLayout()
        team_label = QLabel("Team:")
        team_edit = QLineEdit()
        team_edit.textEdited.connect(self.boxEdited)
        team_edit.setObjectName("user_team")
        hbox_team.addWidget(team_label)
        hbox_team.addWidget(team_edit)

        # Mentor label and editor RIGHT
        hbox_mentor = QHBoxLayout()
        mentor_label = QLabel("Mentor:")
        mentor_edit = QLineEdit()
        mentor_edit.textEdited.connect(self.boxEdited)
        mentor_edit.setObjectName("user_mentor")
        hbox_mentor.addWidget(mentor_label)
        hbox_mentor.addWidget(mentor_edit)

        # Employee ID label and editor LEFT
        hbox_id = QHBoxLayout()
        id_label = QLabel("Employee ID:")
        id_edit = QLineEdit()
        id_edit.textEdited.connect(self.boxEdited)
        id_edit.setObjectName("user_id")
        hbox_id.addWidget(id_label)
        hbox_id.addWidget(id_edit)

        # Box for left side column
        leftColumnBox = QVBoxLayout()
        leftColumnBox.addLayout(hbox_name)
        leftColumnBox.addLayout(hbox_rank)
        leftColumnBox.addLayout(hbox_id)

        # Box for right side column
        rightColumnBox = QVBoxLayout()
        rightColumnBox.addLayout(hbox_pay)
        rightColumnBox.addLayout(hbox_team)
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

        # Populate combo box
        self.updateRankBox()

        # Finalize self
        self.setGeometry(300, 300, 300, 500)
        if self.editing:
            self.setWindowTitle('Edit User Form')
        else:
            self.setWindowTitle('New User Form')
        self.show()

    # saveUser: Saves the user currently being created, makes sure that all req fields are filled
    # ARGS: self (QWidget)
    # RETURNS: None
    def saveUser(self):
        if self.box_edited:
            try:
                # Get user
                self.made_user = self.makeUser()
                self.parent_window.userList.append(self.made_user)
                self.parent_window.updateUserList()
                self.saved = True
                self.close_from_save = True
            except Exception as e:
                print(e, "Error in saveUser")

        self.close()

    # closeEvent: Changes the default closing behavior by overriding the base method
    # ARGS: self (QWidget), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: None
    def closeEvent(self, event):
        # Override closing from parent
        if self.parent_closing:
            event.accept()
        if self.close_from_save or not self.box_edited:
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

    # boxEdited: Changes the state of box_edited when any text is edited
    # ARGS: self (QWidget)
    # RETURNS: None
    def boxEdited(self):
        self.box_edited = True

    # updateRankBox: updates the rank combo box if new item is added
    # ARGS: None
    # RETURNS: None
    def updateRankBox(self):
        # Get combo box object
        rank_edit = self.findChild(QComboBox, "user_rank")
        # Clear existing entries
        rank_edit.clear()
        # Repopulate
        rank_edit.addItem("")
        for rank in self.parent_window.rank_list:
            rank_edit.addItem(rank)

    # editUser: Sets up the UI to edit a user
    # ARGS: self (QWidget), user (object.User)
    # RETURNS: None
    def editUser(self, user=object.User):
        self.editing_user = user
        name = self.findChild(QLineEdit, "user_name")
        pay = self.findChild(QLineEdit, "user_pay")
        rank = self.findChild(QComboBox, "user_rank")
        team = self.findChild(QLineEdit, "user_team")
        mentor = self.findChild(QLineEdit, "user_mentor")
        employee_id = self.findChild(QLineEdit, "user_id")
        name.setText(user.name)
        pay.setText(user.pay)
        rank.setCurrentIndex(rank.findText(user.rank))
        team.setText(user.team)
        mentor.setText(user.mentor)
        employee_id.setText(user.employee_id)
        self.box_edited = False

    # updateUser: Updates a given users entry
    # ARGS: self (QWidget)
    # RETURNS: None
    def updateUser(self):
        # Get user object
        self.parent_window.userList.remove(self.editing_user)
        # Place holder for projects, needs more fleshing out
        self.made_user = self.makeUser()
        self.parent_window.userList.append(self.made_user)
        self.parent_window.updateUserList()
        self.saved = True
        self.close_from_save = True
        self.parent_window.newSelected(QListWidgetItem(self.made_user.name))
        self.close()

    # findUser: Finds a given user by userID
    # ARGS: self (QWidget), user_id (String)
    # RETURNS: user (object.User) || None
    def findUser(self, user_id):
        for user in self.parent_window.userList:
            if user.employee_id == user_id:
                return user
        return None

    # makeUser: Makes a user with the filled in forms
    # ARGS: self (QWidget)
    # RETURNS: object.User
    def makeUser(self):
        name = self.findChild(QLineEdit, "user_name").text()
        pay = self.findChild(QLineEdit, "user_pay").text()
        rank = self.findChild(QComboBox, "user_rank").currentText()
        team = self.findChild(QLineEdit, "user_team").text()
        mentor = self.findChild(QLineEdit, "user_mentor").text()
        employee_id = self.findChild(QLineEdit, "user_id").text()
        return object.User(name, pay, rank, team, mentor, employee_id)


class AddUserInfoGUI(QWidget):
    # Check for edits variable.
    boxEditedVariable = False

    # Parent AddUsersGUI window
    parent_window = ""

    # Selected project to add user info to
    selected_project = object.Project

    # Selected user to add to project with info
    user = object.User

    # __init__: Creates an instance of AddUserInfoGUI
    # ARGS: self (QWidget), project (object.Project), user (object.User), parent_window (QWidget)
    # RETURNS: self (QWidget)
    def __init__(self, project, user, parent_window):
        super().__init__()
        self.selected_project = project
        self.user = user
        self.parent_window = parent_window

    # initUI: Initializes the UI
    # ARGS: self (QWidget)
    # RETURNS: None
    # TODO: Interface Projected Hours, Desired Hours and Actual Hours to user project info. Need User->Project->Project
    #  Hours, Desired Hours and Actual Hours in data base.
    def initUI(self):

        # GUI Code.

        # items
        # Projected hours
        projectedHours_Box = QHBoxLayout()
        projectedHours_Label = QLabel("Projected Hours")
        projectedHours_Input = QLineEdit()
        projectedHours_Input.textEdited.connect(self.boxEdited)
        projectedHours_Input.setObjectName("projectedHours_Input")
        projectedHours_Box.addWidget(projectedHours_Label)
        projectedHours_Box.addWidget(projectedHours_Input)

        # Desired hours
        desiredHours_Box = QHBoxLayout()
        desiredHours_Label = QLabel("Desired Hours")
        desiredHours_Input = QLineEdit()
        desiredHours_Input.textEdited.connect(self.boxEdited)
        desiredHours_Input.setObjectName("desiredHours_Input")
        desiredHours_Box.addWidget(desiredHours_Label)
        desiredHours_Box.addWidget(desiredHours_Input)

        # Actual hours
        actualHours_Box = QHBoxLayout()
        actualHours_Label = QLabel("Actual Hours")
        actualHours_Input = QLineEdit()
        actualHours_Input.textEdited.connect(self.boxEdited)
        actualHours_Input.setObjectName("actualHours_Input")
        actualHours_Box.addWidget(actualHours_Label)
        actualHours_Box.addWidget(actualHours_Input)

        # buttons
        saveButton_Box = QHBoxLayout()
        saveButton = QPushButton("Save")
        saveButton_Box.addWidget(saveButton)
        #add function connection here.

        cancelButton_Box = QHBoxLayout()
        cancelButton = QPushButton("Cancel")
        cancelButton_Box.addWidget(cancelButton)
        # add function connection here

        # combobox
        billingCode_Box = QHBoxLayout()
        billingCode_Label = QLabel("Billing Code")
        billingCode_Combobox = QComboBox()
        if (not isinstance(self.selected_project.billing_codes, str)):
            for i in range(len(self.selected_project.billing_codes)):
                billingCode_Combobox.addItem(self.selected_project.billing_codes[i])
        else:
            billingCode_Combobox.addItem(self.selected_project.billing_codes)

        billingCode_Box.addWidget(billingCode_Label)
        billingCode_Box.addWidget(billingCode_Combobox)

        # boxing
        windowBox = QVBoxLayout()

        largeColTop = QVBoxLayout()
        largeColTop.addLayout(projectedHours_Box)
        largeColTop.addLayout(desiredHours_Box)
        largeColTop.addLayout(actualHours_Box)
        largeColTop.addLayout(billingCode_Box)
        largeHorBottom = QVBoxLayout()
        largeHorBottom.addLayout(saveButton_Box)
        largeHorBottom.addLayout(cancelButton_Box)

        windowBox.addLayout(largeColTop)
        windowBox.addLayout(largeHorBottom)
        # Final setup and display.
        self.setLayout(windowBox)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Add User Information")
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    def boxEdited(self):
        self.boxEditedVariable = True


class AddUsersGUI(QWidget):
    # The project to add users to
    selected_project = object.Project

    # The parent window
    parent_window = QWidget

    # Selected user from all users
    selected_all_user = object.User

    # Selected user from project
    selected_project_user = object.User

    # List of users assigned to the project
    project_user_list = []

    # Sub window for user details
    user_info = AddUserInfoGUI

    # __init__: Creates an instance of AddUsersGUI
    # ARGS: self (QWidget), project (object.Project), parent_window (QWidget)
    # RETURNS: self (QWidget)
    def __init__(self, project, parent_window):
        super().__init__()
        self.selected_project = project
        self.parent_window = parent_window
        self.project_user_list = copy.deepcopy(project.users)

    # initUI: Initializes the UI
    # ARGS: self (QWidget)
    # RETURNS: None
    def initUI(self):
        # Needs 2 panels, one for all users one for users in project

        # Cancel button
        close_button_box = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button_box.addWidget(close_button)

        # User buttons
        user_button_box = QHBoxLayout()

        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(self.addUserToProject)
        user_button_box.addWidget(add_user_button)

        remove_user_button = QPushButton("Remove User")
        remove_user_button.clicked.connect(self.removeUserFromProject)
        user_button_box.addWidget(remove_user_button)

        # Labels
        label_box = QHBoxLayout()

        all_label = QLabel("Global User List")
        project_label = QLabel("Project Specific User List")

        label_box.addWidget(all_label)
        label_box.addWidget(project_label)

        # Panes
        all_users = QListWidget()
        all_users.itemClicked.connect(self.updateAllUser)
        all_users.setObjectName("all_users")

        project_users = QListWidget()
        project_users.itemClicked.connect(self.updateProjectUser)
        project_users.setObjectName("project_users")

        # Layouts

        # Pane layout
        pane_layout = QHBoxLayout()

        pane_layout.addWidget(all_users)
        pane_layout.addWidget(project_users)

        # Main Layout
        main_layout = QVBoxLayout()

        main_layout.addLayout(label_box)
        main_layout.addLayout(pane_layout)
        main_layout.addLayout(user_button_box)
        main_layout.addLayout(close_button_box)

        # Finalizing
        self.setLayout(main_layout)

        self.updateAllUsersList()
        self.updateProjectUsersList()

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle("Add Users To %s" % self.selected_project.name)
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    # addUserToProject: Adds the selected user in the main list to the internal list (not actual project)
    # ARGS: self (QWidget)
    # RETURNS: None
    def addUserToProject(self):
        self.project_user_list.append(self.selected_all_user)
        self.updateProjectUsersList()
        self.user_info = AddUserInfoGUI(self.selected_project, self.selected_all_user, self)
        self.user_info.initUI()

    # removeUserFromProject: Removes the selected user in project list from the project, are you sure prompt?
    # ARGS: self (QWidget)
    # RETURNS: None
    def removeUserFromProject(self):
        try:
            self.project_user_list.remove(self.selected_project_user)
            self.updateProjectUsersList()
        except:
            QMessageBox.question(self, 'Error', 'Selected item is already deleted',
                                 QMessageBox.Close, QMessageBox.Close)

    # updateAllUser: Updates the current selected_all_user
    # ARGS: self (QWidget), item (QListWidgetItem)
    # RETURNS: None
    def updateAllUser(self, item):
        self.selected_all_user = findItem(item.text(), self.parent_window.parent_window.userList)

    # updateProjectUser: Updates the current selected_project_user
    # ARGS: self (QWidget), item (QListWidgetItem)
    # RETURNS: None
    def updateProjectUser(self, item):
        self.selected_project_user = findItem(item.text(), self.project_user_list)

    # updateAllUsersList: Updates the QListWidget with the current version of userList
    # ARGS: self (QWidget)
    # RETURNS: None
    def updateAllUsersList(self):
        all_users = self.findChild(QListWidget, "all_users")
        all_users.clear()
        for user in self.parent_window.parent_window.userList:
            all_users.addItem(user.name)

    # updateProjectUsersList: Updates the QListWidget with the current version of userList
    # ARGS: self (QWidget)
    # RETURNS: None
    def updateProjectUsersList(self):
        project_users = self.findChild(QListWidget, "project_users")
        project_users.clear()
        for user in self.project_user_list:
            project_users.addItem(user.name)

    # closeEvent: Saves created user list to parent window before closing
    # ARGS: self (QWidget), event (QEvent (closing event))
    # RETURNS: None
    def closeEvent(self, event):
        self.parent_window.project_user_list = self.project_user_list
        event.accept()


class NewProjectGUI(QWidget):
    # Parent window
    parent_window = ""

    # Child add user window
    add_user_window = AddUsersGUI

    # If boxes have been edited
    edited = False

    # If form has been saved
    saved = False
    close_from_save = False

    # Editing vars
    editing = False
    editing_project = object.Project
    project_user_list = []

    # Closing behavior var from main parent
    parent_closing = False

    # __init__: Initializes the NewProjectGUI
    # ARGS: self (QWidget)
    # RETURNS: QWidget
    def __init__(self):
        super().__init__()

    # initUI: Creates the UI for the NewProjectGUI
    # ARGS: self (QWidget), parent_window (QMainWindow)
    # RETURNS: None
    def initUI(self, parent_window):
        # Set parent window
        self.parent_window = parent_window

        # BUTTONS

        # Save button
        save_button = QPushButton
        if not self.editing:
            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save)
        else:
            save_button = QPushButton("Update")
            save_button.clicked.connect(self.updateProject)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        # Button box
        button_box = QHBoxLayout()
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)

        # FORMS

        # Billing Codes: LEFT
        billing_label = QLabel("Billing code(s)\nseparated by\ncomma:")
        billing_input = QLineEdit()
        billing_input.setObjectName("billing_input")
        billing_input.textEdited.connect(self.isEdited)
        billing_box = QHBoxLayout()
        billing_box.addWidget(billing_label)
        billing_box.addWidget(billing_input)

        # Expected Hours: RIGHT
        expected_hours_label = QLabel("Expected Project Hours:")
        expected_hours_input = QLineEdit()
        expected_hours_input.setObjectName("expected_hours_input")
        expected_hours_input.textEdited.connect(self.isEdited)
        expected_hours_box = QHBoxLayout()
        expected_hours_box.addWidget(expected_hours_label)
        expected_hours_box.addWidget(expected_hours_input)

        # Title: LEFT
        title_label = QLabel("Title:")
        title_input = QLineEdit()
        title_input.setObjectName("title_input")
        title_input.textEdited.connect(self.isEdited)
        title_box = QHBoxLayout()
        title_box.addWidget(title_label)
        title_box.addWidget(title_input)

        # Description RIGHT
        description_label = QLabel("Description:")
        description_input = QTextEdit()
        description_input.setMaximumHeight(int(self.height() / 4))
        description_input.setObjectName("description_input")
        description_input.textChanged.connect(self.isEdited)
        description_box = QHBoxLayout()
        description_box.addWidget(description_label)
        description_box.addWidget(description_input)

        # Add users button LEFT (only when editing)
        add_users_box = QHBoxLayout()
        if self.editing:
            add_users_button = QPushButton("Add Users")
            add_users_button.clicked.connect(self.addUsers)
            add_users_box.addWidget(add_users_button)

        # Boxes for left and right side
        left_V_box = QVBoxLayout()
        right_V_box = QVBoxLayout()

        # Put into left and right boxes
        left_V_box.addLayout(billing_box)
        right_V_box.addLayout(expected_hours_box)
        left_V_box.addLayout(title_box)
        right_V_box.addLayout(description_box)
        left_V_box.addLayout(add_users_box)

        # Put into main box
        main_box = QHBoxLayout()
        main_box.addLayout(left_V_box)
        main_box.addLayout(right_V_box)

        # Main V Box
        final_box = QVBoxLayout()
        final_box.addLayout(main_box)
        final_box.stretch(1)
        final_box.addLayout(button_box)

        # Set Layout
        self.setLayout(final_box)

        # init geometry and show
        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('New Project Form')
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    # isEdited: Changes state of self.edited if any forms are modified
    # ARGS: self (QWidget)
    # RETURNS: None
    def isEdited(self):
        self.edited = True

    # save: Saves the project to the list of projects
    # ARGS: self (QWidget)
    # RETURNS: None
    def save(self):
        self.saved = True
        # Get information from UI
        tempProject = self.getProject()
        self.parent_window.projectList.append(tempProject)
        self.parent_window.updateUserList()
        self.close()

    # closeEvent: Changes the default closing behavior by overriding the base method
    # ARGS: self (QMainWindow), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: none
    def closeEvent(self, event):
        # If parent is closing, force close
        if self.parent_closing:
            event.accept()
        # If the form is editing and the form is not saved, prompt for cancellation
        if self.editing and self.edited and not self.close_from_save:
            temp = QMessageBox.question(self, 'Cancel Confirmation',
                                        'Are you sure you want to cancel project updates?',
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Save, QMessageBox.No)
        elif self.edited and (not self.close_from_save):
            temp = QMessageBox.question(self, 'Cancel Confirmation',
                                        'Are you sure you want to cancel project creation?',
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Save, QMessageBox.No)
        else:
            event.accept()
            return

        # Logic based on message box choice, only executes if not saved and edited
        if temp == QMessageBox.Yes:
            event.accept()
        elif temp == QMessageBox.Save:
            # Update or save based on state of window
            if self.editing:
                self.updateProject()
            else:
                self.save()
            event.accept()
        else:
            event.ignore()

    # editing: Updates the window to contain info of editing object
    # ARGS: self (QWidget), project (object.Project)
    # RETURNS: None
    def edit(self, project=object.Project):
        self.editing_project = project
        self.findChild(QLineEdit, "billing_input").setText(project.formatBillingCodes())
        self.findChild(QLineEdit, "expected_hours_input").setText(str(project.expected_hours))
        self.findChild(QLineEdit, "title_input").setText(project.name)
        self.findChild(QTextEdit, "description_input").setText(project.description)
        self.edited = False

    # updateProject: Updates an existing project instead of creating a new one
    # ARGS: self (QWidget)
    # RETURNS: None
    def updateProject(self):
        # Get updated project and remove old one from list
        self.parent_window.projectList.remove(self.editing_project)
        project = self.getProject()
        project.users = self.project_user_list
        # Add to list and update master list in main UI
        self.parent_window.projectList.append(project)
        self.parent_window.updateUserList()
        # Update closing vars
        self.saved = True
        self.close_from_save = True
        # Update parent window selected pane
        self.parent_window.newSelected(QListWidgetItem(project.name))
        # TODO: Database updates

        self.close()

    # getProject: Create a project from the form fields
    # ARGS: self (QWidget)
    # RETURNS: object.Project
    def getProject(self):
        billing_input = self.findChild(QLineEdit, "billing_input")
        expected_hours_input = self.findChild(QLineEdit, "expected_hours_input")
        title_input = self.findChild(QLineEdit, "title_input")
        description_input = self.findChild(QTextEdit, "description_input")
        billing_codes = billing_input.text()
        expected_hours = expected_hours_input.text()
        name = title_input.text()
        description = description_input.toPlainText()
        description_input.clear()

        # Fix billing codes to either string or list
        if "," in billing_codes:
            billing_codes = billing_codes.split(",")

        # Save as new object
        return object.Project(name, description, billing_codes, expected_hours)

    # addUsers: Opens a window where users can be added to a project
    # ARGS: self (QWidget)
    # RETURNS: None
    def addUsers(self):
        try:
            self.add_user_window = AddUsersGUI(self.editing_project, self)
            self.add_user_window.initUI()
            self.edited = True
        except Exception as e:
            print(e)
