## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Dan Bachler
## object.py
## User and Project Object Container for Work Scheduler

from datetime import date

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
        self.mentor = mentor
        self.employee_id = employee_id

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
        if self.projects == []:
            return ""
        else:
            projects_string = ""
            for project in self.projects:
                projects_string += project.name + " " + project.billing_code
            return projects_string

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
    actual_hours = 0
    # Dict of past hours by year, keys are years values are ints
    past_actual_hours = {}
    past_planned_hours = {}

    # __init__: Initializes a user project
    # ARGS:
    # Returns: self (object.UserProject)
    def __init__(self):
        pass

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


class Project:
    expected_hours = 0
    # Needs to be list since some projects can have multiple billing codes
    billing_codes = []
    hours_edit_date = ""
    name = ""
    description = ""
    users = []
    # Dict of past hours by year, keys are years values are ints
    past_actual_hours = {}
    past_planned_hours = {}

    # __init__: Initializes a given project
    # ARGS: self (Project), title (String), description (String), expected_hours (int), billing_code (List[String])
    #       users (List[String?]) (opt)
    # RETURNS: Project
    def __init__(self, name, description, billing_code, expected_hours, users=[]):
        self.expected_hours = expected_hours
        self.billing_codes = billing_code
        self.name = name
        # To print: self.hours_edit_date.strftime("%b-%d-%Y")
        self.hours_edit_date = date.today()
        self.users = users
        self.description = description

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
