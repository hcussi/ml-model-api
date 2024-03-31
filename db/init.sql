Create DATABASE usersdb;
CREATE USER 'mlModelUser'@'%' IDENTIFIED BY 's3c3rTpaZZ';
GRANT ALL PRIVILEGES ON usersdb.* TO 'mlModelUser'@'%';
CREATE DATABASE testsdb;
GRANT ALL PRIVILEGES ON testsdb.* TO 'mlModelUser'@'%';
FLUSH PRIVILEGES;
