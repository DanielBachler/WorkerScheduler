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
    projects = ()

    def __init__(self, name, pay, rank, team, mentor, employee_id, projects):
        self.name = name
        self.pay = pay
        self.rank = rank
        self.team = team
        self.mentor = mentor
        self.employee_id = employee_id
        self.projects = projects

    def set_name(self, name):
        self.name = name

    def set_pay(self, pay):
        self.pay = pay

    def set_rank(self, rank):
        self.rank = rank

    def set_mentor(self, mentor):
        self.mentor = mentor

    def set_id(self, employee_id):
        self.employee_id = employee_id

    def set_projects(self, projects):
        self.projects = projects

    # TODO: Setters

    def print_user(self):
        print("User Name: %s\nUser Rank: %s" % (self.name, self.rank))


class Project:
    pass
