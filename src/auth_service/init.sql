CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED BY 'Auth-2357';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS auth;
USE auth;
CREATE TABLE IF NOT EXISTS auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

INSERT INTO auth (username, email, password) VALUES ('testuser', 'testuser@gmail.com', '1234');

