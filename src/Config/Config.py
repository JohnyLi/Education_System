import configparser

#此类用于对config.ini进行操作和查询
#---------------------------------------------全局配置--------------------------------------------#
config_path="Config/config.ini"
#---------------------------------------------全局配置--------------------------------------------#
class Aconfig:
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(config_path)
    def getvalue(self,section,key):
        value=self.__config.get(section,key)
        return value

    def getsection(self,section):
        section = self.__config.items(section)
        return section