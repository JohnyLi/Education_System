#!/usr/bin/python3
from flask import Flask, request, session,redirect, url_for,render_template
from flask_cors import CORS
from Config import Config
from Config.Link_db import *
from SQL_libarary.SQL_Account import *
from SQL_libarary.Func_lib import *

#---------------------------------------------全局配置--------------------------------------------#

#Flask app 相关配置
app=Flask(__name__)
app.config.update(dict( DEBUG=True, SECRET_KEY='Cloud!!!!!2333'))   #config
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
CORS(app, supports_credentials=True)    #跨域

#全局变量配置
myconfig=Aconfig()

route_section="route"
config_path="Config/config.ini"

allurl=ArrayToDict(myconfig.getsection(route_section))
login_url=myconfig.getvalue(route_section,"login")
myinformation_url=myconfig.getvalue(route_section,"myinformation")

#数据库配置
db=Link_db()  #与数据库建立连接
Account = SQL_Account(db)


#---------------------------------------------全局配置--------------------------------------------#
#===============================================页面==============================================#
#登录界面
@app.route('/')
@app.route(login_url, methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username=request.form['username']
        password=request.form['Password']
        myAccount=Account.GetInfor(username)
        if(len(myAccount)!=1):
            error = '用户名或密码错误'
        else:
            AccountSHAPassword=myAccount[2]     #初始设计account表中第三列为加密后的密码
            SHA_password=GetSHA(password)
            if (AccountSHAPassword!=SHA_password):
                error = '用户名或密码错误'
            else:
                privilege = myAccount[3]
                session['username']=username
                session['login']=True
                session['privilege']=privilege
                return redirect(url_for('myinformation'))


    if session.get('login') and session.get('username') and session.get('privilege'):
        return redirect(url_for('myinformation'))
    else:
        session.clear()

    return render_template('login.html', error=error)

###################################################################################################
@app.route(myinformation_url, methods=['GET', 'POST'])
def myinformation():
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        session.clear()
        return redirect(url_for('login'))










#===============================================页面==============================================#
#...............................................main..............................................#
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)


