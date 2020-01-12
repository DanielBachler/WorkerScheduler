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

    cnx = None

    def __init__(self):
        pass

    # Login to database. Store open connection
    def db_login(self, ex):
        srv_addr, uname, pw = ex.login()
        self.cnx = sql.connect(user=uname, password=pw, host=srv_addr, database='tws')
        print(self.cnx)
        print("Connected to database!")

    def init_db(self):
        if self.crs == None or self.cnx == None:
            return
        else:
            self.db_command("CREATE TABLE IF NOT EXISTS employee (eid int, employee_name character, rank int, role character, hourly_rate real);")
            self.db_command("CREATE TABLE IF NOT EXISTS project (pid int, project_name character, estimated_hrs real, start_date date, end_date date, rpt int);")


    # Create a database user.
    def create_user(self):
        pass

    # Delete a database user.
    def del_user(self):
        pass