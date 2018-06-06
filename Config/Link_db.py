#!/usr/bin/python3
import pymysql
from Config.Config import *


config_section="database"

#database config
myconfig=Aconfig()

address=myconfig.getvalue(config_section,"dbhost")
port=myconfig.getvalue(config_section,"dbport")
databaseName=myconfig.getvalue(config_section,"dbname")
username=myconfig.getvalue(config_section,"dbuser")
password=myconfig.getvalue(config_section,"dbpassword")

class Link_db:
    def __init__(self):
        self.__db = pymysql.connect(address, username,password, databaseName,charset='utf8')
        self.__cursor = self.__db.cursor()

    def GetCursor(self):
        return self.__db.cursor()

    def select(self,sql):
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            return data
        except:
            print("Error: unable to fecth data with sql query: %s") %(sql)
            return False



    def update(self,sql):
        try:
            Affect=self.__cursor.execute(sql)
            self.__db.commit()
            return Affect
        except:
            print("Error: unable to update data with sql query: %s") % (sql)
            self.__db.rollback()
            return False

    def close(self):
        self.__db.close()

