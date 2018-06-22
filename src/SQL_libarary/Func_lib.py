from hashlib import sha1
from Config.Config import *
import os

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

def getEXT(filename):
    f=filename.split('.')
    for i in range(len(f)):
        if(i==len(f)-1):
            return f[i]
def getFilename(filename):
    f = filename.split('.')
    newname=""
    for i in range(len(f)):
        if (i == len(f) - 1):
            break
        newname+=f[i]
        if (i < len(f) - 2):
            newname+="."
    return newname

def getFile(file_dir):
    f = file_dir.split('/')
    for i in range(len(f)):
        if (i == len(f) - 1):
            return f[i]
def dir(file_dir):
    f = file_dir.split('/')
    newdir=""
    for i in range(len(f)):
        if (i == len(f) - 1):
            break
        newdir+=f[i]
        if (i < len(f) - 2):
            newdir+="/"
    return newdir

def getAllFile(dir):
    while(dir[len(dir)-1]=="/"):
        newdir=""
        for i in range(len(dir)):
            if(i==len(dir)-1):
                break
            newdir+=dir[i]
        dir=newdir
    set1 = []
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        if os.path.isdir(filepath):
            filepath = filepath.split("\\")[-1]
            mydict={'fname':filepath,'leixing':'文件夹'}
            set1.append(mydict)
        else:
            filepath = filepath.split("\\")[-1]
            mydict = {'fname': filepath, 'leixing': '文件'}
            set1.append(mydict)
    return set1

def checkcourse(coursename,mycourse):
    for i in mycourse:
        if(coursename==i['name']):
            return True
    return False

def GetPageDict(nowpage, data,pageoffset,maxshow):
    nowpage=int(nowpage)
    #nowpage 当前页 data 数据 pageoffset 每页最多条数 maxshow 显示出来的页数
    mydict = {}
    if(len(data)==0):
        return {'page_list':[1],'showdict':[],'showye':0,'nowpage':1,'total':1}
    total = len(data) / pageoffset
    if (total > int(total)):
        total = int(total) + 1
    total = int(total)
    # 向上取整

    mydict['total'] = total
    mydict['nowpage'] = nowpage
    if (nowpage != 1):
        mydict['showye'] = 1
    else:
        mydict['showye'] = 0

    showdict=[]
    page_list=[]
    start=(nowpage-1)*pageoffset+1

    if(start>len(data)):
        nowpage=total
    start=(nowpage-1)*pageoffset+1
    end = start + pageoffset - 1

    if (end > len(data)):
            end = len(data)

    i = start - 1
    while (i < end):
        showdict.append(data[i])
        i += 1

    pagestart = nowpage-2
    if(pagestart<=0):
        pagestart=1
    pageend = pagestart + maxshow -1
    if(pageend>total):
        pageend=total
        pagestart=total-maxshow+1
    if (pagestart <= 0):
        pagestart = 1

    i = pagestart
    while (i <= pageend):
            page_list.append(i)
            i += 1

    mydict['page_list'] = page_list
    mydict['showdict'] = showdict

    return mydict