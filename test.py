from SQL_libarary.SQL_Account import *
from SQL_libarary.SQL_Log import *
from Config.Config import *
db=Link_db()
database=SQL_Account(db)

print(database.GetInfor("jack"))

myconfig=Aconfig()
#database config
address=myconfig.getsection("route")
mydict=ArrayToDict(address)
print(mydict)

