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
    ws_db.connect_to_db(ex)

    rank_list = ["Sr. Analyst", "Analyst", "Principle", "New Analyst", "Consultant", "Admin"]

    dbcalls.update_ranks(rank_list)

    ex.initUI()
    ex.setWindowIcon(QIcon('icon.png'))

    sys.exit(app.exec_())


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
