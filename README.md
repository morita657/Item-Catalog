# Item Catalog

This project is part of the Full Stack Web Developer nanodegree from udacity. The project utilizes the [Full Stack Foundations](https://classroom.udacity.com/courses/ud088) and [Authentication and Authorization](https://classroom.udacity.com/courses/ud330).

## Usage
Download this repository and run on your machine or go here


## The purpose of this project
Modern web applications perform a variety of functions and provide amazing features and utilities to their users; but deep down, it’s really all just creating, reading, updating and deleting data. In this project, I will combine my knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to my users.

## Prerequirements
This project requires Python 2.X (2.7.x is expected) and PostgreSQL 9.3 or latest version. [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) are required to run SQL database server and web app.

## How to run
1. Download or clone repository on you machine.
2. Bring the project directory under the vagrant directory.
3. Start the virtual machine `vagrant up` and `vagrant ssh`.
4. Go to `cd /vagrant/project` directory.
5. Run database with `python finalProjectDatabase_setup.py`
6. Run `python finalProject.py` to build web app.
7. Shutdown the VM with `CTRL + D`.
8. Don't forget `vagrant halt` to power off VirtualBox.

## Code Quality
[Here](https://google.github.io/styleguide/pyguide.html) is the Google Python Style Guide that I followed.
