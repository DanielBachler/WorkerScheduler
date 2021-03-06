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
import sys
from datetime import datetime

import mysql.connector as sql

from src import dbcalls

DB_TYPE = sql   # Set to sqlite3 to use sqlite. (for quick testing and development, depreciated)

connect = None  # Singleton instance of database connection

# Manages connection with mySQL database
class DB_Connection:

    cnx = None
    crs = None

    def __init__(self):
        pass

    # Create singleton database connection
    @staticmethod
    def connect_to_db(ex, fresh=False):
        global connect
        if connect is None:
            connect = DB_Connection()
            connect.db_login(ex)
            if fresh:
                connect.init_db()
            dbcalls.init_dbwrapper(connect)
        else:
            print("Unable to create new database connection. Connection already active.", file=sys.stderr)

    # Login to database. Store open connection
    def db_login(self, ex):
        srv_addr, uname, pw = ex.login()
        if DB_TYPE is sqlite3:
            self.cnx = sqlite3.connect("ws.db")
            self.crs = self.cnx.cursor()
        else:
            self.cnx = sql.connect(user=uname, password=pw, host=srv_addr, database='tws')
            self.crs = self.cnx.cursor()
            print(self.cnx)
        print("Connected to database!")

    def init_db(self):
        if self.crs == None or self.cnx == None:
            return
        else:
            print("Creating database")
            self.db_command("CREATE TABLE IF NOT EXISTS employee (eid integer not null, employee_name varchar(64),"
                            "rank varchar(32), emp_role integer, hourly_rate real, mentor varchar(64) default NULL,"
                            "PRIMARY KEY (eid));")
            self.db_command("CREATE TABLE IF NOT EXISTS project (pid integer not null auto_increment, "
                            "project_name varchar(64), description varchar(1024), estimated_hrs real, start_year integer, "
                            "start_month integer, end_year integer, end_month integer, rpt int, last_update date,"
                            "PRIMARY KEY (pid));")
            self.db_command("CREATE TABLE IF NOT EXISTS team (tid integer not null auto_increment,"
                            "team_name varchar(32), PRIMARY KEY (tid));")
            self.db_command("CREATE TABLE IF NOT EXISTS billing_code (code integer not null primary key);")
            self.db_command("CREATE TABLE IF NOT EXISTS billing_code_assignment (pid integer, code integer,"
                            "PRIMARY KEY (pid, code));")
            self.db_command("CREATE TABLE IF NOT EXISTS team_membership (tid integer, eid integer, PRIMARY KEY (tid, eid));")
            self.db_command("CREATE TABLE IF NOT EXISTS user_project (pid integer not null,"
                            "billing_code integer, eid integer, projected_hours real default NULL,"
                            "requested_hours real default NULL, earned_hours real default 0);")
            # self.db_command("CREATE TABLE IF NOT EXISTS company_info (company_name varchar(32));")
            self.db_command("CREATE TABLE IF NOT EXISTS time_assignments (code integer, eid integer, mo integer,"
                            "yr integer, hrs real, PRIMARY KEY (code, eid, mo, yr));")
            self.db_command("CREATE TABLE IF NOT EXISTS emp_role (role_name varchar(32), primary key (role_name));")

            self.db_command("CREATE INDEX emp_name ON employee(employee_name);")
            self.db_command("CREATE INDEX rank_idx ON emp_role(role_name);")

            self.db_command("ALTER TABLE time_assignments ADD FOREIGN KEY (eid) REFERENCES employee(eid) ON DELETE SET NULL")
            self.db_command("ALTER TABLE time_assignments ADD FOREIGN KEY (code) REFERENCES billing_code(code) ON DELETE SET NULL;")

            self.db_command("ALTER TABLE team_membership ADD FOREIGN KEY (tid) REFERENCES team(tid) ON DELETE CASCADE")
            self.db_command("ALTER TABLE team_membership ADD FOREIGN KEY (eid)REFERENCES employee(eid) ON DELETE CASCADE ")

            self.db_command("ALTER TABLE employee ADD FOREIGN KEY (rank) REFERENCES emp_role(role_name) ON DELETE SET NULL;")

            self.db_command("ALTER TABLE billing_code_assignment ADD FOREIGN KEY (code) REFERENCES billing_code(code) ON DELETE SET NULL;")
            self.db_command("ALTER TABLE billing_code_assignment ADD FOREIGN KEY (pid) REFERENCES project(pid) ON DELETE SET NULL ")

    def set_admin_user(self, name):
        self.db_command("GRANT ALL ON *.* TO '%s'@'localhost';" % name)
        self.db_command("GRANT ALL ON *.* TO '"+name+"'@'%';")
        self.db_command("FLUSH PRIVILEGES;")

    # Create a database user.
    def create_user(self, eid, name, rank="NULL", rate="NULL", role="1", mentor="NULL"):
        stmt = "CREATE USER '%s'@'localhost';" % name
        self.db_command(stmt)
        stmt = "CREATE USER '"+name+"'@'%';"
        self.db_command(stmt)
        self.set_admin_user(name)
        if role is None:
            role = "0"
        stmt = '''INSERT INTO employee(eid, employee_name, emp_role, hourly_rate, mentor, rank) VALUES 
                    (%s, "%s",%s, %f, "%s","%s");''' % (str(eid), name, str(role), float(rate), str(mentor), str(rank))
        self.db_command(stmt)

    # Update user by EID
    def update_user(self, eid, name, rank="NULL", rate="NULL", role="1", mentor=""):
        if rank == "" or rank == "None":
            rank = "NULL"
        if mentor == "None":
            mentor = ""
        if role is None:
            role = "0"
        stmt = '''UPDATE employee SET employee_name="%s", rank="%s", emp_role=%s, hourly_rate=%s, mentor="%s" WHERE
                    eid=%s;''' % (name, str(rank), str(role), str(rate), mentor, str(eid))
        self.db_command(stmt)

    # Delete a database user.
    def rm_user(self, eid):
        stmt = 'DELETE FROM employee WHERE eid=%d;' % eid
        self.db_command(stmt)

    # List all users
    def list_users(self):
        res = self.db_query("SELECT * from employee;")
        if res is None:
            print("Error executing query on database,", file=sys.stderr)
        return res

    # Create project
    def create_project(self, name, desc, est_hrs, start_yr, start_mo, end_yr, end_mo, rpt):
        dt = datetime.today().strftime('%Y-%m-%d')
        stmt = 'INSERT INTO project (project_name, description, estimated_hrs, start_year, start_month, end_year, ' \
               'end_month, rpt, last_update) VALUES ("%s", "%s", %f, %s, %s, %s, %s, %d, "%s")' % (name, desc, float(est_hrs),
                                                                                              start_yr, start_mo, end_yr,
                                                                                              end_mo, rpt, str(dt))
        self.db_command(stmt)

    # Create project
    def update_project(self, pid, name, desc, est_hrs, start_yr, start_mo, end_yr, end_mo, rpt, last_update=""):
        dt = last_update if last_update == "" else datetime.today().strftime('%Y-%m-%d')
        repeat = "1" if rpt else "0"

        stmt = '''UPDATE project SET pid=%d, project_name="%s", description="%s", estimated_hrs=%s, start_year=%s,
                    start_month=%s, end_year=%s, end_month=%s, rpt=%s, last_update="%s" WHERE project_name="%s";''' \
               % (int(pid), name, desc, str(est_hrs), str(start_yr), str(start_mo), str(end_yr), str(end_mo), repeat, dt, name)
        self.db_command(stmt)

    def add_userproj(self, pid, code, eid, proj_hours, req_hrs, earn_hours):
        if str(req_hrs) == "":
            req_hrs = "NULL"
        if str(earn_hours) == "":
            earn_hours = "NULL"
        stmt = '''INSERT INTO user_project (pid, billing_code, eid, projected_hours, requested_hours, earned_hours) 
        VALUES (%s, %s, %s, %s, %s, %s);''' % (str(pid), str(code), str(eid), str(proj_hours), str(req_hrs),
                                               str(earn_hours))
        self.db_command(stmt)

    def update_userproj(self, pid, code, eid, proj_hours, req_hrs, earn_hours):
        if str(req_hrs) == "":
            req_hrs = "NULL"
        if str(earn_hours) == "":
            earn_hours = "NULL"
        if earn_hours is None:
            earn_hours = 0
        if req_hrs is None:
            req_hrs = "NULL"
        stmt = '''UPDATE user_project SET pid=%s, billing_code=%s, eid=%s, projected_hours=%s, requested_hours=%s,
                    earned_hours=%s WHERE billing_code=%s AND eid=%s;''' % (str(pid), str(code), str(eid), str(proj_hours), str(req_hrs),
                                                                            str(earn_hours), str(code), str(eid))
        self.db_command(stmt)

    # Create a team
    def create_team(self, name):
        stmt = 'INSERT INTO team (team_name) VALUES ("%s");' % name
        self.db_command(stmt)

    # Add user to team
    def add_user_to_team(self, eid, tid):
        stmt = 'INSERT INTO team_membership VALUES (%d, %d);' % (tid, eid)
        self.db_command(stmt)

    # Add employee rank to database
    def add_rank(self, rank):
        stmt = '''INSERT INTO emp_role (role_name) VALUES ("%s");''' % str(rank)
        self.db_command(stmt)

    def rm_rank(self, rank):
        stmt = '''DELETE FROM emp_role WHERE role_name="%s"''' % str(rank)
        self.db_command(stmt)

    # Remove user from team
    def remove_user_from_team(self, tid, eid):
        stmt = '''DELETE FROM team_membership WHERE tid=%d AND eid=%d''' % (int(tid), int(eid))
        self.db_command(stmt)

    # Fetch teams for a given user
    def get_teams_for_user(self, eid):
        stmt = '''SELECT tid FROM team_membership WHERE eid=%d''' % int(eid)
        res = self.db_query(stmt)
        if res is None:
            return []
        teams = []
        for tup in res:
            teams.append(tup[0])
        return res

    # Fetch users on a given team
    def get_users_on_team(self, tid):
        stmt = '''SELECT eid FROM team_membership WHERE tid=%d''' % int(tid)
        res = self.db_query(stmt)
        if res is None:
            return []
        users = []
        for tup in res:
            users.append(tup[0])
        return res

    # Add billing code to database
    def add_billing_code(self, bc):
        print("New billing code:", bc)
        stmt = 'INSERT INTO billing_code VALUES (%s)' % str(bc)
        self.db_command(stmt)

    # Associate billing code with project
    def add_billing_code_for_project(self, pid, bc):
        stmt = 'INSERT INTO billing_code_assignment VALUES (%s, %s);' % (str(pid), str(bc))
        self.db_command(stmt)

    # Return all teams
    def list_all_teams(self):
        res = self.db_query("SELECT * from team;")
        if res is None:
            print("Error executing query on database,", file=sys.stderr)
        return res

    # Check if an SQL query has comments. This likely is an injection attack
    def _check_attack(self, stmt):
        if "#" in stmt or "--" in stmt or "/*" in stmt:
            print("Probable SQL Injection attack detected. Will not execute query.", file=sys.stderr)
            return True
        return False

    # Execute database query
    def db_command(self, stmt):
        if self._check_attack(stmt):
            return
        try:
            self.crs.execute(stmt)
            self.cnx.commit()
        except Exception as e:
            print("Error executing command", str(e), stmt, file=sys.stderr)

    # Execute database query
    def db_query(self, stmt):
        if self._check_attack(stmt):
            return [[]]
        try:
            self.crs.execute(stmt)
            return self.crs.fetchall()
        except Exception as e:
            print("Error executing query", str(e), stmt, file=sys.stderr)
