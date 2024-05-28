# Authentication module

This module serves the authentication service for the application.

## Purpose

Users that will use the application must authenticate in order to gain access to the password's database. They will rely on a Master Password that will be used to compare with the stored hashed version of that same password; if the hashed sent password matches the stored hashed password, we assume the user is how says he/she is.

## To do's

1. Sign up: There isn't a way yet to allow users register to the authentication database.
2. Delete account or data: Users may want to delete their information from the databases. In such case, we must give the users a way to retrieve all his/her stored passwords once we delete their user.
3. Secure credential storage: Altough the main module workflow already works, the information stored in the database isn't considering any sort of security.

## Contributing guide

Remeber to set up a virtual environment when cloning the project. Use `python3 -m venv venv` to create a virtual environment and `pip install -r requirements.txt` to install the libraries and prerrequisites enlisted in the requirements.txt file. **If an error arises when installing the modules, look in the error message which module or library caused the error, and remove it from the `requirements.txt` file.**
Once you done the previous step, this module requires some secrets in order to run. Create a ``.env` file with the following lines:
```
MYSQL_USER='auth_user'
MYSQL_PASSWORD='Auth-2357'
MYSQL_DB='auth'
```
You will also need to have MySQL DBMS installed in your machine. There is a file called `init.sql` that you can use to set up the testing database and user.
Finally, run `python3 auth_service.py` or `pytest auth_service.py` to verify that everything is working fine! You shouldn't get any error.

## Comments

There is a problem called "The browser cypto chicken-and-egg". It would be interesting trying to solve or give a partial solution to this problem at least in the authentication module:
This [Stack Exhange post](https://security.stackexchange.com/questions/238441/solution-to-the-browser-crypto-chicken-and-egg-problem) explains pretty well the issue and provides a good framework to try solve the dilemma. However, this feature is not important righ now and we can leave it to the end.
