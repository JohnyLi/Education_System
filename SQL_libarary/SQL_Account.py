from Config.Link_db import *
from hashlib import sha1
import time

config_path="Config/config.ini"
config_section="table"

#table name config
AccountTable=Config.getvalue(config_path,config_section,"AccountTable")
LogTable=Config.getvalue(config_path,config_section,"LogTable")


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
        state = self.__db.update(sql)
        return state


    #增加一条用户账号密码
    def InsertAccount(self,username,password,priority):
        # 将密码加密
        SHA_password = GetSHA(password)
        sql = " insert into %s (username,password,priority) values('%s','%s',%d)" % (AccountTable,username,SHA_password,priority)
        state = self.__db.update(sql)
        return state

    #删除一条用户账号密码
    def DeleteAccount(self,username):
        sql = " delete from %s where username = '%s' " %(AccountTable,username)
        state = self.__db.update(sql)
        return state

    #往日志中增加一条日志
    def insert(self, username, operation):
        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into %s (userid,operation,Time) " \
              "select userid , '%s' , '%s' from %s where username='%s' " % (
              LogTable, operation, Time, AccountTable, username)
        state = self.__db.update(sql)
        return state

def GetSHA(var):   #此为SHA单向不可逆加密
    result = sha1()
    result.update(var.encode('utf-8'))
    return result.hexdigest()



