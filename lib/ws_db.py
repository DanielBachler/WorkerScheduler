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

import sqlite3

import mysql.connector as sql

from lib import CONSTANTS as K
from lib import ws_gui

DB_TYPE = sqlite3

# Manages connection with mySQL database
class DB_Connection:

    cnx = None
    crs = None

    def __init__(self):
        pass

    # Login to database. Store open connection
    def db_login(self, ex):
        srv_addr, uname, pw = ex.login()
        if DB_TYPE is sqlite3:
            self.cnx = sqlite3.connect("ws.db")
            self.crs = self.cnx.cursor()
        else:
            self.cnx = sql.connect(user=uname, password=pw, host=srv_addr, database='tws')
            print(self.cnx)
        print("Connected to database!")

    def init_db(self):
        if self.crs == None or self.cnx == None:
            return
        else:
            self.db_command("CREATE TABLE IF NOT EXISTS employee (eid integer primary key, employee_name varchar(64), rank integer, emp_role integer, hourly_rate real, mentor integer default NULL);")
            self.db_command("CREATE TABLE IF NOT EXISTS project (pid integer primary key, project_name varchar(64), description varchar(1024), estimated_hrs real, start_year integer, start_month integer, end_year integer, end_month integer, rpt int, last_update date);")
            self.db_command("CREATE TABLE IF NOT EXISTS team (tid integer primary key, team_name varchar(32));")
            self.db_command("CREATE TABLE IF NOT EXISTS billing_code (code integer primary key);")
            self.db_command("CREATE TABLE IF NOT EXISTS billing_code_assignment (pid integer, code varchar(16));")
            self.db_command("CREATE TABLE IF NOT EXISTS team_membership (tid integer, eid integer);")
            self.db_command("CREATE TABLE IF NOT EXISTS project_assignment (eid integer, pid integer);")
            self.db_command("CREATE TABLE IF NOT EXISTS user_project (ipid integer primary key, billing_code integer, eid integer, projected_hours real default NULL, requested_hours real default NULL, earned_hours real default 0);")
            self.db_command("CREATE TABLE IF NOT EXISTS company_info (company_name varchar(32));")
            # TODO: Table for time assignments
            self.db_command("CREATE TABLE IF NOT EXISTS emp_role (role_id integer primary key, role_name varchar(32));")
            self.db_command("CREATE TABLE IF NOT EXISTS access_level (level_id integer primary key, level_name varchar(16));")
            self.db_command("CREATE TABLE IF NOT EXISTS user_proj_past (upid integer, start_yr integer, start_mo integer, end_yr integer, end_mo integer, projected_hrs real, actual_hrs real);")
            self.db_command("CREATE TABLE IF NOT EXISTS proj_past (pid integer, start_yr integer, start_mo integer, end_yr integer, end_mo integer, projected_hrs real, actual_hrs real);")

            self.db_command("INSERT INTO employee (eid, employee_name) VALUES (0, 'manager');")

    # Return a user's information
    def get_user_info(self):
        self.db_command("GRANT ALL ON *.* to user@localhost IDENTIFIED BY 'password'; ")    # TODO
        self.db_command("GRANT ALL ON *.* to user@'%' IDENTIFIED BY 'password';")           # TODO


    # Set a company's information. This only needs to be done once.
    def set_company_info(self):
        pass

    # Create a database user.
    def create_user(self):
        eid = 0
        name = "Bob"
        rank = 0
        rate = 10.0
        # TODO: Create mySQL user
        stmt = "INSERT INTO employee VALUES (%d, '%s', %d, %f);" % (eid, name, rank, rate)
        self.db_command(stmt)

    # Delete a database user.
    def del_user(self):
        name = "Bob"
        stmt = 'DELETE FROM employee WHERE employee_name="%s";' % name
        self.db_command(stmt)

    # List all users
    def list_users(self):
        users = self.db_query('select * from employee;')
        # TODO: Do we want to return only a subset of the fields in employee
        return users

    # Allow user to request hours
    def user_request_hours(self):
        pass

    # Allow user to log hours
    def user_log_hours(self):
        pass

    # Create project
    def create_project(self):
        pass

    # Get information on a project
    def get_project_data(self):
        pass

    # List all projects
    def list_projects(self):
        pass

    # Remove a project
    def delete_project(self):
        pass

    # Add user to team
    def add_user_to_team(self):
        pass

    # Remove user from team
    def remove_user_from_team(self):
        pass

    # Fetch teams for a given user
    def get_teams_for_user(self):
        pass

    # Fetch users on a given team
    def get_users_on_team(self):
        pass

    # Associate user with project
    def add_user_to_project(self):
        pass

    # Remove user from project
    def remove_user_from_project(self):
        pass

    # Fetch users on a given project
    def get_users_for_project(self):
        pass

    # Associate billing code with project
    def add_billing_code_for_project(self):
        pass

    # Disassociate billing code from project
    def remove_billing_code_from_project(self):
        pass

    # Return all billing codes
    def list_all_billing_codes(self):
        pass

    # Return all projects
    def list_all_projects(self):
        pass

    # Return all teams
    def list_all_teams(self):
        pass

    # Execute database query
    def db_command(self, stmt):
        try:
            self.crs.execute(stmt)
            self.cnx.commit()
        except Exception as e:
            print("Error executing command", str(e), stmt)

    # Execute database query
    def db_query(self, stmt):
        try:
            self.crs.execute(stmt)
            return self.crs.fetchall()
        except Exception as e:
            print("Error executing query", str(e), stmt)