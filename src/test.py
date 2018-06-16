from SQL_libarary.SQL_Account import *
from SQL_libarary.SQL_Log import *
from Config.Config import *
from urllib import request
import threading
'''
db=Link_db()
database=SQL_Account(db)
print(database.GetInfor('admin'))

'''
def open(url):
    for i in range(5):
        r=request.urlopen(url)
        text= r.read().decode()
        print(text)



if __name__ == '__main__':
    url="http://localhost/introduction"
    la=[]
    for i in range(5):
        t=threading.Thread(target=open,args=(url,))
        la.append(t)
    for i in la:
        i.start()
    for i in la:
        i.join()
