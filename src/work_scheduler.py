#!/usr/bin/env python3

# The Work Scheduler
# Montana State University senior design project
#
# Copyright 2019
#
# Created: 2019-10-19 by Brendan Kristiansen
# work_scheduler.py
# Driver for The Work Scheduler

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from lib import ws_gui
from lib import ws_db
from lib import CONSTANTS as K
from lib import object

app = None


def main():
    # TEMP
    rank_list = ["Sr. Analyst", "Analyst", "Principle", "New Analyst", "Consultant", "Admin"]
    projectList = tempProjectList()
    userList = tempUserList(projectList)
    ex = ws_gui.Main_UI()
    conn = ws_db.DB_Connection()
    conn.db_login(ex)
    conn.init_db()
    ex.initUI(userList, projectList, rank_list)
    ex.setWindowIcon(QIcon('icon.png'))

    sys.exit(app.exec_())


# METHOD FOR TESTING
def tempUserList(project_list):
    userDan = object.User("Dan", "9.95", "1", "Capstone", "Gary", "246239")
    userBrendan = object.User("Brendan", "15", "1", "Capstone", "NA", "123456")
    userJesse = object.User("Jesse", "20", "1", "Capstone", "NA", "987654")
    tempList = [userBrendan, userDan, userJesse]
    return tempList


# METHOD FOR TESTING
def tempProjectList():
    project1 = object.Project("Johnson Project", "A Description", ["317713", "156895"], 14)
    project2 = object.Project("Fairweather Account", "A Description", "219789", 24)
    project3 = object.Project("Beckham Account", "A Description", "5656565", 12)
    project4 = object.Project("Rivea Project", "A Description", "555555", 120)
    projectList = [project1, project2, project3, project4]
    return projectList


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
else:
    print("Unable to import as module")
