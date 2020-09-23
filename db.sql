
USE abc;
CREATE TABLE if not exists users(username VARCHAR(50) NOT NULL PRIMARY KEY, email VARCHAR(50),password VARCHAR(50),name VARCHAR(50),rollno TEXT(50),branch VARCHAR(50),hostelname VARCHAR(100),roomno VARCHAR(50),mobileno TEXT(100));

CREATE TABLE if not exists complaints(complaint_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(100), subject TEXT,category TEXT,time_of_availability VARCHAR(100),uergency TEXT,details text);

CREATE TABLE if not exists suggetions(suggetion_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(100), subject TEXT,category TEXT,details text);
