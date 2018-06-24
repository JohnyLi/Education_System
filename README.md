![Sustech](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/sustech.png)
# Education_System
## 项目介绍
* 我们的项目名叫 Education System。
* 包含的功能有：权限管理、用户修改个人信、管理员修改用户信息、测试分数发布、选课系统、课程资源等。
* 测试样例部署在 119.29.231.205，访问http://119.29.231.205 即可。
## 功能简介
<strong>这是一个教学服务平台，该服务平台分为三个主要用户服务功能。权限分为了三级，学生、教师和管理员。</strong>

* 学生有以下权限：<br/>
1.查看个人信息：查看及修改个人信息 <br/>
2.我的课程：已选课程分数的分数查看 <br/>
3.选课<br/>
4.资源：已选课程的资源查看与下载<br/>

* 教师有以下权限：<br/>
1.	查看个人信息：查看及修改个人信息<br/>
2.	我的课程：已添加课程的test添加、课程信息修改、学生增删及其分数的查询和修改<br/>
3.	创建课程：新建一个课程，包括执教教师、开课时间、课程介绍等信息<br/>
4.	资源：课程文件的增删改查<br/>

* 管理员有以下权限：<br/>
1.	查看个人信息：查看及修改个人信息<br/>
2.	我的课程：已添加课程的test添加、课程信息修改、学生增删及其分数的查询和修改<br/>
3.	创建课程：新建一个课程，包括执教教师、开课时间、课程介绍等信息<br/>
4.	用户管理：老师学生用户的增删及信息的修改<br/>
5.	资源：课程文件的增删改查<br/>
6.	高级管理员选项：重置数据库<br/>

## 项目工具
* 语言：![Python 3.6](https://www.python.org/downloads/release/python-365/)
* Web 框架：![Flask](http://flask.pocoo.org/)
* 数据库：![sqlite3](https://www.sqlite.org/index.html)

## 快速部署
* 环境配置<br/>
![Python 3.6](https://www.python.org/downloads/release/python-365/) 安装及配置系统环境。
* 依赖下载 <br/>
- $ cd Eduction_System
- $ python -m pip install -r requirements.txt
* 运行 <br/>
- $ cd Eduction_System/src
- $ python Listener.py
<strong>运行后将监听0.0.0.0的80端口。</strong>

* 运行截图<br/>
运行后将看到类似下图的代码行。<br/>

![运行截图](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/run.png)

## 文件目录
<p>-src						（source 文件夹）</p>
<p>|-=Config				（config 文件夹）</p>
<p>|-config.ini	 		（配置文件）</p>
<p>|-Config.py			（获取配置文件中的配置的方法）</p>
<p>|-Link_db.py			（数据库的连接）</p>
<p>|-=documents			（存放各课程的资源）</p>
<p>|-=SQL_libarary			（存放sql操作方法的文件夹）</p>
<p>|-Func_lib.py			（存放杂乱的方法）</p>
<p>|-SQL_Account.py	（主要对Account表进行操作的方法的集类）</p>
<p>|-SQL_Course.py		（主要对Course类表进行操作的方法的集类）</p>
<p>|-SQL_Infor.py		（主要对Infor表进行操作的方法的集类）v
<p>|-=static				（static 文件夹）</p>
<p>|-=css				（存放css文件）</p>
<p>|-=database			（存放数据库与sql文件）</p>
<p>|-=js				（存放js文件）</p>
<p>|-=pic				（存放图片）</p>
<p>|-=templates			（存放html文件）v
<p>-Listener.py				（运行本程序）</p>

## 数据库设计
* 数据库用的是Sqlite3
### 表设计
* account （保存用户账号信息）<br/>
	userid 用户ID（自增）[int]<br/>
	username 用户名	[string]<br/>
	password 密码（经过Sha不可逆加密）[string]<br/>
	privilege 权限 （1为学生，2为教师，3为管理员）[int]<br/>

![account表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/account.png)
* infor	（保存用户资料）<br/>
	userid 用户ID （与account相连） [int]<br/>
	telephone 电话号码	[string]<br/>
	sex 性别 [string]<br/>
	born 出生日期 （yyyy.mm.dd）[string]<br/>
![infor表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/infor.png)
* log	（日志）<br/>
	logid 日志ID （自增） [int]<br/>
	userid 用户ID （与account相连） [int]<br/>
	operation 操作名 [string]<br/>
	time 时间 [string]<br/>
![log表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/log.png)
* course	（课程基本信息）<br/>
	courseid 课程ID （自增） [int]<br/>
	teacherid 教师ID （与account相连） [int]<br/>
	name 课程名 [string]<br/>
	term 学期  [string]<br/>
	time 授课时间 [string]<br/>
	intro 课程介绍 [string]<br/>
![course表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/coursetable.png)
* student_course	（学生选的课及其综合分数）<br/>
	courseid 课程ID （与course相连） [int]<br/>
	studentid 学生ID （与account的userid相连） [int]<br/>
	score 该学生课程综合分数 [float]
![student_course表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/student_course.png)

* student_test	（学生选的课的test和分数）<br/>
	testid  testID （与test_course相连）[int]<br/>
	studentid 学生ID （与account的userid相连）  [int]<br/>
	score 分数  [float]
![student_test表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/student_test.png)

* test_course	（课程的test信息）<br/>
	testid testID (自增) [int]<br/>
	coursed 课程ID （与course相连）  [int]<br/>
	testname test的名字 [string]
![test_course表](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/test_course.png)







## 项目部分截图




