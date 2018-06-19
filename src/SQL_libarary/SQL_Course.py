from Config.Link_db import *
from Config.Config import *
from SQL_libarary.SQL_Account import *
import time


#此类作为对课程进行操作的sql方法的libarary
#Course表为存放courseid、teacherid、name、term和time的表
#Student_Course表为存放courseid、studentid和score的表
#Student_Test表为存放testid、studentid和score的表
#Test_Course表为存放testid、coursetid和testname的表

#---------------------------------------------全局配置--------------------------------------------#

table_section="table"
#table name config

myconfig=Aconfig()#获取config配置

CourseTable=myconfig.getvalue(table_section,"CourseTable")    #获取Course表名
Student_Course_Table=myconfig.getvalue(table_section,"Student_Course_Table")    #获取Student_Course表名
Student_Test_Table=myconfig.getvalue(table_section,"Student_Test_Table")    #获取Student_Test表名
Test_Course_Table=myconfig.getvalue(table_section,"Test_Course_Table")    #获取Test_Course表名
AccountTable=myconfig.getvalue(table_section,"AccountTable")    #获取Account表名
LogTable=myconfig.getvalue(table_section,"LogTable")    #获取日志表名

#---------------------------------------------全局配置--------------------------------------------#

class SQL_Course:
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

    # 根据用户名获取其id
    def GetUserid(self,username):
        sql = "select userid from %s where username='%s' " %(AccountTable,username)
        data = self.__db.select(sql)
        if(len(data)==0):
            return False
        return data[0][0]

    # 通过学生名查询其的课程
    def SearchCourse_1(self,username):
        id=self.GetUserid(username)
        sql = " select name,username from %s s join %s c on c.courseid=s.courseid " \
              "join %s a on a.userid=c.teacherid  where studentid=%s" % (Student_Course_Table,CourseTable,AccountTable,id)
        data = self.__db.select(sql)
        result=[]
        for i in data:
            mydict={}
            mydict['name']=i[0]
            mydict['teacher']=i[1]
            result.append(mydict)
        return result

    # 通过老师名查询其的课程
    def SearchCourse_2(self, username):
        id = self.GetUserid(username)
        sql = " select name,username from %s c join %s a on a.userid=c.teacherid where teacherid=%s" % (CourseTable, AccountTable,id)
        data = self.__db.select(sql)
        result = []
        for i in data:
            mydict = {}
            mydict['name'] = i[0]
            mydict['teacher'] = i[1]
            result.append(mydict)
        return result

    #查询所有课程
    def SearchCourse_3(self):
        sql= "select name,username from %s c join %s a on a.userid=c.teacherid" %(CourseTable,AccountTable)
        data = self.__db.select(sql)
        result = []
        for i in data:
            mydict = {}
            mydict['name'] = i[0]
            mydict['teacher'] = i[1]
            result.append(mydict)
        return result

    def Course_Infor(self,course,studentname):
        sql= "select username,courseid from %s c join %s a on a.userid=c.teacherid where name='%s'" %(CourseTable,AccountTable,course)
        data = self.__db.select(sql)
        courseid=data[0][1]
        teacher=data[0][0]

        sql="select score from %s s join %s a on s.studentid=a.userid where username='%s'" %(Student_Course_Table,AccountTable,studentname)
        data = self.__db.select(sql)
        score=data[0][0]


        sql="select testid,testname from %s where courseid=%s"%(Test_Course_Table,courseid)
        data = self.__db.select(sql)
        testlist=[]
        for i in data:
            mydict={'id':i[0],'testname':i[1]}
            testlist.append(mydict)

        test=[]
        for i in testlist:
            mydict={'testname':i['testname']}
            id=i['id']
            sql="select score from %s s join %s a on a.userid=s.studentid where username='%s' and testid=%s"\
                %(Student_Test_Table,AccountTable,studentname,id)
            data = self.__db.select(sql)
            if(len(data)!=0):
                mydict['score']=data[0][0]
            else:
                mydict['score']=None
            test.append(mydict)


        result={'course':course,'teacher':teacher,'score':score,'test':test}
        return result

    def Course_Score(self,course):
        mycourse={'course':course}
        courseid=self.getCourseID(course)
        testlist=self.getCourseTest(courseid)
        test=[]
        for i in testlist:
            testname = self.getTestName(i)
            test.append(testname)
        mycourse['test'] = test

        sql="select studentid,username,score from %s s join %s a on userid=studentid where courseid=%s"\
            %(Student_Course_Table,AccountTable,courseid)
        data = self.__db.select(sql)
        mycourse['student']=[]
        for i in data:
            mydict={'username':i[1],'userid':i[0],'score':i[2]}
            mytest = []
            for testid in testlist:
                testname=self.getTestName(testid)
                sql = "select score from %s where studentid=%s and testid=%s"%(Student_Test_Table,i[0],testid)
                data1=self.__db.select(sql)
                if(len(data1)==0):
                    mydict1={'name':testname,'score':None}
                else:
                    mydict1 = {'name': testname, 'score': data1[0][0]}
                mytest.append(mydict1)
            mydict['tests']=mytest

            mycourse['student'].append(mydict)

        return mycourse

    def getCourseID(self,course):
        sql = "select courseid from %s where name='%s'" % (CourseTable, course)
        data = self.__db.select(sql)
        courseid = data[0][0]
        return courseid

    def getCourseTest(self,courseid):
        sql = "select testid from %s where courseid=%s" % (Test_Course_Table, courseid)
        data = self.__db.select(sql)
        testlist = []
        for i in data:
            testlist.append(i[0])
        return testlist

    def getTestName(self,testid):
        sql = "select testname from %s where testid=%s" % (Test_Course_Table, testid)
        data = self.__db.select(sql)
        return data[0][0]
    def getTestID(self,testname,course):
        courseid=self.getCourseID(course)
        sql="select testid from %s where courseid=%s and testname='%s'" %(Test_Course_Table,courseid,testname)
        data = self.__db.select(sql)
        return data[0][0]

    def changetestscore(self,userid,course,testname,score):
        testid=self.getTestID(testname,course)
        sql = "select * from %s where studentid=%s and  testid=%s  "%(Student_Test_Table,userid,testid)
        data = self.__db.select(sql)
        if(len(data)==0):
            sql= "insert into %s values(%s,%s,%s) " % (Student_Test_Table,testid,userid,score)
            status = self.__db.update(sql)
            return status
        else:
            sql= "update %s set score=%s where studentid=%s and testid=%s"%(Student_Test_Table,score,userid,testid)
            status = self.__db.update(sql)
            return status

    def changescore(self,userid,course,score):
        courseid=self.getCourseID(course)
        sql="update %s set score=%s where studentid=%s and courseid=%s"%(Student_Course_Table,score,userid,courseid)
        status = self.__db.update(sql)
        return status

    def addtest(self,testname,course):
        courseid = self.getCourseID(course)
        sql="insert into %s (courseid,testname) values(%s,'%s')"%(Test_Course_Table,courseid,testname)
        status = self.__db.update(sql)
        return status

    def addcourse(self,course,username,introduction,time):
        sql = "select courseid from %s where name='%s'" % (CourseTable, course)
        data = self.__db.select(sql)
        if(len(data)!=0):
            return False
        account=SQL_Account(self.__db)
        userid=account.getIDbyName(username)
        sql = "insert into %s (teacherid,name,intro,time) values (%s,'%s','%s','%s')"\
              %(CourseTable,userid,course,introduction,time)
        status = self.__db.update(sql)
        return status
    def courseBYname(self,course):
        sql = "select * from %s where name='%s'"%(CourseTable,course)
        data = self.__db.select(sql)
        if(len(data)==0):
            return False
        data=data[0]
        result={'name':course,'time':data[4],'term':data[3],'intro':data[5]}
        Account=SQL_Account(self.__db)
        teacher=Account.getNamebyID(data[1])
        result['teacher']=teacher
        return result

    def selectcourse(self,username,course):
        courseid = self.getCourseID(course)
        userid = self.GetUserid(username)
        mycourse=self.SearchCourse_1(username)
        for i in mycourse:
            if(course==i['name']):
                return False
        sql = "insert into %s (courseid,studentid) values(%s,%s)"%(Student_Course_Table,courseid,userid)
        status = self.__db.update(sql)
        return status

    def tuike(self,username,course):
        courseid = self.getCourseID(course)
        userid = self.GetUserid(username)
        sql = "delete from %s where studentid=%s and courseid=%s"%(Student_Course_Table,userid,courseid)
        status = self.__db.update(sql)
        testlist=self.getCourseTest(courseid)
        for i in testlist:
            sql = "delete from %s where studentid=%s and testid=%s"%(Student_Test_Table,userid,i)
            status = self.__db.update(sql)

    def changecourse(self,oldname,newname,time,intro):
        sql = "update %s set name='%s',time='%s',intro='%s' where name='%s'" %(CourseTable,newname,time,intro,oldname)
        status = self.__db.update(sql)
        return status

    def addstudent(self,username,course):
        courseid=self.getCourseID(course)
        userid=self.GetUserid(username)
        if(userid==False):
            return "用户名不存在"
        Account=SQL_Account(self.__db)
        infor1=Account.GetInfor(username)
        if(infor1[0][3]!=1):
            return "该用户不为学生"
        sql="select * from %s where studentid=%s"%(Student_Course_Table,userid)
        data=self.__db.select(sql)
        if(len(data)!=0):
            return "该学生已选课"
        else:
            sql="insert into %s (courseid,studentid) values(%s,%s)"%(Student_Course_Table,courseid,userid)
            status = self.__db.update(sql)
            return "增加成功"