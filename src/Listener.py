#!/usr/bin/python3
from flask import Flask, request, session,redirect, url_for,render_template,g,jsonify,send_from_directory,abort
from flask_cors import CORS
from Config import Config
from Config.Link_db import *
from SQL_libarary.SQL_Account import *
from SQL_libarary.SQL_Infor import *
from SQL_libarary.SQL_Course import *
from SQL_libarary.Func_lib import *
from werkzeug.utils import secure_filename
import json
import os

#---------------------------------------------全局配置--------------------------------------------#
#全局变量配置
myconfig=Aconfig()

#Flask app 相关配置
flask_section="flask"
app=Flask(__name__)
app.config.update(dict(SECRET_KEY=myconfig.getvalue(flask_section,"SECRET_KEY")))   #保存session的密钥
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
account_url=myconfig.getvalue(route_section,"account")
resource_url=myconfig.getvalue(route_section,"resource")
download_url=myconfig.getvalue(route_section,"download")
delete_url=myconfig.getvalue(route_section,"delete")
forget_url=myconfig.getvalue(route_section,"forget")
super_url=myconfig.getvalue(route_section,"super")

#用户sidebar设置
studentbar={'查看个人信息':myinformation_url,'我的课程':course_url,'选课':select_url,'资源':resource_url}
teacherbar={'查看个人信息':myinformation_url,'我的课程':course_url,'创建课程':addcourse_url,'资源':resource_url}
adminbar={'查看个人信息':myinformation_url,'我的课程':course_url,'创建课程':addcourse_url,
          '用户管理':account_url,'资源':resource_url,'高级管理员选项':super_url}

maxshow=5   #翻页最大展示数
pageoffset=9    #每页最大展示数
UPLOAD_PATH='./documents/'  #上传目录
ALLOWED_EXTENSIONS=set(['txt', 'png', 'jpg', 'xls', 'JPG',
                        'PNG', 'xlsx', 'gif', 'GIF','doc','docx','ppt','pptx','rar','zip','pdf'])   #允许的文件的扩展名
start="1950,1,1"    #日历最早日期
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
#登录界面，允许所有人
@app.route('/')
@app.route(login_url, methods=['GET', 'POST'])
def login():
    Account=SQL_Account(get_db())   #获取Account方法集
    error = None
    if request.method == 'POST':    #若为post方法，即用户进行登录操作
        username=request.form['username']
        password=request.form['password']
        myAccount=Account.GetInfor(username)    #查询是否有这个用户
        if(len(myAccount)!=1):
            error = '用户名或密码错误'
        else:
            myAccount=myAccount[0]
            AccountSHAPassword=myAccount[2]     #拿到密码
            SHA_password=GetSHA(password)       #对密码进行sha加密
            if (AccountSHAPassword!=SHA_password):  #对密码进行判断
                error = '用户名或密码错误'
            else:
                privilege = myAccount[3]
                session['username']=username
                session['login']=True
                session['privilege']=privilege      #session 保存用户状态
                return redirect(url_for('introduction'))    #成功则进入introduction页面
    # 检查cookie是否为登录状态
    if session.get('login') and session.get('username') and session.get('privilege'):
        return redirect(url_for('introduction'))
    else:
        session.clear()

    return render_template('login.html', error=error)

###################################################################################################
#介绍界面，允许所有登录用户
@app.route(introduction_url)
def introduction():
    #检查cookie是否为登录状态
    if (not (session.get('login') and session.get('username') and session.get('privilege'))):
        return redirect(url_for('logout'))

    username=session['username']
    p=session['privilege']
    sidebar=GetSideBar(GetBar(p))   #对sidebar进行处理

    return render_template('introduction.html',username=username,sidebar=sidebar,p=p)
###################################################################################################
#我的信息，允许所有登陆用户
@app.route(myinformation_url, methods=['GET', 'POST'])
def myinformation():
    infor=SQL_Infor(get_db())   #获取infor方法集
    # 检查cookie是否为登录状态
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p),'查看个人信息')    #对sidebar进行处理

    user={'privilege':p,'sex':'未填写','telephone':'未填写','born':'未填写'} #user数据初始化
    userinfor = infor.GetInfor(username)    #根据用户名获取其信息
    if (len(userinfor) != 1):
        pass
    else:
        myinfor = userinfor[0]
        user['telephone'] = myinfor[1]
        user['sex'] = myinfor[2]
        user['born'] = myinfor[3]   #对user进行处理

    return render_template('myinformation.html', username=username, sidebar=sidebar,user=user,p=p)
###################################################################################################
#修改个人信息，允许所有用户
@app.route(changeinformation_url, methods=['GET', 'POST'])
def changeinformation():
    Infor=SQL_Infor(get_db())   #获取infor方法集
    Account=SQL_Account(get_db())   #获取account方法集

    # 检查cookie是否为登录状态
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    if(request.method=="POST"): #ajax操作
        result = {'status': ''}
        #检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)

        myjson = json.loads(request.get_data()) #获取页面发来的json
        username = myjson['username']
        oldpassword = myjson['oldpassword']
        caozuo=myjson['caozuo']

        if not(Account.CheckPassword(username,oldpassword)):    #对密码进行检查
            result['status']="原密码错误"
            return jsonify(result)
        if(caozuo=='password'):     #修改密码的操作
            newpassword=myjson['newpassword']
            if(newpassword!=""):
                Account.UpdateAccount(username,newpassword)
                result['status']="修改密码成功"
                return jsonify(result)
        else:
            sex=myjson['sex']
            born=myjson['born']
            telephone=myjson['telephone']
            Infor.UpdateInfor(username,telephone,sex,born)  #对infor表进行更新
            result['status'] = "修改信息成功"
            return jsonify(result)



    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p))

    user = { "telephone": "",'sex': "无", 'born': "2000.1.1"}
    userinfor=Infor.GetInfor(username)  #获取用户信息
    if(len(userinfor)!=1):
        pass
    else:
        myinfor=userinfor[0]
        user['telephone']=myinfor[1]
        user['sex']=myinfor[2]
        user['born']=myinfor[3]

    return render_template("changeinformation.html",username=username,sidebar=sidebar,start=start,user=user,p=p)

###################################################################################################
#course页面，允许所有用户
@app.route(course_url, methods=['GET', 'POST'])
def course():
    Course= SQL_Course(get_db())    #获取course方法集

    if (request.method == "POST"):  #ajax方法
        result = {'status': ''}
        # 检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data()) #获取json
        caozuo=myjson['caozuo']
        if(caozuo=="test"):     #修改test的分数
            userid=myjson['userid']
            testname=myjson['testname']
            score=myjson['score']
            if not (score.isdigit()):   #对score进行验证是否为数字
                result['status'] = "分数应为数字"
                return jsonify(result)
            if(float(score)>100) or (float(score)<0):   #限制score范围
                result['status'] = "分数应处于0~100"
                return jsonify(result)
            mycourse1=myjson['course']
            Course.changetestscore(userid,mycourse1,testname,score) #更新test的score
            result['status'] = "更新成功"
        elif(caozuo=="score"):  #修改综合分数
            userid=myjson['userid']
            score = myjson['score']
            if not (score.isdigit()):   #对score进行验证是否为数字
                result['status'] = "分数应为数字"
                return jsonify(result)
            if (float(score) > 100 )or (float(score)<0):    #限制score范围
                result['status'] = "分数应处于0~100"
                return jsonify(result)
            mycourse1 = myjson['course']
            Course.changescore(userid, mycourse1, score)     #更新score
            result['status'] = "更新成功"
        elif(caozuo=="add"):    #增加一个test
            testname=myjson['testname']
            mycourse1 = myjson['course']
            Course.addtest(testname,mycourse1)
            result['status'] = "更新成功"
        elif(caozuo=="tuike"):      #退课
            username=myjson['username']
            course=myjson['course']
            Course.tuike(username,course)
            result['status'] = "退课成功"
        elif(caozuo=="delete"):     #删除学生
            username = myjson['username']
            course = myjson['course']
            Course.tuike(username, course)
            result['status'] = "退课成功"
        elif(caozuo=="change"):     #修改课程信息
            oldname=myjson['oldname']
            newname=myjson['newname']
            time=myjson['time']
            intro=myjson['intro']
            Course.changecourse(oldname,newname,time,intro)
            result['status'] = "更新成功"
        elif(caozuo=="student"):    #增加学生
            username = myjson['username']
            course = myjson['course']
            sentence=Course.addstudent(username,course)
            result['status'] = sentence
        return jsonify(result)

    #检查session
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '我的课程')

    #根据权限和用户名获取对应课程
    if(p==1):
        mycourse=Course.SearchCourse_1(username)
    elif(p==2):
        mycourse=Course.SearchCourse_2(username)
    elif(p==3):
        mycourse=Course.SearchCourse_3()
    else:
        return redirect(url_for('logout'))

    #根据url中course参数获取课程名
    xcourse=request.args.get('course','')
    seek=False
    if(len(mycourse)!=0):
        for i in mycourse:
            if(i['name']==xcourse):
                seek=True
                break

    if(seek==False):    #若课程名不存在则返回course.html
        data=None
        if(p==3):
            infor = Course.GetAllCourseInfor()
            page=request.args.get('p',1)
            data=GetPageDict(page,infor, pageoffset , maxshow)
        return render_template("course.html", username=username, sidebar=sidebar,data=data, mycourse=mycourse,p=p)
    else:       #若课程名存在则返回mycourse.html或course_teacher.html
        if(p==1):
            infor=Course.Course_Infor(xcourse,username)
            return render_template("mycourse.html",username=username,sidebar=sidebar,infor=infor,p=p)
        else:
            page=request.args.get('p',1)
            infor=Course.Course_Score(xcourse)
            x=Course.courseBYname(xcourse)
            infor['name']=xcourse
            infor['time']=x['time']
            infor['intro']=x['intro']
            infor['teacher']=x['teacher']
            data=GetPageDict(page,infor['student'],pageoffset - 2, maxshow)
            return render_template("course_teacher.html",username=username,sidebar=sidebar,course=infor,p=p,data=data)
###################################################################################################
#创建课程，仅允许教师和管理员
@app.route(addcourse_url, methods=['GET', 'POST'])
def addcourse():
    Account=SQL_Account(get_db())
    Course=SQL_Course(get_db())

    if (request.method == "POST"):  #ajax方法
        result = {'status': ''}
        #检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        elif((session.get('privilege')!=2)and(session.get('privilege')!=3)):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data()) #获取json
        username=myjson['username']
        coursename=myjson['course']
        introduction=myjson['introduction']
        time=myjson['time']
        seek=Course.addcourse(coursename,username,introduction,time)    #增加课程
        if(seek!=False):
            result['status']="增加成功"
        else:
            result['status']="该名称已存在"
        return jsonify(result)

    #检查session
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '创建课程')
    if(p==1):   #若权限为学生则送至选课
        return redirect(url_for('selectcourse'))
    elif(p==2):
        return render_template("addcourse.html",username=username,sidebar=sidebar,p=p)
    elif(p==3):
        teachers=Account.getAllbyPrivilege(2)
        return render_template("addcourse.html", username=username, sidebar=sidebar,p=p,teachers=teachers)
###################################################################################################
#选课界面
@app.route(select_url, methods=['GET', 'POST'])
def selectcourse():
    Course=SQL_Course(get_db())
    if (request.method == "POST"):  #ajax方法
        result = {'status': ''}
        #检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        elif(session.get('privilege')!=1):  #仅允许学生进行操作
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data()) #获取json
        username=myjson['username']
        course=myjson['course']
        status=Course.selectcourse(username,course)
        if(status==False):
            result['status'] = "该课程已选过"
            return jsonify(result)
        else:
            result['status'] = "选课成功"
            return jsonify(result)

    #检查session
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '选课')

    if(p!=1):   #若不为学生则送至创建课程
        return redirect(url_for("addcourse"))

    #根据url获取课程名
    xcourse=request.args.get("course","")
    if(xcourse==""):    #若课程名不存在则展示课程列表
        courses=Course.SearchCourse_3()
        mycourse=Course.SearchCourse_1(username)
        mycourselist=[]
        for i in mycourse:
            mycourselist.append(i['name'])

        return render_template("selectcourse.html", username=username, sidebar=sidebar, p=p, courses=courses,mycourse=mycourselist)
    else:   #若课程名存在则展示课程信息
        mycourse = Course.SearchCourse_1(username)
        mycourselist = []
        for i in mycourse:
            mycourselist.append(i['name'])
        courseinfor=Course.courseBYname(xcourse)
        if(courseinfor!=False):
            return render_template("courseinfor.html", username=username, sidebar=sidebar, p=p,course=courseinfor,mycourse=mycourselist)
        else:
            return redirect(url_for("selectcourse"))
###################################################################################################
#用户管理，仅允许管理员
@app.route(account_url, methods=['GET', 'POST'])
def account():
    Infor=SQL_Infor(get_db())
    Account=SQL_Account(get_db())

    if (request.method == "POST"):  #ajax方法
        result = {'status': ''}
        #检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        elif(session.get('privilege')!=3):  #仅允许管理员操作
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data()) #获取json
        caozuo=myjson['caozuo']
        username = myjson['username']
        sex = myjson['sex']
        born = myjson['born']
        telephone = myjson['telephone']
        if(caozuo=='change'):   #修改信息
            Infor.UpdateInfor(username,telephone,sex,born)
            password=myjson['password']
            if(password!=""):
                Account.UpdateAccount(username,password)
            result['status'] = "更新成功"
        elif(caozuo=='delete'): #删除用户
            privilege=myjson['privilege']   #根据权限删除用户
            if(int(privilege)==1):
                if (Infor.DeleteAll_student(username)):
                    result['status'] = "删除成功"
                else:
                    result['status'] = "删除失败"
            elif(int(privilege)==2):
                if (Infor.DeleteAll_teacher(username)):
                    result['status'] = "删除成功"
                else:
                    result['status'] = "删除失败"
        elif(caozuo=='add'):    #增加用户
            if(len(Account.GetInfor(username))!=0): #检查是否存在用户名
                result['status'] = "此用户名已存在"
                return jsonify(result)
            privilege=int(myjson['privilege'])
            password = myjson['password']
            if(password==""):
                password="123456"
            if(Infor.InsertInfor(username,password,telephone,sex,born,privilege)):
                result['status'] = "增加成功"
            else:
                result['status'] = "增加失败"
        return jsonify(result)


    #检查session
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '用户管理')
    page= request.args.get('p', 1)  #根据url获取第几页
    privilege=request.args.get('privilege','1')
    if(p!=3):
        return redirect(url_for("introduction"))

    if(privilege=="2"):
        user=Infor.GetUserBYprivilege(2)
    else:
        user = Infor.GetUserBYprivilege(1)
    data=GetPageDict(page,user, pageoffset - 2, maxshow)    #对翻页进行处理


    return render_template("account.html",username=username,p=p,sidebar=sidebar,data=data,start=start,privilege=privilege)
###################################################################################################
#资源页面，允许所有登陆用户
@app.route(resource_url, methods=['GET','POST'], strict_slashes=False)
def resource():
    Course=SQL_Course(get_db())
    #检查session
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '资源')

    if (p == 1):
        mycourse = Course.SearchCourse_1(username)
    elif (p == 2):
        mycourse = Course.SearchCourse_2(username)
    elif (p == 3):
        mycourse = Course.SearchCourse_3()
    else:
        return redirect(url_for('logout'))

    #获取url中的course参数
    course = request.args.get('course', '')
    if(course=="") or (not checkcourse(course, mycourse)):  #检查course是否存在，不存在则返回选择课页面
        return render_template("course_1.html", username=username, sidebar=sidebar, mycourse=mycourse, p=p)

    #获取url中的file_dir参数
    file_dir1 = request.args.get('file_dir','')
    file_dir = UPLOAD_PATH + course + "/"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)   #若该课程未有文件夹则创建
    file_dir = file_dir + file_dir1
    try:
        allfileset = getAllFile(file_dir)   #获取目录下所有文件和文件夹
    except:
        return render_template("course_1.html", username=username, sidebar=sidebar, mycourse=mycourse, p=p)

    #获取url中的page
    page = int(request.args.get("p", 1))
    mydata=GetPageDict(page, allfileset, pageoffset - 2, maxshow)   #对数据和翻页进行处理

    if request.method == 'POST':    #文件上传
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        if request.files.__contains__('file'):
            try:
                f = request.files["file"]
                if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
                    oldfilename=f.filename
                    fname = secure_filename(f.filename)
                    ext = getEXT(fname)  # 获取文件后缀
                    noextfname=getFilename(oldfilename)
                    nowfname=noextfname+"."+ext
                    while(True):    #检车是否存在同文件名，存在则在该文件后加(1)
                        dict1={'fname':nowfname,'leixing':'文件'}
                        if not dict1 in allfileset:
                            break
                        else:
                            noextfname = getFilename(nowfname)
                            nowfname=noextfname+"(1)"+"."+ext
                    new_filename = nowfname  # 修改了上传的文件名
                    f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
                    msg = fname+' 上传成功'
                else:
                    msg = '为禁止文件类型或上传失败'
            except:
                msg = '上传失败'
        else:
            msg = '上传失败'
        return render_template('resource.html', data=mydata,msg=msg,mydir=file_dir1,username=username,p=p,sidebar=sidebar,course=course)


    return render_template('resource.html',data=mydata,mydir=file_dir1,username=username,p=p,sidebar=sidebar,course=course)
###################################################################################################
#下载，允许所有登陆用户
@app.route(download_url, methods=['GET','POST'])
def download():
    Course = SQL_Course(get_db())
    #检查session
    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))

    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '资源')
    course = request.args.get('course', "")

    if (p == 1):
        mycourse = Course.SearchCourse_1(username)
    elif (p == 2):
        mycourse = Course.SearchCourse_2(username)
    elif (p == 3):
        mycourse = Course.SearchCourse_3()
    else:
        return redirect(url_for('logout'))
    #检查url中的course是否有效
    if (course == "") or (not checkcourse(course, mycourse)):
        return render_template("course_1.html", username=username, sidebar=sidebar, mycourse=mycourse, p=p)
    #获取文件目录
    file_dir=request.args.get('file_dir',"")
    if(file_dir==""):
        abort(404)

    filename=getFile(file_dir)
    dir1=dir(file_dir)
    dir1=UPLOAD_PATH+course+'/'+dir1
    if request.method=="GET":
        if os.path.isfile(os.path.join(dir1, filename)):
            return send_from_directory(dir1,filename,as_attachment=True)
        abort(404)
###################################################################################################
#删除和创建文件夹，仅允许教师和管理员
@app.route(delete_url, methods=['POST'])
def delete():
    Course = SQL_Course(get_db())
    if (request.method == "POST"):
        result = {'status': ''}
        #检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        elif(session.get('privilege')!=3) and (session.get('privilege')!=2):    #对权限进行核查
            result['status'] = "请刷新浏览器"
            return jsonify(result)

        username = session['username']
        p = session['privilege']

        if (p == 1):
            mycourse = Course.SearchCourse_1(username)
        elif (p == 2):
            mycourse = Course.SearchCourse_2(username)
        elif (p == 3):
            mycourse = Course.SearchCourse_3()
        else:
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson = json.loads(request.get_data()) #获取json
        caozuo=myjson['caozuo']
        course=myjson['course']
        file_dir = myjson['file_dir']
        if not checkcourse(course, mycourse):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        if(caozuo=='delete'):   #删除文件
            filename=getFile(file_dir)
            dir1=dir(file_dir)
            dir1=UPLOAD_PATH+course+dir1
            newdir=dir1+'/'+filename
            if os.path.exists(newdir):
                if(os.path.isfile(newdir)): #判断是否为文件
                    os.remove(newdir)
                elif(os.path.isdir(newdir)):    #判断是否为文件夹
                    os.rmdir(newdir)
                result['status'] = "删除成功"
                return jsonify(result)
        elif(caozuo=='folder'): #创建文件夹
            dir1 = UPLOAD_PATH + course + '/' +file_dir
            os.makedirs(dir1)
            result['status'] = "创建成功"
            return jsonify(result)
###################################################################################################
#忘记密码，允许所有人
@app.route(forget_url,methods=['GET','POST'])
def forget():
    Account=SQL_Account(get_db())
    Infor=SQL_Infor(get_db())
    if (session.get('login') or session.get('username') or session.get('privilege')):   #清除session
        session.clear()
    check=None
    error=None
    username=None
    if not (session.get('check')):  #check不存在时则进入输入用户名的界面
        session.clear()
        if (request.method == "POST"):
            username=request.form['username']
            myinfor=Account.GetInfor(username)
            if(len(myinfor)==0):    #判断是否存在用户
                error='用户名不存在'
            else:
                session['check']=1
                check=1
        return render_template('forget.html',error=error,check=check,username=username,start=start)
    elif(session['check']==1):  #check为1的时候则进入验证用户信息的界面
        if (request.method == "POST"):
            username = request.form['username']
            myinfor = Infor.GetInfor(username)
            if (len(myinfor) == 0):
                error = '用户名不存在'
                check=None
                session.pop('check')
            else:   #核查信息
                myinfor=myinfor[0]
                telephone=request.form['telephone']
                born=request.form['born']
                if(myinfor[1]==int(telephone))and (myinfor[3]==born):
                    check=2
                    session['check']=2
                else:
                    check=1
                    session['check']=1
                    error='信息不正确'
        return render_template('forget.html', error=error, check=check, username=username,start=start)
    elif(session['check']==2):  #check为2时进入输入新密码的界面
        if (request.method == "POST"):
            username = request.form['username']
            myinfor = Infor.GetInfor(username)
            if (len(myinfor) == 0):
                error = '用户名不存在'
                check=None
                session.pop('check')
            else:
                password1=request.form['password1']
                password2 = request.form['password2']
                if(password1==password2):
                    Account.UpdateAccount(username,password1)
                    check=3
                    session['check']=3
                else:
                    error='两次密码不一致'
                    check=2
                    session['check']=2
        return render_template('forget.html', error=error, check=check, username=username,start=start)
###################################################################################################
#超级管理员选项，仅允许管理员
@app.route(super_url, methods=['POST','GET'])
def super():
    Account=SQL_Account(get_db())
    if (request.method == "POST"):  #ajax操作
        result = {'status': ''}
        #检查session
        if not (session.get('login') and session.get('username') and session.get('privilege')):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        elif(session.get('privilege')!=3):
            result['status'] = "请刷新浏览器"
            return jsonify(result)
        myjson=json.loads(request.get_data())   #获取json
        username=myjson['username']
        password=myjson['password']
        caozuo=myjson['caozuo']
        if(caozuo=='resetdatabase'):
            #重置数据库
            if(Account.CheckPassword(username,password)):
                if(Account.reset()):
                    result['status'] = "重置数据库完成"
                    return jsonify(result)
                else:
                    result['status'] = "重置数据库失败"
                    return jsonify(result)
            else:
                result['status'] = "密码错误"
                return jsonify(result)


    if not (session.get('login') and session.get('username') and session.get('privilege')):
        return redirect(url_for('logout'))
    username = session['username']
    p = session['privilege']
    sidebar = GetSideBar(GetBar(p), '高级管理员选项')

    if(p!=3):
        return redirect(url_for('logout'))

    return render_template("super.html", username=username, sidebar=sidebar, p=p)


###################################################################################################
#登出
@app.route(logout_url)
def logout():
    session.clear() #清除session
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


#查看是否为允许后缀的文件
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 《《《《《《《《《《《《《《《《《《《《《《《《小方法》》》》》》》》》》》》》》》》》》》》》》》》#
#...............................................main..............................................#
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=False)


