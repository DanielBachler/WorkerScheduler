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
    projects = []

    def __init__(self, name, pay, rank, team, mentor, employee_id, projects, desired_hours, actual_hours):
        self.name = name
        self.pay = pay
        self.rank = rank
        self.team = team
        self.mentor = mentor
        self.employee_id = employee_id
        self.projects = projects
        self.desired_hours = desired_hours
        self.actual_hours = actual_hours

    def print_user(self):
        print_string = ("User Name: %s\nUser Rank: %s\n"
                        "User Pay: %s \nUser Team: %s\n"
                        "User Mentor: %s\nEmployee ID: %s\n"
                        "Desired Hours: %s\nActual Hours: %s\n"
                        "Projects: %s" %
                        (self.name, self.rank, self.pay, self.team,
                         self.mentor, self.employee_id, self.desired_hours, self.actual_hours, self.print_projects()))
        return print_string

    def print_projects(self):
        projects_string = ""
        return projects_string

class Project:
    pass
