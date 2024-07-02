# Authentication module

This module serves the authentication service for the application.

## Purpose

Users that will use the application must authenticate in order to gain access to the password's database. They will rely on a Master Password that will be used to compare with the stored hashed version of that same password; if the hashed sent password matches the stored hashed password, we assume the user is how says he/she is.

## Implementation guide

Follow the instructions to set up the authentication service alone in a computer or server. You will need the following components:
- Linux as your host OS
- Docker installed
- A computer firewall like UFW
- MySQL DBSM in your host computer

Exectute `docker build -t auth_service .` to build your image. You can also download the image in [DockerHub](https://hub.docker.com/repository/docker/rodajrc/auth_service/general).

Once you have the docker image downloaded, run it with the following command:

```bash
docker run --network="host" -p 8000:8000 --name auths_service auth_service 
docker run -itd --network user_defined_bridge --name auth_service -p 8001:8001 -e MYSQL_HOST="127.0.0.1" -e MYSQL_USER="auth_user_docker" rodajrc/auth_service
```

This will instantiate the container using the network interface of your host machine. If you computer is in the cloud, you may need to change some configuration parameters in your firewall and MySQL DBSM.

Assuming you have UFW, use the following commands to ensure that your database is secure over the internet:

```bash
sudo ufw allow in on lo to any port 3306
sudo ufw deny 3306
```

Also, in MySQL configuration, you must need to change the parameter `bind-address` to allow connections from anywhere. To do that, chaange the value to `0.0.0.0`. The configuraion file of MySQL can be found in `/etc/mysql/mysql.conf.d/mysqld.cnf` or `/etc/mysql/my.cnf`. Also, be sure to have a user in MySQL with privileges across the network or from the network of your docker container.

## To do's

1. Delete account or data: Users may want to delete their information from the databases. In such case, we must give the users a way to retrieve all his/her stored passwords once we delete their user.

## Contributing guide

Remeber to set up a virtual environment when cloning the project. Use `python3 -m venv venv` to create a virtual environment and `pip install -r requirements.txt` to install the libraries and prerrequisites enlisted in the requirements.txt file. **If an error arises when installing the modules, look in the error message which module or library caused the error, and remove it from the `requirements.txt` file.**
Once you done the previous step, this module requires some secrets in order to run. Create a ``.env` file with the following lines:
```
MYSQL_USER='auth_user'
MYSQL_PASSWORD='auth_password'
MYSQL_DB='auth_database'
```
You will also need to have MySQL DBMS installed in your machine. There is a file called `init.sql` that you can use to set up the testing database and user.
Finally, run `python3 auth_service.py` or `pytest auth_service.py` to verify that everything is working fine! You shouldn't get any error.

## Comments

There is a problem called "The browser cypto chicken-and-egg". It would be interesting trying to solve or give a partial solution to this problem at least in the authentication module:
This [Stack Exhange post](https://security.stackexchange.com/questions/238441/solution-to-the-browser-crypto-chicken-and-egg-problem) explains pretty well the issue and provides a good framework to try solve the dilemma. However, this feature is not important righ now and we can leave it to the end.
