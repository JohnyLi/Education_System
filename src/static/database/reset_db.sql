
DROP TABLE IF EXISTS `test_course`;
CREATE TABLE IF NOT EXISTS `test_course` (
	`testid`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`courseid`	int NOT NULL,
	`testname`	string NOT NULL
);

DROP TABLE IF EXISTS `student_test`;
CREATE TABLE IF NOT EXISTS `student_test` (
	`testid`	int NOT NULL,
	`studentid`	int NOT NULL,
	`score`	float
);

DROP TABLE IF EXISTS `student_course`;
CREATE TABLE IF NOT EXISTS `student_course` (
	`courseid`	int NOT NULL,
	`studentid`	int NOT NULL,
	`score`	float
);

DROP TABLE IF EXISTS `log`;
CREATE TABLE IF NOT EXISTS `log` (
	`logid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`userid`	string NOT NULL,
	`operation`	string,
	`time`	string
);

DROP TABLE IF EXISTS `infor`;
CREATE TABLE IF NOT EXISTS `infor` (
	`userid`	int NOT NULL,
	`telephone`	string NOT NULL,
	`sex`	string NOT NULL,
	`born`	string NOT NULL
);
INSERT INTO `infor` VALUES (1,18118760884,'男','1996.12.16');

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
	`courseid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`teacherid`	int,
	`name`	string NOT NULL,
	`term`	string,
	`time`	string,
	`intro`	string
);

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
	`userid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`username`	string NOT NULL,
	`password`	string NOT NULL,
	`privilege`	int NOT NULL
);


