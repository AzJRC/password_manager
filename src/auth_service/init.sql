CREATE USER IF NOT EXISTS 'auth'@'localhost' IDENTIFIED BY 'auth-2357';
GRANT ALL PRIVILEGES ON auth.* TO 'auth'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS auth;
USE auth;
CREATE TABLE IF NOT EXISTS auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

INSERT INTO auth (username, email, password) VALUES ('rodajrc', 'rodajrc@gmail.com', '1234');

