#!/usr/bin/python3
from flask import Flask, request, session,redirect, url_for,render_template,g,jsonify
from flask_cors import CORS
from Config import Config
from Config.Link_db import *
from SQL_libarary.SQL_Account import *
from SQL_libarary.SQL_Infor import *
from SQL_libarary.SQL_Course import *
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
select_url=myconfig.getvalue(route_section,"select")
addcourse_url=myconfig.getvalue(route_section,"addcourse")
course_url=myconfig.getvalue(route_section,"course")
logout_url=myconfig.getvalue(route_section,"logout")


studentbar={'查看个人信息':myinformation_url,'我的课程':course_url,'选课':select_url}
teacherbar={'查看个人信息':myinformation_url,'我的课程':course_url,'创建课程':addcourse_url}
adminbar={'查看个人信息':myinformation_url,'我的课程':course_url,'创建课程':addcourse_url}


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
    infor=SQL_Infor(get_db())
    # 检查cookie是否为登录状态
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p),'查看个人信息')

    user={'privilege':p,'sex':'未填写','telephone':'未填写','born':'未填写'}
    userinfor = infor.GetInfor(username)
    if (len(userinfor) != 1):
        pass
    else:
        myinfor = userinfor[0]
        user['telephone'] = myinfor[1]
        user['sex'] = myinfor[2]
        user['born'] = myinfor[3]

    return render_template('myinformation.html', username=username, sidebar=sidebar,user=user)

###################################################################################################
@app.route(changeinformation_url, methods=['GET', 'POST'])
def changeinformation():
    Infor=SQL_Infor(get_db())
    Account=SQL_Account(get_db())
    # 检查cookie是否为登录状态
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    if(request.method=="POST"):
        result = {'status': ''}
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)

        myjson = json.loads(request.get_data())
        username = myjson['username']
        oldpassword = myjson['oldpassword']
        caozuo=myjson['caozuo']

        if not(Account.CheckPassword(username,oldpassword)):
            result['status']="原密码错误"
            return jsonify(result)
        if(caozuo=='password'):
            newpassword=myjson['newpassword']
            if(newpassword!=""):
                Account.UpdateAccount(username,newpassword)
                result['status']="修改密码成功"
                return jsonify(result)
        else:
            sex=myjson['sex']
            born=myjson['born']
            telephone=myjson['telephone']
            Infor.UpdateInfor(username,telephone,sex,born)
            result['status'] = "修改信息成功"
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
@app.route(course_url, methods=['GET', 'POST'])
def course():
    Course= SQL_Course(get_db())

    if (request.method == "POST"):
        result = {'status': ''}
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data())
        caozuo=myjson['caozuo']
        if(caozuo=="test"):
            userid=myjson['userid']
            testname=myjson['testname']
            score=myjson['score']
            mycourse1=myjson['course']
            Course.changetestscore(userid,mycourse1,testname,score)
            result['status'] = "更新成功"
        elif(caozuo=="score"):
            userid=myjson['userid']
            score = myjson['score']
            mycourse1 = myjson['course']
            Course.changescore(userid, mycourse1, score)
            result['status'] = "更新成功"
        elif(caozuo=="add"):
            testname=myjson['testname']
            mycourse1 = myjson['course']
            Course.addtest(testname,mycourse1)
            result['status'] = "更新成功"
        return jsonify(result)


    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '我的课程')

    if(p==1):
        mycourse=Course.SearchCourse_1(username)
    elif(p==2):
        mycourse=Course.SearchCourse_2(username)
    elif(p==3):
        mycourse=Course.SearchCourse_3()
    else:
        return redirect(url_for('logout'))

    xcourse=request.args.get('course','')
    seek=False
    if(len(mycourse)!=0):
        for i in mycourse:
            if(i['name']==xcourse):
                seek=True
                break
    if(seek==False):
        return render_template("course.html", username=username, sidebar=sidebar, mycourse=mycourse)
    else:
        if(p==1):
            infor=Course.Course_Infor(xcourse,username)
            return render_template("mycourse.html",username=username,sidebar=sidebar,infor=infor)
        else:
            infor=Course.Course_Score(xcourse)
            infor['name']=xcourse
            return render_template("course_teacher.html",username=username,sidebar=sidebar,course=infor)

###################################################################################################
@app.route(addcourse_url, methods=['GET', 'POST'])
def addcourse():
    Account=SQL_Account(get_db())
    Course=SQL_Course(get_db())

    if (request.method == "POST"):
        result = {'status': ''}
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        elif((session.get('privilege')!=2)and(session.get('privilege')!=3)):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data())
        print(myjson)
        username=myjson['username']
        coursename=myjson['course']
        seek=Course.addcourse(coursename,username)
        if(seek!=False):
            result['status']="增加成功"
        else:
            result['status']="该名称已存在"
        return jsonify(result)

    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '创建课程')
    if(p==1):
        return redirect(url_for('select'))
    elif(p==2):
        return render_template("addcourse.html",username=username,sidebar=sidebar,p=p)
    elif(p==3):
        teachers=Account.getAllbyPrivilege(2)
        return render_template("addcourse.html", username=username, sidebar=sidebar,p=p,teachers=teachers)


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


