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

    def __init__(self, name, pay, rank):
        self.name = name
        self.pay = pay
        self.rank = rank


class Project:
    pass
