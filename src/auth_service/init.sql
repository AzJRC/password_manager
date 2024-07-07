
/* Replace localhost with the ip of the container */
/* Replace auth_user_password with a personal password*/

CREATE USER IF NOT EXISTS 'auth_user_docker'@'%' IDENTIFIED BY 'auth_user_password';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user_docker'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS auth;
USE auth;
CREATE TABLE IF NOT EXISTS auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
