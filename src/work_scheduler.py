#!/usr/bin/env python3

## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Brendan Kristiansen
## work_scheduler.py
## Driver for The Work Scheduler

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from lib import ws_gui
from lib import ws_db
from lib import CONSTANTS as K
from lib import object

app = None


def main():
    projectList = tempProjectList()
    userList = tempUserList(projectList)
    ex = ws_gui.Main_UI()
    conn = ws_db.DB_Connection()
    conn.db_login(ex)
    ex.initUI(userList, projectList)
    ex.setWindowIcon(QIcon('icon.png'))

    sys.exit(app.exec_())


# METHOD FOR TESTING
def tempUserList(project_list):
    userDan = object.User("Dan", "9.95", "1", "Capstone", "Gary", "2460239", (project_list[1], project_list[2]), 20, 18)
    userBrendan = object.User("Brendan", "15", "1", "Capstone", "NA", "1", (project_list[0], project_list[2]), 69, 96)
    userJesse = object.User("Jesse", "20", "1", "Capstone", "NA", "2", (project_list[3], project_list[2]), 40, 0)
    tempList = [userBrendan, userDan, userJesse]
    return tempList


# METHOD FOR TESTING
def tempProjectList():
    project1 = object.Project("14", "317", "Johnson Project")
    project2 = object.Project("24", "219", "Fairweather Account")
    project3 = object.Project("12", "519", "Beckham Account")
    project4 = object.Project("120", "Geralt", "Rivea Project")
    projectList = [project1, project2, project3, project4]
    return projectList


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
else:
    print("Unable to import as module")