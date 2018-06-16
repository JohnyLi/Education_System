drop table if exists account;
drop table if exists course;
drop table if exists log;
drop table if exists infor;
drop table if exists sqlite_sequence;
CREATE TABLE IF NOT EXISTS `log` (
	`logid`	int NOT NULL,
	`userid`	string NOT NULL,
	`operation`	string,
	`time`	string,
	PRIMARY KEY(`logid`)
);
CREATE TABLE IF NOT EXISTS `infor` (
	`userid`	int NOT NULL,
	`telphone`	string NOT NULL,
	`sex`	string NOT NULL,
	`born`	string NOT NULL
);
INSERT INTO `infor` VALUES (1,18118760884,'男','1996.12.16');
INSERT INTO `infor` VALUES (2,19999999999,'男','1950.11.13');
CREATE TABLE IF NOT EXISTS `course` (
	`courseid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`teacherid`	int,
	`name`	string NOT NULL,
	`term`	string NOT NULL,
	`time`	string NOT NULL
);
CREATE TABLE IF NOT EXISTS `account` (
	`userid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`username`	string NOT NULL,
	`password`	string NOT NULL,
	`privilege`	int NOT NULL
);
INSERT INTO `account` VALUES (1,'admin','d033e22ae348aeb5660fc2140aec35850c4da997',3);
INSERT INTO `account` VALUES (2,'李狗蛋','7c4a8d09ca3762af61e59520943dc26494f8941b',1);
INSERT INTO `account` VALUES (4,'詹姆斯','7c4a8d09ca3762af61e59520943dc26494f8941b',2);

