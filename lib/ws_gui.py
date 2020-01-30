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
#   NewUserGUI: Change rank to drop down and add Admin edit ability for list
#   NewProjectGUI: add forms, functionality (Billing code needs to be multiple entry form)
#   Overall: Master Project list not tied to database for testing, add to main UI
#   Projects: Modify to meet Ed's updated reqs
#   Users: Remove hours as currently implemented and change to dictionary with projects as keys?
#   Overall: Keep ranks as list in database

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from lib import object

from lib import CONSTANTS as K


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

        # Admin menu, only create if user is admin rank
        if self.admin:
            # Menu bar item
            adminMenu = menubar.addMenu("Admin")
            # Actions
            add_rank = QAction("Add new rank", self)
            add_rank.triggered.connect(self.addRank)
            # Add actions
            adminMenu.addAction(add_rank)

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
        deleteSelectedUser = QPushButton('Delete User')
        deleteSelectedUser.setToolTip('This button will permanently delete the selected employee from the database')
        deleteSelectedUser.clicked.connect(self.deletedSelectedFunc)
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
            if not self.newUserWindow.isEnabled():
                self.newUserWindow.close()
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
            selected_project = object.Project
            for project in self.projectList:
                if project.title == name:
                    selected_object = project
            right_view.setText(selected_object.print_project())
        else:
            selected_user = object.User
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
        currentUser = self.centralWidget().findChild(QListWidget).currentItem().text()
        print("Deleting " + currentUser)

    # editSelectedUser: Edits the currently highlighted user
    # ARGS: self (QMainWindow)
    # RETURNS: None
    def editSelectedUser(self):
        currentUser = self.centralWidget().findChild(QListWidget).currentItem().text()
        print("Editing " + currentUser)

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
                left_view.addItem(project.title)
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
                left_view.addItem(project.title)
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
        try:
            hbox_rank = QHBoxLayout()
            rank_label = QLabel("Rank:")
            rank_edit = QComboBox()
            rank_edit.setObjectName("user_rank")
            # Set changed command
            rank_edit.activated.connect(self.boxEdited)
            hbox_rank.addWidget(rank_label)
            hbox_rank.addWidget(rank_edit)
        except Exception as e:
            print(e)

        # # Rank label and editor LEFT
        # hbox_rank = QHBoxLayout()
        # rank_label = QLabel("Rank:")
        # rank_edit = QLineEdit()
        # rank_edit.textEdited.connect(self.boxEdited)
        # rank_edit.setObjectName("user_rank")
        # hbox_rank.addWidget(rank_label)
        # hbox_rank.addWidget(rank_edit)

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
        self.setWindowTitle('New User Form')
        self.show()

    # saveUser: Saves the user currently being created, makes sure that all req fields are filled
    # ARGS: self (QWidget)
    # RETURNS: None
    def saveUser(self):
        if self.box_edited:
            try:
                # Save the entered user in the fields, checks?
                name = self.findChild(QLineEdit, "user_name").text()
                pay = self.findChild(QLineEdit, "user_pay").text()
                rank = self.findChild(QComboBox, "user_rank").currentText()
                team = self.findChild(QLineEdit, "user_team").text()
                mentor = self.findChild(QLineEdit, "user_mentor").text()
                employee_id = self.findChild(QLineEdit, "user_id").text()
                # Place holder for projects, needs more fleshing out
                self.made_user = object.User(name, pay, rank, team, mentor, employee_id)
                self.parent_window.userList.append(self.made_user)
                self.parent_window.updateUserList()
                self.saved = True
                self.close_from_save = True
            except Exception as e:
                print(e)

        self.close()

    # closeEvent: Changes the default closing behavior by overriding the base method
    # ARGS: self (QWidget), event (a QEvent) which is in this case is one of the closing events
    # RETURNS: None
    def closeEvent(self, event):
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


class NewProjectGUI(QWidget):
    main_window = ""
    # If boxes have been edited
    edited = False

    # __init__: Initializes the NewProjectGUI
    # ARGS: self (QWidget)
    # RETURNS: QWidget
    def __init__(self):
        super().__init__()

    # initUI: Creates the UI for the NewProjectGUI
    # ARGS: self (QWidget), main_window (QMainWindow)
    # RETURNS: None
    def initUI(self, main_window):
        # Set parent window
        self.main_window = main_window

        # BUTTONS

        # Save button

        # Cancel button

        # FORMS

        # Billing Codes: LEFT
        billing_label = QLabel("Billing code(s)\nseparated by comma:")
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
        description_input.setObjectName("description_input")
        description_input.textChanged.connect(self.isEdited)
        description_box = QHBoxLayout()
        description_box.addWidget(description_label)
        description_box.addWidget(description_input)

        # Users button: LEFT
        user_button = QPushButton("Add Users")
        user_button.clicked.connect(self.addUsers)
        user_box = QHBoxLayout()
        user_box.addWidget(user_button)

        # Boxes for left and right side
        left_V_box = QVBoxLayout()
        right_V_box = QVBoxLayout()

        # Put into left and right boxes
        left_V_box.addLayout(billing_box)
        right_V_box.addLayout(expected_hours_box)
        left_V_box.addLayout(title_box)
        right_V_box.addLayout(description_box)
        left_V_box.addLayout(user_box)

        # Put into main box
        main_box = QHBoxLayout()
        main_box.addLayout(left_V_box)
        main_box.addLayout(right_V_box)

        # Set Layout
        self.setLayout(main_box)

        # init geometry and show
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('New Project Form')
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    # isEdited: Changes state of self.edited if any forms are modified
    # ARGS: self (QWidget)
    # RETURNS: None
    def isEdited(self):
        self.edited = True

    # addUsers: Form to add users to project and set times
    # ARGS: self (QWidget)
    # RETURNS: None
    def addUsers(self):
        pass


# DEPRECIATED
class AddProjectsGUI(QWidget):
    # List of projects at time of opening
    project_list = []

    # List of projects to assign
    to_assign = []

    # Parent window
    parent_window = ""

    # Currently selected item
    selected_item_all = ""
    selected_item_user = ""

    # __init__: Initializes the AddProjectGUI window
    # ARGS: self (QWidget)
    # RETURNS: QWidget
    def __init__(self):
        super().__init__()

    # initUI: Creates the initial UI for Add Projects window
    # ARGS: self (QWidget), project_list (List[Project]), parent_window (QWidget)
    # RETURNS: None
    def initUI(self, project_list, parent_window):
        # Populate project_list
        self.project_list = project_list
        self.parent_window = parent_window

        # Left Top Panel displaying existing projects
        existing_projects_label = QLabel("All Projects")
        existing_projects = QListWidget()
        existing_projects.itemClicked.connect(self.updateAllProjects)
        existing_projects.setObjectName("existing_projects")

        # Box for panel and label
        existing_projects_box = QVBoxLayout()
        existing_projects_box.addWidget(existing_projects_label)
        existing_projects_box.addWidget(existing_projects)

        # Left Bottom panel displaying selected project info
        existing_selected_label = QLabel("Selected Project Details")
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
        assigned_projects.itemClicked.connect(self.updateUserProjects)
        assigned_projects.setObjectName("assigned_projects")

        # Box for top right panel
        assigned_projects_box = QVBoxLayout()
        assigned_projects_box.addWidget(assigned_projects_label)
        assigned_projects_box.addWidget(assigned_projects)

        # Right bottom panel displaying selected project info
        assigned_selected_label = QLabel("Selected Project Details")
        assigned_selected = QTextEdit()
        assigned_selected.setObjectName("assigned_selected")

        # Box for bottom right panel and label
        assigned_selected_box = QVBoxLayout()
        assigned_selected_box.addWidget(assigned_selected_label)
        assigned_selected_box.addWidget(assigned_selected)

        # V Box for right panels
        right_panel_box = QVBoxLayout()
        right_panel_box.addLayout(assigned_projects_box)
        right_panel_box.addLayout(assigned_selected_box)

        # H Box for panel boxes
        panel_box = QHBoxLayout()
        panel_box.addLayout(left_panel_box)
        panel_box.addLayout(right_panel_box)

        # Button for adding project to user
        add_to_user = QPushButton("Add")
        add_to_user.clicked.connect(self.addToUser)

        # Button to save project list
        save_to_user = QPushButton("Save")
        save_to_user.clicked.connect(self.saveToUser)

        # Button to cancel window
        cancel_window = QPushButton("Cancel")
        cancel_window.clicked.connect(self.close)

        # Button for removing project from user
        remove_from_user = QPushButton("Remove")
        remove_from_user.clicked.connect(self.removeFromUser)

        # H Box for buttons
        button_box = QHBoxLayout()
        button_box.addWidget(add_to_user)
        button_box.addWidget(save_to_user)
        button_box.addWidget(cancel_window)
        button_box.addWidget(remove_from_user)

        # Box to hold everything
        main_box = QVBoxLayout()
        main_box.addLayout(panel_box)
        main_box.addLayout(button_box)

        # Set layout to main layout
        self.setLayout(main_box)

        # Setup functions
        self.initLists()

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Add Project to User')
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    # addToUser: Adds the currently selected project of existing_projects to the user
    # ARGS: self (QWidget)
    # RETURNS: None
    def addToUser(self):
        # Get project object
        real_project = self.getProject(self.selected_item_all.text(), self.project_list)

        # Run updates for various widgets and lists
        self.to_assign.append(real_project)
        self.updateUserProjects(self.selected_item_all)
        self.updateUserProjectsList()

    # removeFromUser: Removes the selected project in assigned_projects from the user
    # ARGS: self (QWidget)
    # RETURNS: None
    def removeFromUser(self):
        # Get project object
        selected_project = self.getProject(self.selected_item_user.text(), self.to_assign)

        # Remove from list
        self.to_assign.remove(selected_project)
        self.updateUserProjectsList()

    # saveToUser: saves the selected project list to the user
    # ARGS: self (QWidget)
    # RETURNS: None
    def saveToUser(self):
        self.parent_window.user_projects = self.to_assign
        self.close()

    # initLists: Populates the two QListWidgets with the appropriate information
    # ARGS: self (QWidget)
    # RETURNS: None
    def initLists(self):
        # Get the QLists to update
        existing_projects = self.findChild(QListWidget, "existing_projects")

        # Populate existing projects
        for project in self.project_list:
            existing_projects.addItem(project.title)

    # updateAllProjects:
    # ARGS: self (QWidget), item (QListWidget item)
    # RETURNS: None
    def updateAllProjects(self, item):
        self.selected_item_all = item

        # Get text window
        text_window = self.findChild(QTextEdit, "existing_selected")

        # Find the project
        selected_project = self.getProject(item.text(), self.project_list)

        # Set text
        text_window.setText(selected_project.print_project())

    # updateUserProjects:
    # ARGS: self (QWidget), item (QListWidget item)
    # RETURNS: None
    def updateUserProjects(self, item):
        # Update highlighted item
        self.selected_item_user = item

        # Get text window
        text_window = self.findChild(QTextEdit, "assigned_selected")

        # Find the project
        selected_project = self.getProject(item.text(), self.to_assign)

        # Set text
        text_window.setText(selected_project.print_project())

    # updateUserProjectsList: Updates the list of user specific projects
    # ARGS: self (QWidget)
    # RETURNS: None
    def updateUserProjectsList(self):
        assigned_projects = self.findChild(QListWidget, "assigned_projects")

        # Clear List
        assigned_projects.clear()

        # Populate
        for project in self.to_assign:
            assigned_projects.addItem(project.title)

    # getProject: Gets the project object given the name
    # ARGS: self (QWidget), project_name (String), project_list (List[Project])
    # RETURNS: selected_project (Project)
    def getProject(self, project_name, project_list):
        selected_project = object.Project
        for project in project_list:
            if project.title == project_name:
                selected_project = project

        return selected_project
