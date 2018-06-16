drop table if exists account;
drop table if exists course;
drop table if exists log;
drop table if exists infor;
drop table if exists sqlite_sequence;


CREATE TABLE "account" ( 
`userid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 `username` string NOT NULL,
 `password` string NOT NULL, 
 `privilege` int NOT NULL 
 );
 CREATE TABLE "log" ( 
 `logid` int NOT NULL, 
 `userid` string NOT NULL,
 `operation` string,
 `time` string,
 PRIMARY KEY(`logid`) 
 );
CREATE TABLE "infor"(
'userid' int not null,
 'telphone' string not null,
 'sex' string not null,
 'born' string not null );
 CREATE TABLE "course"( 
 'courseid' INTEGER not null PRIMARY KEY AUTOINCREMENT, 
 'teacherid' int, 'name' string not null, 
 'term' string not null, 
 'time' string not null );