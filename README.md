# Password Manager

This projects aims to build a web-based passoword manager. A pasword manager (From now on, PM) is an application that permits users store their credentials in a secure fashion without the need of remembering each one of their passwords. The PM can be acceded by the user using a master password (The only credential that the user must remember), and then he can either add more entries to his/her vault or query their credentials to use them in the site the want.

## Project Requirements

A PM has certain standard requirements that we must address in order to succesfully deploy a trusthworty application.

### Functional requirements

1. Web interface: The application must have a web interface where the users can access their dedicated password managers.
2. Automatic clipboard: The application must copy the desired password directly to the user's clipboard to avoid showing the password and forcing the user to manually copy it.
3. Password autogeneration: The application must provide a way to generate standarized secure passwords for the websites.

### Non-Functional requirements:

1. Consistency: The data transmitted across the application and the end-user must remain intact.
2. Reliability: The information must be securely stored within the application's database.
3. Security: The application must manage user's information carefully, and all security standards must be in place to avoid data leaks.
4. Portability: The application must be accesible through any web browser.

## Security concerns

A web-based PM has a particular sets of security concerns that we must have in mind before diving into the development and deployment.

### Password storage

epa

### Password hashing and password salting

epa

### Server security

epa

### Authentication methods

epa

### Thrustworthy (Browser crypto egg-and-chicken problem)

epa

## Tech-stack

The following technology will be used to build the application.

### Backend

For its ease of use, the backend will be built mainly in Python. Some libraries like crypto will be used to address cryptography concerns. The Database Management System (DBMS) choosen for this project will be MySQL, which will be used to store the credentials in the authentication methods and in to store the user's credentials.

### Frontend

The Frontend will be developed using Typescript to ensure consistency and reduce bugs in the application.

### Command Line

The application will provide access via CLI, using a secure channel, like SSH.
