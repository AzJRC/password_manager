
/* You may want to replace '%' with the ip of the container or server that will hold the MySQL Database */
/* You may want to replace 'auth_user_password' with a different passphrase to enforce security*/
/* Remember that if you change any of the user's parameters that defines it, you will need to add or provide the
   corresponding new values to your sever via environment variables, or if using Docker, pass the credentials as
   needed.*/

CREATE USER IF NOT EXISTS 'pwdmgr_admin'@'%' IDENTIFIED BY 'pwdmgr_admin_password';
GRANT ALL PRIVILEGES ON pwdmgr.* TO 'pwdmgr_admin'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS pwdmgr;
USE pwdmgr;

CREATE TABLE IF NOT EXISTS vaults (	
	vault_id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS vault_entries (
	entry_id INT AUTO_INCREMENT PRIMARY KEY,
       	vault_id INT REFERENCES vaults(vault_id),
	service_name VARCHAR(255) NOT NULL,
	encrypted_password TEXT NOT NULL
);

