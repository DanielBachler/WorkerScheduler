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

FRESH_INSTANCE_MODE = False     # Set to be true by first command line argument. Use to configure database server

def main():
    # TEMP

    if len(sys.argv) == 2:
        if sys.argv[1] == "fresh":
            global FRESH_INSTANCE_MODE
            FRESH_INSTANCE_MODE = True

    ex = ws_gui.Main_UI()
    ws_db.DB_Connection.connect_to_db(ex, fresh=FRESH_INSTANCE_MODE)

    if FRESH_INSTANCE_MODE:
        dbcalls.update_ranks( ["Sr. Analyst", "Analyst", "Principle", "New Analyst", "Consultant", "Admin"])

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
