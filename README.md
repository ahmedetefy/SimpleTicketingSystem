# SimpleTicketingSystem
### Problem Description:

A simple ticketing system where anonymous allowed users are allowed to submit anonymous tickets. 

On the other hand, managers or employees can access the system by providing their username and password. Once authenticated, they are represented with a list of Tickets.
They can edit, delete or add comments to these tickets.

A system with these descriptions would require a backend API that recieves requests from a front end application,
and in return send data saved in models.

An API Backend is required to be stateless while the frontend is not.

### Solution Description:

For this application, I chose to use Python 2.7, Flask, SQLAlchemy and PostgreSQL for the backend application.

As for the frontend application, my choices were HTML, CSS and Javascript, Typescript. In a nutshell, Angular 4 and Bootstrap.

I am an adept Python Django and Django REST developer, but I chose to learn and develop Flask + SQLAlchemy for backend and Angular 4 for the first time during the 7 days allocated for the task for the following reasons:

* They match Byrd's Stack.

* I wanted to demonstrate to your prestigious company my ability to learn fast and adapt efficiently. These two qualities in my opinion are the most important and critical qualities a developer needs in the ever so fast changing and growing development community.

Tradeoffs:
-----------
All the mentioned features in the tasks are completed according to their expected functionality.

Due to shortage of time, a few of the views in the template are not mobile responsive, but I made sure to ensure that some of them are to demonstrate my frontend skills.

Additions:
-----------
I added the scaffolding for a Virtual Machine to assist in setting up and running the project.

I ensured that functions that require logged in users are protected on both the frontend and the backend sides for better security and error handling.

# Usage Directions

## Installations

### Backend

This project uses Vagrant for VM management. 

* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](http://downloads.vagrantup.com/).

### Frontend

This project uses NodeJS and Angular CLI.

* Install [NodeJS](https://nodejs.org/en/download/)
* Install AngularCLI using npm

```
$ npm install -g @angular/cli
```

## Instructions

### Backend
```
(1) Make sure your local host points to 0.0.0.0 on your machine

 $ echo "0.0.0.0 localhost" | sudo tee --append /etc/hosts

(2) Clone the repository

$ git clone https://github.com/ahmedetefy/SimpleTicketingSystem.git

(3) $ cd SimpleTicketingSystem/backend
(4) $ vagrant up
(5) $ vagrant ssh
(6) $ cd /vagrant/projects
(7) $ mkvirtualenv --quiet ticket
(8) $ cd flask-jwt-auth
(9) $ pip install -r requirements.txt
(10) $ export SECRET_KEY='my_precious'
(11) $ python manage.py create_db
(12) $ python manage.py db init
(13) $ python manage.py db migrate
(14) Run the tests and make sure they all pass

$python manage.py test

(15) Run populate script

$ python populate.py

(16) python manage.py runserver --host 0.0.0.0 --port 8000

```

### Frontend

```
(1) Open a different terminal and cd into frontend directory

$ cd SimpleTicketingSystem/frontend

(2) Install all dependencies 

$ npm build

(3) $ ng serve

(4) Finally visit localhost:4200 

```

### User Login Information

email: byrd@byrd.com

password: byrd
