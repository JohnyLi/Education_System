from Config.Link_db import *
import time
LogTable="log"
AccountTable="account"
class SQL_Log:
    def __init__(self,db):
        self.__db = db

    def insert(self,username,operation):
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into %s (userid,operation,Time) " \
              "select userid , '%s' , '%s' from %s where username='%s' " % (LogTable,operation,Time,AccountTable,username)
        state =self.__db.update(sql)
        return state
