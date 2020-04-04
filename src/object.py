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
        role = 0    # Brendan to Dan: Set this to something appropriate
        dbcalls.update_user(self.employee_id, str(self.name), str(role), str(self.pay), str(self.mentor), str(self.rank))

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
    def __init__(self, billing_code, projected_hours, desired_hours=None, actual_hours=None, owner=0):
        self.billing_code = billing_code
        self.projected_hours = projected_hours
        self.desired_hours = desired_hours
        self.actual_hours = actual_hours
        self.owner = owner

        self.push()

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
        dbcalls.update_userproj(self.billing_code, self.owner, proj_hrs=self.projected_hours, des_hrs=self.desired_hours,
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
    def __init__(self, name, description, billing_code, expected_hours, users=[], repeating=False):
        # if users is None:
        self.users = []
        # else:
        #     self.users = users
        self.expected_hours = expected_hours
        self.billing_codes = billing_code
        self.name = name
        # To print: self.hours_edit_date.strftime("%b-%d-%Y")
        self.hours_edit_date = date.today()
        self.description = description
        self.repeating = repeating

        try:
            self.push()
            self.id = self.get_pid()

            # for user in users:
            #     # Brendan to Dan: We need the users variable to be a list of UID's.
            #     dbcalls.base.add_user_to_project(user, self.id)

            for code in billing_code:
                dbcalls.associate_billing_code(self.get_pid(), code)
        except Exception as e:
            print(e)

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
        if not isinstance(self.billing_codes, str):
            codes = ""
            for code in self.billing_codes:
                codes += code + "\n"
        else:
            codes = self.billing_codes
        return codes

    # formatBillingCodes: Puts all the billing codes into a string with commas
    # ARGS: self (object.Project)
    # RETURNS: codes/self.billing_codes (String)
    def formatBillingCodes(self):
        if not isinstance(self.billing_codes, str):
            codes = ""
            for i in range(0, len(self.billing_codes)-1):
                codes += self.billing_codes[i] + ", "
            codes += self.billing_codes[-1]
            return codes
        else:
            return self.billing_codes

    def push(self):
        dbcalls.update_project(self.name, self.description, self.expected_hours, last_update=self.hours_edit_date,
                               rpt=self.repeating)

    def get_pid(self):
        return dbcalls.get_pid(self.name)

    # getID: Returns the unique id (id)
    # ARGS: self (object.Project)
    # RETURNS: id (int)
    def getId(self):
        return self.id
