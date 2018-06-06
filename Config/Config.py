import configparser

config_path="Config/config.ini"

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