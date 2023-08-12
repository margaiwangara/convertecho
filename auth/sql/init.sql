CREATE USER 'johndoe'@'localhost' IDENTIFIED BY 'JohnDoe123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* to 'johndoe'@'localhost';

USE auth;

CREATE TABLE users (id iNT NOT NULL AUTO_INCREMENT PRIMARY KEY, email VARCHAR(100) NOT NULL UNIQUE, password varchar(255) NOT NULL);

INSERT INTO users (email, password) VALUES ('johndoe@convertecho.com', 'JohnDoe111');