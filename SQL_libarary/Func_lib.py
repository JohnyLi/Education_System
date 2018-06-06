from hashlib import sha1
from Config.Config import *


myconfig=Aconfig()

def GetSHA(var):   #此为SHA单向不可逆加密
    result = sha1()
    result.update(var.encode('utf-8'))
    return result.hexdigest()

def GetSideBar(sidebar,activebar=None):
    result=[]
    for bar in sidebar:
        bar1=bar
        name=bar1['name']
        if(activebar==name):
            bar1['active']='active'
        result.append(bar1)
    return result

def ArrayToDict(array):
    mydict={}
    for i in array:
        mydict[i[0]]=i[1]
    return mydict