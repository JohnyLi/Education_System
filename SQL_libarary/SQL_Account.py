from Config.Link_db import *
from Config.Config import *
import time
from SQL_libarary.Func_lib import *

table_section="table"

myconfig=Aconfig()
#table name config
AccountTable=myconfig.getvalue(table_section,"AccountTable")
LogTable=myconfig.getvalue(table_section,"LogTable")


class SQL_Account:

    #初始化在类中储存数据库连接
    def __init__(self,db):
        self.__db = db

    #获得用户账号密码整个表
    def GetAllInfor(self):
        sql = " select * from %s" % (AccountTable)
        data = self.__db.select(sql)
        return data

    #根据用户名获取对应的加密过的密码
    def GetInfor(self,username):
        sql = " select * from %s where username='%s'" % (AccountTable,username)
        data=self.__db.select(sql)
        if(data != False):
            return data
        else:
            return None

    #修改密码
    def UpdateAccount(self,username,password):
        # 将密码加密
        SHA_password=GetSHA(password)
        sql = " update %s set password='%s' where username='%s'" % (AccountTable,SHA_password ,username)
        status = self.__db.update(sql)
        return status


    #增加一条用户账号密码
    def InsertAccount(self,username,password,privilege):
        # 将密码加密
        SHA_password = GetSHA(password)
        sql = " insert into %s (username,password,privilege) values('%s','%s',%d)" % (AccountTable,username,SHA_password,privilege)
        status = self.__db.update(sql)
        return status

    #删除一条用户账号密码
    def DeleteAccount(self,username):
        sql = " delete from %s where username = '%s' " %(AccountTable,username)
        status = self.__db.update(sql)
        return status

    #往日志中增加一条日志
    def insert(self, username, operation):
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into %s (userid,operation,Time) " \
              "select userid , '%s' , '%s' from %s where username='%s' " % (
              LogTable, operation, Time, AccountTable, username)
        status = self.__db.update(sql)
        return status





