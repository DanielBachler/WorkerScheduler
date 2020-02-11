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
    userList = tempUserList()
    ex = ws_gui.Main_UI(userList)
    conn = ws_db.DB_Connection()
    conn.db_login(ex)
    conn.init_db()
    ex.initUI()
    ex.setWindowIcon(QIcon('icon.png'))

    sys.exit(app.exec_())


# METHOD FOR TESTING
def tempUserList():
    userDan = object.User("Dan", "9.95", "1", "Capstone", "Gary", "2460239", ("Work Scheduler", "Robotics"), 20, 18)
    userBrendan = object.User("Brendan", "15", "1", "Capstone", "NA", "1", ("Work Scheduler", "Test"), 69, 96)
    userJesse = object.User("Jesse", "20", "1", "Capstone", "NA", "2", ("Work Scheduler", "Robotics"), 40, 0)
    tempList = [userBrendan, userDan, userJesse]
    return tempList

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
else:
    print("Unable to import as module")