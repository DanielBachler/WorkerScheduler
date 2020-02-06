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

from lib import ws_gui
from lib import ws_db
from lib import CONSTANTS as K

app = None

def main():
    ex = ws_gui.Main_UI()
    conn = ws_db.DB_Connection()
    conn.db_login(ex)
    conn.init_db()
    ex.initUI()

    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
else:
    print("Unable to import as module")