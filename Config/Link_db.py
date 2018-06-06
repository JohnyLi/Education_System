#!/usr/bin/python3
import pymysql
from Config import Config

config_path="Config/config.ini"
config_section="database"

#database config
address=Config.getvalue(config_path,config_section,"dbhost")
port=Config.getvalue(config_path,config_section,"dbport")
databaseName=Config.getvalue(config_path,config_section,"dbname")
username=Config.getvalue(config_path,config_section,"dbuser")
password=Config.getvalue(config_path,config_section,"dbpassword")

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

