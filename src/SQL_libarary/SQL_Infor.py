from Config.Link_db import *
from Config.Config import *
from SQL_libarary.SQL_Account import *
from SQL_libarary.SQL_Course import *
import time


#此类作为对Information表进行操作的sql方法的libarary
#Information表为存放userid、telephone、sex和born的表

#---------------------------------------------全局配置--------------------------------------------#

table_section="table"
#table name config

myconfig=Aconfig()#获取config配置

InforTable=myconfig.getvalue(table_section,"InformationTable")    #获取Information表名
AccountTable=myconfig.getvalue(table_section,"AccountTable")    #获取Account表名
CourseTable=myconfig.getvalue(table_section,"CourseTable")    #获取Course表名
LogTable=myconfig.getvalue(table_section,"LogTable")    #获取日志表名

#---------------------------------------------全局配置--------------------------------------------#

class SQL_Infor:
    # 初始化在类中储存数据库连接
    def __init__(self, db):
        self.__db = db  # 获取与database的连接的class

    # 往日志中增加一条日志
    def insertlog(self, username, operation):
            Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = "insert into %s (userid,operation,Time) " \
                  "select userid , '%s' , '%s' from %s where username='%s' " % (
                      LogTable, operation, Time, AccountTable, username)
            status = self.__db.update(sql)
            return status

    #获取全部信息
    def GetAllInfor(self):
        sql = " select * from %s" % (InforTable)
        data = self.__db.select(sql)
        return data

    # 根据用户名获取对应的信息
    def GetInfor(self, username):
            sql = " select username,telephone,sex,born from %s i join %s a on a.userid=i.userid " \
                  "where a.username='%s'" % (InforTable,AccountTable, username)
            data = self.__db.select(sql)
            if (data != False):
                return data
            else:
                return None

    # 根据用户名获取其id
    def GetUserid(self,username):
        sql = "select userid from %s where username='%s' " %(AccountTable,username)
        data = self.__db.select(sql)
        return data[0][0]

    #更新用户信息
    def UpdateInfor(self,username,telephone,sex,born):
        userid=self.GetUserid(username)
        sql= "update %s set telephone='%s',sex='%s',born='%s' where userid='%s'" \
             % (InforTable,telephone,sex,born ,userid)
        status = self.__db.update(sql)
        self.insertlog(username,"更新用户信息")
        return status

    def GetUserBYprivilege(self,privilege):
        sql = "select i.userid,username,born,sex,telephone,privilege from %s i join %s a on a.userid=i.userid where privilege=%s"\
              %(InforTable,AccountTable,privilege)
        data = self.__db.select(sql)
        result=[]
        for i in data:
            mydict={'userid':i[0],'username':i[1],'born':i[2],'sex':i[3],'telephone':i[4],'privilege':i[5]}
            result.append(mydict)
        return result

    def DeleteAll_teacher(self,username):
        Account=SQL_Account(self.__db)
        Course = SQL_Course(self.__db)
        userid=Account.getIDbyName(username)
        sql="Delete from %s where userid=%s" %(InforTable,userid)
        status = self.__db.update(sql)

        Courselist=Course.SearchCourse_2(username)
        for i in Courselist:
            courseid=Course.getCourseID(i['name'])
            testlist=Course.getCourseTest(courseid)
            for testid in testlist:
                sql = "Delete from %s where testid=%s" % (Test_Course_Table, testid)
                status = self.__db.update(sql)
                sql = "Delete from %s where testid=%s" % (Student_Test_Table, testid)
                status = self.__db.update(sql)

        sql="Delete from %s where userid=%s" %(CourseTable,userid)
        status = self.__db.update(sql)
        Account.DeleteAccount(username)
        return True

    def DeleteAll_student(self,username):
        Account = SQL_Account(self.__db)

        userid = Account.getIDbyName(username)
        sql = "Delete from %s where studentid=%s" %(Student_Test_Table,userid)
        status = self.__db.update(sql)
        sql = "Delete from %s where studentid=%s" % (Student_Course_Table, userid)
        status = self.__db.update(sql)
        Account.DeleteAccount(username)
        return True

    def InsertInfor(self,username,password,telephone,sex,born,privilege):
        Account = SQL_Account(self.__db)
        Account.InsertAccount(username,password,privilege)
        userid=Account.getIDbyName(username)
        sql = "Insert into %s values(%s,'%s','%s','%s')"%(InforTable,userid,telephone,sex,born)
        status = self.__db.update(sql)
        return True