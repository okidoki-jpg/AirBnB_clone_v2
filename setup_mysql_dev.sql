--  dev SQL script to prepare MySQL server for project

-- create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- create user if it doesn't exist and set password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- grant all privileges to user hbnb_dev on hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- grant select privilege to user hbnb_dev on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- flush privileges to update MySQL's privilege cache
FLUSH PRIVILEGES;
