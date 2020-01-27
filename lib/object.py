## The Work Scheduler
## Montana State University senior design project
##
## Copyright 2019
##
## Created: 2019-10-19 by Dan Bachler
## object.py
## User and Project Object Container for Work Scheduler

if __name__ == "__main__":
    print("Unable to execute as script")
    exit(-1)


class User:
    name = ""
    pay = ""
    rank = ""
    team = ""
    mentor = ""
    employee_id = ""
    desired_hours = ""
    actual_hours = ""
    # Dict with project titles as keys, values are lists with first value as projected hours, second as actual hours
    projects = {}

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
        try:
            projects_string = ""

            for project in self.projects.keys():
                projects_string += project.title + "\n"

            return projects_string
        except:
            print("Failed to print projects")

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


class Project:
    expected_hours = ""
    billing_code = ""
    hours_edit_date = ""
    title = ""
    users = []

    # __init__: Initializes a given project
    # ARGS: self (Project), expected_hours (String), billing_code (String), title (String)
    # RETURNS: Project
    def __init__(self, expected_hours, billing_code, title):
        self.expected_hours = expected_hours
        self.billing_code = billing_code
        self.title = title

    # print_project: Makes a string for a project in a formatted manor
    # ARGS: self (Project)
    # RETURNS: None
    def print_project(self):
        print_string = ("Title: %s\nBilling Code: %s\nExpected Hours: %s\n"
                        "Date of Last Edit: %s\nAssigned Employees: %s" %
                        (self.title, self.billing_code, self.expected_hours, self.hours_edit_date,
                         self.print_users()))
        return print_string

    # print_users: Makes a formatted string for the users assigned to a project
    # ARGS: self (Project)
    # RETURNS: None
    def print_users(self):
        user_string = ""
        for user in self.users:
            user_string += user.name + "\n"
        return user_string
