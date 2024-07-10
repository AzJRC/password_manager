
/* You may want to replace '%' with the ip of the container or server that will hold the MySQL Database */
/* You may want to replace 'auth_user_password' with a different passphrase to enforce security*/
/* Remember that if you change any of the user's parameters that defines it, you will need to add or provide the
   corresponding new values to your sever via environment variables, or if using Docker, pass the credentials as
   needed.*/

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
