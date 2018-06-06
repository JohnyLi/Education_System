import configparser

def getvalue(path,section,key):
    config = configparser.ConfigParser()
    config.read(path)
    value=config.get(section,key)
    return value
