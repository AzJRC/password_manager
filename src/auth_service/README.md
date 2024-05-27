# Authentication module

This module serves the authentication service for the application.

## Purpose

Users that will use the application must authenticate in order to gain access to the password's database. They will rely on a Master Password that will be used to compare with the stored hashed version of that same password; if the hashed sent password matches the stored hashed password, we assume the user is how says he/she is.

## To do's:

1. Sign up: There isn't a way yet to allow users register to the authentication database.
2. Delete account or data: Users may want to delete their information from the databases. In such case, we must give the users a way to retrieve all his/her stored passwords once we delete their user.
3. Secure credential storage: Altough the main module workflow already works, the information stored in the database isn't considering any sort of security.

## Comments:

There is a problem called "The browser cypto chicken-and-egg". It would be interesting trying to solve or give a partial solution to this problem at least in the authentication module:
This [Stack Exhange post](https://security.stackexchange.com/questions/238441/solution-to-the-browser-crypto-chicken-and-egg-problem) explains pretty well the issue and provides a good framework to try solve the dilemma. However, this feature is not important righ now and we can leave it to the end.
