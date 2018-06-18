#!/usr/bin/python3
from flask import Flask, request, session,redirect, url_for,render_template,g,jsonify
from flask_cors import CORS
from Config import Config
from Config.Link_db import *
from SQL_libarary.SQL_Account import *
from SQL_libarary.SQL_Infor import *
from SQL_libarary.Func_lib import *
import json

#---------------------------------------------全局配置--------------------------------------------#
#全局变量配置
myconfig=Aconfig()

#Flask app 相关配置
flask_section="flask"
app=Flask(__name__)
app.config.update(dict( DEBUG=True, SECRET_KEY=myconfig.getvalue(flask_section,"SECRET_KEY")))   #config
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
CORS(app, supports_credentials=True)    #跨域


#对route路径进行配置
route_section="route"

login_url=myconfig.getvalue(route_section,"login")
myinformation_url=myconfig.getvalue(route_section,"myinformation")
changeinformation_url=myconfig.getvalue(route_section,"changeinformation")
introduction_url=myconfig.getvalue(route_section,"introduction")
logout_url=myconfig.getvalue(route_section,"logout")


studentbar={'查看个人信息':myinformation_url}
teacherbar={'查看个人信息':myinformation_url}
adminbar={'查看个人信息':myinformation_url}


start="1950,1,1"
#---------------------------------------------全局配置--------------------------------------------#
#===============================================页面==============================================#
'''
@app.before_request
def before_request():
        g.db = Link_db()
'''
def get_db():   #使用flask的g对象，每次访问都会有个独立的g对象，保证线程的数据库操作的安全
    if not hasattr(g, 'db'):
        g.db = Link_db()
    return g.db

@app.teardown_appcontext    #用户访问结束后，关闭database连接，释放资源
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()
###################################################################################################
#登录界面
@app.route('/')
@app.route(login_url, methods=['GET', 'POST'])
def login():
    Account=SQL_Account(get_db())
    error = None
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        myAccount=Account.GetInfor(username)
        if(len(myAccount)!=1):
            error = '用户名或密码错误'
        else:
            myAccount=myAccount[0]
            AccountSHAPassword=myAccount[2]     #初始设计account表中第三列为加密后的密码
            SHA_password=GetSHA(password)
            if (AccountSHAPassword!=SHA_password):
                error = '用户名或密码错误'
            else:
                privilege = myAccount[3]
                session['username']=username
                session['login']=True
                session['privilege']=privilege
                return redirect(url_for('introduction'))

    if session.get('login') and session.get('username') and session.get('privilege'):
        return redirect(url_for('introduction'))
    else:
        session.clear()

    return render_template('login.html', error=error)

###################################################################################################
@app.route(introduction_url)
def introduction():
    #检查cookie是否为登录状态
    if (not (session.get('login') and session.get('username') and session.get('privilege'))):
        return redirect(url_for('logout'))

    username=session['username']
    p=session['privilege']
    sidebar=GetSideBar(GetBar(p))
    return render_template('introduction.html',username=username,sidebar=sidebar)

###################################################################################################
@app.route(myinformation_url, methods=['GET', 'POST'])
def myinformation():
    # 检查cookie是否为登录状态
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

###################################################################################################
@app.route(changeinformation_url, methods=['GET', 'POST'])
def changeinformation():
    Infor=SQL_Infor(get_db())
    Account=SQL_Account(get_db())
    # 检查cookie是否为登录状态
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))
    if(request.method=="POST"):
        myjson = json.loads(request.get_data())
        result={'status':''}
        username = myjson['username']
        oldpassword = myjson['oldpassword']

        if not(Account.CheckPassword(username,oldpassword)):
            result['status']="原密码错误"
            return jsonify(result)

        newpassword=myjson['newpassword']
        if(newpassword!=""):
            if(Account.UpdateAccount(username,newpassword)==1):
                result['status']="修改密码成功\n"
            else:
                result['status'] = "修改密码失败\n"

        sex=myjson['sex']
        born=myjson['born']
        telephone=myjson['telephone']
        if(Infor.UpdateInfor(username,telephone,sex,born)==1):
                result['status'] += "修改信息成功"
        else:
            result['status'] += "修改信息失败"

        return jsonify(result)



    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p))

    user = { "telephone": "",'sex': "无", 'born': "2000.1.1"}
    userinfor=Infor.GetInfor(username)
    if(len(userinfor)!=1):
        pass
    else:
        myinfor=userinfor[0]
        user['telephone']=myinfor[1]
        user['sex']=myinfor[2]
        user['born']=myinfor[3]

    return render_template("changeinformation.html",username=username,sidebar=sidebar,start=start,user=user)


###################################################################################################
@app.route(logout_url)
def logout():
    session.clear()
    return redirect(url_for('login'))


#===============================================页面==============================================#
#《《《《《《《《《《《《《《《《《《《《《《《《一点方法》》》》》》》》》》》》》》》》》》》》》》》》#
def GetBar(privilege):  #根据用户privilege返回不同的sidebar
    if(privilege==3):
        return adminbar
    elif(privilege==2):
        return teacherbar
    elif(privilege==1):
        return studentbar


# 《《《《《《《《《《《《《《《《《《《《《《《《小方法》》》》》》》》》》》》》》》》》》》》》》》》#
#...............................................main..............................................#
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)


