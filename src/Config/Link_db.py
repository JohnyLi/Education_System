#!/usr/bin/python3
import sqlite3
from Config.Config import *
#此类为database的连接类,每次有用户访问时将会初始化这个类建立连接，访问结束后释放连接
#为了防止每次执行sql语句时都需要进行连接database，所以只在这个类中建立一次连接，执行sql语句时都通过这个类来执行。

#---------------------------------------------全局配置--------------------------------------------#
config_section="database"

#database config
myconfig=Aconfig()  #获取config配置

path=myconfig.getvalue(config_section,"path")  #获得database的路径
init_path=myconfig.getvalue(config_section,"init")  #获得初始化database的sql文本的路径


#---------------------------------------------全局配置--------------------------------------------#

class Link_db:

    #初始化连接
    def __init__(self):
        self.__db = sqlite3.connect(path)
        self.__cursor = self.__db.cursor()


    #返回cursor，实际上并没有用到。
    def GetCursor(self):
        return self.__db.cursor()

    #执行查询的语句，返回多个元组组成的元组。若执行失败则返回bool类型的False
    def select(self,sql):
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            return data
        except:
            print("Error: unable to fecth data with sql query: "+sql)
            return False

    # 执行更新的语句，返回改变了多少行，为int类型。若执行失败则返回bool类型的False
    def update(self,sql):
        try:
            Affect=self.__cursor.execute(sql)
            self.__db.commit()
            return Affect
        except:
            print("Error: unable to update data with sql query: "+sql)
            self.__db.rollback()
            return False

    #关闭连接
    def close(self):
        if(self.__db!=None):
            self.__db.close()

    #重新连接
    def reconnect(self):
        try:
            self.__db = sqlite3.connect(path)
            self.__cursor = self.__db.cursor()
        except:
            print("连接数据库失败")

    #数据库重置
    def reset(self):
        sql=open(init_path,'rb')
        self.__cursor.executescript(sql.read().decode('utf-8'))
        self.__db.commit()



