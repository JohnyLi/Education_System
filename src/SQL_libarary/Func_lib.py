from hashlib import sha1
from Config.Config import *

#此类存放各种杂乱的方法。

myconfig=Aconfig()

def GetSHA(var):   #此为SHA单向不可逆加密
    result = sha1()
    result.update(var.encode('utf-8'))
    return result.hexdigest()

def GetSideBar(sidebar,activebar=None): #对sidebar进行整理并返回整理好的元组
    result=[]
    for key in sidebar:
        bar1={}
        bar1['name']=key
        bar1['href']=sidebar[key]
        if(activebar==key):
            bar1['active']='active'
        result.append(bar1)
    return result

def ArrayToDict(array): #将array变成dict,将莫名其妙的数据结构整理好并返回
    mydict={}
    for i in array:
        mydict[i[0]]=i[1]
    return mydict

def SetDate(date):
    mydate=date.split('.')
    sentence=''
    for i in range(len(mydate)):
        sentence+=mydate[i]
        if(i!=len(mydate)-1):
            sentence+=','
    return sentence