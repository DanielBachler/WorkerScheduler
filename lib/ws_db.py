## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Brendan Kristiansen
## ws_db.py
## Database wrapper for Work Scheduler

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)

import mysql.connector as sql

from lib import CONSTANTS as K
from lib import ws_gui

# Manages connection with mySQL database
class DB_Connection:

    def __init__(self):
        pass

    # Login to database. Store open connection
    def db_login(self, ex):
        srv_addr, uname, pw = ex.login()

    # Create a database user.
    def create_user(self):
        pass

    # Delete a database user.
    def del_user(self):
        pass