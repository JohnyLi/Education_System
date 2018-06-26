![Sustech](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/sustech.png)
# Education_System
## 项目介绍
* 我们的项目名叫 Education System。
* 包含的功能有：权限管理、用户修改个人信、管理员修改用户信息、测试分数发布、选课系统、课程资源等。
* 测试样例部署在 119.29.231.205，访问http://119.29.231.205 即可。
* 提供账户: 
学生 用户名：科比 密码：123456 <br/>
	    教师 用户名：汪峰 密码：123456 <br/>
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

## 功能实现原理阐述
### Web 监听
* 本程序运用了Flask框架。
![web](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/web.png)

* 只需在方法前加上装饰器并指定路径即可。
### html页面获取数据及执行运算
* Flask中用的是jinja2表达式
* 例如下图我在/introduction中返回了模板introduction.html。
![fig1](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/html1.png) 
<br/>fig1<br/>
![fig2](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/html2.png)
<br/>fig2<br/>
![fig3](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/html3.png)
<br/>fig3<br/>
![fig4](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/html4.png)
<br/>fig4<br/>
![fig5](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/html5.png)
<br/>fig5<br/>
* 可以看到图2是对p进行运算，即可根据p的值做出相应展示。
* 图3中可以获得username的值。
* 图4是在layout.html中加入了一个body，就可以令其他html页面选择继承其页面。
* 图5是在introduction.html中，继承了layout.html，返回时就可以直接获取到layout.html的其他部分代码并拼接。

### 用户状态
* 本程序中主要用Cookies来保存用户状态。
* Flask中提供了一种session的cookies，可以根据程序密钥对cookies进行可逆加密，即可以实现将用户状态保存至cookies中且用户只可删除无法修改。
* 在登录成功后，程序将会上传session保存至cookies，如下图。<br/>

![fig1](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/user1.png)

* 然后在除了登录页面之外的页面，每次访问都会对cookies进行检查 <br/>

![fig2](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/user2.png)

* 三个session，缺一不可，缺少一个则送至logout清除cookies然后回到login。这样有效的防止了未登录却可以对教务系统进行访问的事故。
* 在某些只允许高级用户前进的页面或者操作，将对其session中的privilege进行进一步核查，以防低级用户访问高级用户进行危险操作。

### 数据库连接与线程优化
* 为了防止每次对数据库操作都要连接一次数据库浪费资源，用了以下方法避免并保证每条线程单一连接。
* Flask 提供了一种g的对象，g对象和访问一一对应。
* 在下图中，设计了一个get_db()方法和close_db()的方法。

![fig1](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/database.png)

* 在某些需要操作数据库的页面方法中，会先执行get_db()获取数据库连接。
* close_db()对在页面方法上下文结束后执行，即若g对象中存在数据库连接则对其进行关闭。

### 数据库操作
* 对数据库进行操作的页面需要执行get_db()获取连接对象。然后通过该连接对象创建需要的SQL_libarary中的对象。SQL_libarary中不对数据库进行连接，仅包含对数据库进行操作的sql语句与执行的方法，所以需要获得连接对象。
* 例如下图中登录页面需要对Account表进行查询。首先通过数据库连接对象创建Account对象，然后根据账号密码并加密然后对表中进行查询操作。
<br/>

![fig1](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/database1.png)

![fig2](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/database2.png)


### 页面操作执行
* 在本程序中，页面一般使用表单和ajax进行post操作。
* 例如在用户管理页面，图一和图二，修改用户信息时用的是ajax。服务器会对其信息进行处理并返回一个json包含了status。返回后页面就会alert出status的值。一般是成功或者失败。
* 再例如在上传资源时，图三，用的是表单。服务器会处理上传文件并返回新页面包含是否成功的信息。

![fig1](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/caozuo1.png)
<br/>fig1<br/>
![fig2](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/caozuo2.png)
<br/>fig2<br/>
![fig3](https://raw.githubusercontent.com/JohnyLi/MyPicture/master/Education_System/caozuo3.png)
<br/>fig3<br/>




## 项目部分截图




