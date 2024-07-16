import os
from dotenv import load_dotenv

"""
Configuration parameters provided by system environment variables. There are
default values in case those envs were not initialized.

+ MYSQL_USER: [STRING] The user that can access the MySQL database for authentication.
+ MYSQL_PASSWORD: [STRING] The password for MYSQL_USER.
+ MYSQL_HOST: [STRING] IP, hostname, or domain of the device where the database is allocated.
+ MYSQL_PORT: [STRING] Port atwhich MySQL.service is running.
+ MYSQL_DB: [STRING] Database where user's information will be stored.
"""
load_dotenv()
config = {
    'MYSQL_USER': os.getenv('MYSQL_USER'),
    'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
    'MYSQL_HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
    'MYSQL_PORT': os.getenv('MYSQL_PORT', '3306'),
    'MYSQL_DB': os.getenv('MYSQL_DB')
}
