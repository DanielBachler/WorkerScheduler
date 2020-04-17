## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Dan Bachler
## object.py
## User and Project Object Container for Work Scheduler

from datetime import date

from src import dbcalls

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)


class User:
    name = ""
    pay = ""
    rank = ""
    team = ""
    mentor = None
    employee_id = ""
    # List of UserProject Objects
    projects = []
    # If a user is an admin (0 = False)
    role = 0

    # __init__: Initializes a given user
    # ARGS: self (User), name (String), pay (String), rank (String), team (String), mentor (String),
    #       employee_id (String)
    # RETURNS: User
    def __init__(self, name, pay, rank, team, mentor, employee_id):
        self.name = name
        self.pay = pay
        self.rank = rank
        self.team = team
        if mentor != "NA":
            self.mentor = mentor
        self.employee_id = employee_id

        self.push()

    # Create user from database entry
    @classmethod
    def from_db_row(cls, row):
        if row is None:
            return None

        eid = row[0]
        name = row[1]
        rank = row[2]
        role = 1   # TODO: Use this as an admin flag
        rate = row[4]
        mentor = row[5]

        new_user = cls(name, rate, rank, "", mentor, eid)
        return new_user

    # print_user: Makes a string of the information for the selected user in a formatted fashion
    # ARGS: self (User)
    # RETURNS: print_string (String)
    def print_user(self):
        print_string = ("User Name: %s\nUser Rank: %s\n"
                        "User Pay: %s \nUser Team: %s\n"
                        "User Mentor: %s\nEmployee ID: %s\nProjects: \n%s" %
                        (self.name, self.rank, self.pay, self.team,
                         self.mentor, self.employee_id, self.print_projects()))
        return print_string

    # print_projects: Prints a Users projects using projects.print_project for each Project object
    # ARGS: self (User)
    # RETURNS: projects_string (String)
    def print_projects(self):
        if not self.projects:
            return ""
        else:
            projects_string = ""
            for project in self.projects:
                projects_string += project.name + " " + project.billing_code
            return projects_string

    def push(self):
        dbcalls.update_user(self.employee_id, str(self.name), str(self.role), str(self.pay), str(self.mentor),
                            str(self.rank))

    # getID: returns the unique id (employee_id)
    # ARGS: self (object.User)
    # RETURNS employee_id (string)
    def get_Id(self):
        return self.employee_id

    # TODO: Fix with new UserProject object

    # addProject: adds a project to the dict with projected hours
    # ARGS: self (object.User), project (object.Project), projected_hours (int)
    # RETURNS: None
    def addProject(self, project, projected_hours):
        if project in self.projects.keys():
            current_list = self.projects[project]
            current_list[0] = projected_hours
            self.projects[project] = current_list
        else:
            self.projects[project] = (projected_hours, "NA")


class UserProject:
    billing_code = ""
    owner = ""
    pid = ""
    projected_hours = 0
    # Default is none, to differentiate from desired of 0
    desired_hours = None
    actual_hours = None
    # Dict of past hours by year, keys are years values are ints
    past_actual_hours = {}
    past_planned_hours = {}

    owner = 0

    # __init__: Initializes a user project
    # ARGS: billing_code (String), projected_hours (int), desired_hours (int | None), actual_hours (int | None)
    # Returns: self (object.UserProject)
    def __init__(self, eid, pid, billing_code, projected_hours, desired_hours=None, actual_hours=None):
        self.billing_code = billing_code
        self.projected_hours = projected_hours
        self.desired_hours = desired_hours
        self.actual_hours = actual_hours
        self.owner = eid
        self.pid = pid

        self.push()

    @classmethod
    def create_from_db_row(cls, row):
        pid = row[0]
        billing_code = row[1]
        eid = row[2]
        projected_hours = row[3]
        requested_hours = row[4]
        earned_hours = row[5]
        return cls(eid, pid, billing_code, projected_hours, desired_hours=requested_hours, actual_hours=earned_hours)

    # planned_vs_desired: Calculates the planned vs desired hours diff
    # ARGS: self (object.UserProject)
    # RETURNS: (int)
    def planned_vs_desired(self):
        return self.projected_hours - self.desired_hours

    # actual_vs_planned: Calculates the actual vs planned hours diff
    # ARGS: self (object.UserProject)
    # RETURNS: (int)
    def actual_vs_planned(self):
        return self.actual_hours - self.projected_hours

    # actual_vs_desired: Calculates the actual vs desired diff
    # ARGS: self (object.UserProject)
    # RETURNS: (int)
    def actual_vs_desired(self):
        return self.actual_hours - self.desired_hours

    def push(self):
        dbcalls.update_userproj(self.pid, self.billing_code, self.owner, proj_hrs=self.projected_hours, des_hrs=self.desired_hours,
                                act_hrs=self.actual_hours)

    # toString: Converts data into printable string
    # ARGS: self (object.UserProject)
    # RETURNS: toRet (String)
    def toString(self):
        toRet = "Billing code: " + self.billing_code + "\nProject Hours: " + str(self.projected_hours) + "\nDesired " \
                "Hours: " + str(self.desired_hours) + "\nActual Hours: " + str(self.actual_hours)
        return toRet

    def __str__(self):
        return self.toString()


class Project:
    expected_hours = 0
    # Needs to be list since some projects can have multiple billing codes
    billing_codes = []
    hours_edit_date = ""
    name = ""
    description = ""
    users = []
    id = 0
    repeating = False
    # Dict of past hours by year, keys are years values are ints
    past_actual_hours = {}
    past_planned_hours = {}

    # __init__: Initializes a given project
    # ARGS: self (Project), title (String), description (String), expected_hours (int), billing_code (List[String])
    # RETURNS: Project
    def __init__(self, name, description, billing_code, expected_hours, users=None, repeating=False):
        # If no users given, set to empty list
        if users is None:
            self.users = []
        # Otherwise assign users (will be list of uid's)
        else:
            self.users = users
        self.expected_hours = expected_hours
        self.billing_codes = billing_code
        self.name = name
        # To print: self.hours_edit_date.strftime("%b-%d-%Y")
        self.hours_edit_date = date.today()
        self.description = description
        self.repeating = repeating

    # create_from_db_row: Creates a project object from a DB row
    # ARGS: row (List[db row])
    # RETURNS: object.Project
    @classmethod
    def create_from_db_row(cls, row):
        if row is None:
            return None
        title = row[1]
        desc = row[2]
        # Pull all billing codes from db and associate the right ones
        try:
            all_billing_codes = dbcalls.get_bc_assignments()
            billing_codes = []
            for id, bc in all_billing_codes:
                if id == row[0]:
                    billing_codes.append(bc)
        except Exception as e:
            print(e)
            print("New shit broke")
        # Get the hours for the project
        hours = row[3]
        new_proj = cls(title, desc, billing_codes, hours)
        new_proj.id = row[0]
        new_proj.hours_edit_date = date.today()
        return new_proj

    # print_project: Makes a string for a project in a formatted manor
    # ARGS: self (Project)
    # RETURNS: None
    def print_project(self):
        print_string = ("Title: %s\nDescription: %s\nBilling Code: %s\nExpected Hours: %s\n"
                        "Date of Last Edit: %s\nAssigned Employees: %s" %
                        (self.name, self.description, self.printBillingCodes(), self.expected_hours,
                         self.hours_edit_date.strftime("%b-%d-%Y"), self.print_users()))
        return print_string

    # print_users: Makes a formatted string for the users assigned to a project
    # ARGS: self (Project)
    # RETURNS: user_string (String)
    # TODO: Redo to pull names using the UID list
    def print_users(self):
        user_string = ""
        for user in self.users:
            user_string += user.name + "\n"
        return user_string

    # printBillingCodes: creates a formatted string of the assigned billing codes
    # ARGS: self (object.Project)
    # RETURNS: codes (String)
    def printBillingCodes(self):
        codes = ""
        for code in self.billing_codes:
            codes += str(code) + "\n"
        return codes

    # formatBillingCodes: Puts all the billing codes into a string with commas
    # ARGS: self (object.Project)
    # RETURNS: codes/self.billing_codes (String)
    def formatBillingCodes(self):
        codes = ""
        if len(self.billing_codes) == 1:
            codes = str(self.billing_codes[0])
        elif len(self.billing_codes) == 0:
            codes = ""
        else:
            for i in range(0, len(self.billing_codes)-1):
                codes += str(self.billing_codes[i]) + ", "
            codes += str(self.billing_codes[-1])
        return codes


    def push(self):
        dbcalls.update_project(self.getId(), self.name, self.description, self.expected_hours, last_update=self.hours_edit_date,
                               rpt=self.repeating)

    def get_pid(self):
        return dbcalls.get_pid(self.name)

    # getID: Returns the unique id (id)
    # ARGS: self (object.Project)
    # RETURNS: id (int)
    def getId(self):
        return self.id
