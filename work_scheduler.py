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

from src import ws_gui
from src import ws_db
from src import object
from src import dbcalls

app = None


def main():
    # TEMP

    ex = ws_gui.Main_UI()
    conn = ws_db.DB_Connection()
    dbcalls.init_dbwrapper(conn)
    conn.db_login(ex)
    conn.init_db()

    rank_list = ["Sr. Analyst", "Analyst", "Principle", "New Analyst", "Consultant", "Admin"]
    projectList = tempProjectList()
    userList = tempUserList(projectList)
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
    project2 = object.Project("Fairweather Account", "A Description", ["219789"], 24)
    project3 = object.Project("Beckham Account", "A Description", ["5656565"], 12)
    project4 = object.Project("Rivea Project", "A Description", ["555555"], 120)
    projectList = [project1, project2, project3, project4]
    return projectList


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main()
    except Exception as e:
        print("********** BEGIN EXCEPTION **********")
        print(str(e))
        print(e.with_traceback())
        inpt = input("Press enter to continue...")
else:
    print("Unable to import as module")