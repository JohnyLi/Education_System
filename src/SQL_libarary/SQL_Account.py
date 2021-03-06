from Config.Link_db import *
from Config.Config import *
import time
from SQL_libarary.Func_lib import *

#此类作为对Account表进行操作的sql方法的libarary
#Account表为存放用户账号、密码和权限的表

#---------------------------------------------全局配置--------------------------------------------#

table_section="table"
#table name config

myconfig=Aconfig()#获取config配置


AccountTable=myconfig.getvalue(table_section,"AccountTable")    #获取Account表名
LogTable=myconfig.getvalue(table_section,"LogTable")    #获取日志表名

#---------------------------------------------全局配置--------------------------------------------#

class SQL_Account:

    #初始化在类中储存数据库连接
    def __init__(self,db):
        self.__db = db  #获取与database的连接的class

        # 往日志中增加一条日志
    def insertlog(self, username, operation):
            Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = "insert into %s (userid,operation,Time) " \
                  "select userid , '%s' , '%s' from %s where username='%s' " % (
                      LogTable, operation, Time, AccountTable, username)
            status = self.__db.update(sql)
            return status

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
    def CheckPassword(self,username,password):
        sql = " select password from %s where username='%s'" % (AccountTable, username)
        data = self.__db.select(sql)
        data=data[0][0]
        if(data==GetSHA(password)):
            return True
        else:
            return False

    #修改密码
    def UpdateAccount(self,username,password):
        # 将密码加密
        SHA_password=GetSHA(password)
        sql = " update %s set password='%s' where username='%s'" % (AccountTable,SHA_password ,username)
        status = self.__db.update(sql)
        self.insertlog(username,"修改密码")
        return status


    #增加一条用户账号密码
    def InsertAccount(self,username,password,privilege):
        # 将密码加密
        SHA_password = GetSHA(password)
        sql = " insert into %s (username,password,privilege) values('%s','%s',%d)" % (AccountTable,username,SHA_password,privilege)
        status = self.__db.update(sql)
        self.insertlog("admin", "增加用户")
        return status

    #删除一条用户账号密码
    def DeleteAccount(self,username):
        sql = " delete from %s where username = '%s' " %(AccountTable,username)
        status = self.__db.update(sql)
        self.insertlog("admin", "删除用户")
        return status

    #获取某权限下所有用户
    def getAllbyPrivilege(self,privilege):
        sql = "select username from %s where privilege=%s " %(AccountTable,privilege)
        data = self.__db.select(sql)
        result=[]
        for i in data:
            result.append(i[0])
        return result

    #根据用户名获取其ID
    def getIDbyName(self,username):
        sql = "select userid from %s where username='%s'" %(AccountTable,username)
        data = self.__db.select(sql)
        return data[0][0]

    #根据ID获取用户名
    def getNamebyID(self,userid):
        sql = "select username from %s where userid='%s'" % (AccountTable, userid)
        data = self.__db.select(sql)
        return data[0][0]

    #重置数据库
    def reset(self):

            self.__db.reset()
            self.InsertAccount('admin','admin',3)
            return True







