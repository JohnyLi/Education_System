#!/usr/bin/python3
from flask import Flask, request, session,redirect, url_for,render_template
from flask_cors import CORS
from Config import Config
from Config.Link_db import *
from SQL_libarary.SQL_Account import *
from hashlib import sha1


#Flask app 相关配置
app=Flask(__name__)
app.config.update(dict( DEBUG=True, SECRET_KEY='Cloud!!!!!2333'))   #config
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
CORS(app, supports_credentials=True)    #跨域

#全局变量配置


#数据库配置
db=Link_db()  #与数据库建立连接
Account = SQL_Account(db)


#--------------------------------------------------------------------------------------------------#
#登录界面
@app.route('/login', methods=['GET', 'POST'])
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
                priority = myAccount[3]
                session['UserName']=username
                session['Login']=True
                return redirect(url_for('main'),priority)


    if session.get('Login')==True:
        if session.get('UserName'):
            username=session['UserName']
            myAccount=Account.GetInfor(username)
            if(len(myAccount)==1):
                priority = myAccount[3]
                return redirect(url_for('main'),priority)
            else:
                session.pop('username',None)
                session.pop('Login',None)

    return render_template('Login.html', error=error)





def GetSHA(var):   #此为SHA单向不可逆加密
    result = sha1()
    result.update(var.encode('utf-8'))
    return result.hexdigest()





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)


