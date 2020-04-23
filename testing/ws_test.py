import sys

sys.path.append('../')
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src import ws_gui
from src import ws_db
from src import CONSTANTS as K
from src import object
from src import dbcalls
import unittest

import work_scheduler


class unitTestRunner(unittest.TestCase):
    def test_DB(self):
        self.assertRaises(Exception, work_scheduler.ws_db.DB_Connection())

    def test_Temp_User_List(self):
        userDan = object.User("Dan", "9.95", "1", "Capstone", "Gary", "246239")
        userBrendan = object.User("Brendan", "15", "1", "Capstone", "NA", "123456")
        userJesse = object.User("Jesse", "20", "1", "Capstone", "NA", "987654")
        tempList = [userBrendan, userDan, userJesse]
        if (tempList == work_scheduler.tempUserList(work_scheduler)):
            self.assertTrue()

    def test_DB_Init(self):
        test_GUI_True = dummyGUI(True,0)

        #for i in range(0,7):

         #   test_GUI_False = dummyGUI(False, i)

         #   try:
         #       test_Connection = ws_db.DB_Connection()
         #       test_Connection.db_login(test_GUI_False)

         #   except Exception:
         #       self.fail("Initialization of the database doesn't handle exceptions.")

        try:
            test_Connection = ws_db.DB_Connection()
            dbcalls.init_dbwrapper(test_Connection)
            test_Connection.db_login(test_GUI_True)
        except Exception:
            self.fail("Testing Database failed ")


# Dummy GUI meant for providing dummy data to our database.
class dummyGUI():
    dataType = True
    iteration = 0
    def __init__(self,inDataType, inInteration):
        self.dataType = inDataType
        self.iteration = inInteration
        pass

    #   for testing db login
    def login(self):
        data ={
            0: ("","",""),
            1: (1,0,1),
            2: ("home.jessearstein.com","asdf","sag"),
            3: ("home.jessearstein.com", "jesse","incorrectPass"),
            4: ("192.168.2.1","David", 1),
            5: ("192.168.2.1","bert", "jerry"),
            6: ("home.jessearstein.com",1,'c'),
            7: ('home.jessearstein.com','jesse','pass')
        }
        if(self.dataType == False):
            return data.get(self.iteration, "Out of Bounds")
        else:
            return "home.jessearstein.com","jesse","pass"


if __name__ == '__main__':
    unittest.main()
