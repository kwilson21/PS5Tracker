# PS5Tracker

This is the PS5 Tracker server. The server is designed to handle retailer availabilities and auto purchasing a PS5.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Setting Up WSL

If you are a Windows user, I highly suggest setting up WSL and using Ubuntu as your OS. This is because some libraries that we use for this repo do not work in a Windows environment.

To set up WSL in Windows 10/11, follow these instructions to get WSL set up on your Windows machine: [Windows Subsystem for Linux Installation Guide for Windows 10](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

## Cloning the Repository

If you haven't already, you will need to clone the `kwilson21/PS5Tracker` GitHub repository to your local machine. This can be accomplished by running the following:

```bash
cd
mkdir repos
cd repos
git clone git@github.com:kwilson21/PS5Tracker.git
```

If you encounter an error at this point, it is likely you have not configured an SSH key with GitHub, to resolve this issue, see [Generating a new SSH key and adding it to GitHub](https://askubuntu.com/questions/527551/how-to-access-a-git-repository-using-ssh) for more details

## Setting Up Your Environment

Getting started with PS5Tracker, you will need to install Python version 3.9 or above.

You can get the latest version of Python for Windows/Mac here: https://www.python.org/downloads/

To install python 3.9 on Ubuntu, follow [How to install python3.9 on Ubuntu 20.04](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/) for instructions

You will also want to make sure that you have pip3 installed
```bash
sudo apt install python3.9-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py
```

It is HIGHLY recommended that you use pipenv when working on this repo.

Installing pipenv on Ubuntu

```bash
python3.9 -m pip install --user pipenv
```

Installing pipenv on Mac OS X

```bash
brew install pipenv
```

Otherwise use pip to install pipenv

```bash
py -m pip install --user pipenv
```

If pipenv isn't avaialble in your shell after installation, you'll need to add the user base's binary directory to your PATH. For more information, refer to the pipenv documentation here: [Pragmatic Installation of Pipenv](https://pipenv.kennethreitz.org/en/latest/install/#pragmatic-installation-of-pipenv)

## Install Required Packages

If you are using pipenv and are on a dev environment

```bash
cd ~/repos/PS5Tracker
pipenv install --dev
```

On a production environment

```bash
cd ~/repos/PS5Tracker
pipenv install
```

## Configuring Environment Variables

To configure your environment variables for this app, create a file called `.env` in the project root directory and set the following variables accordingly

```bash
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_NAME=test
DATABASE_USER=root
DATABASE_PASSWORD=1234
APP_ENV=development
```

### Pre commit

We have a configuration for
[pre-commit](https://github.com/pre-commit/pre-commit), to add the hook run the
following command:

```bash
pre-commit install
```

### Installing MySQL

To install MySQL on Windows, simply follow this links: [MySQL Installer 8.0.18](https://dev.mysql.com/downloads/installer/)

If you decide to set up WSL, I suggest using Ubuntu 20.04LTS for your flavor of linux. You can follow [this](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) guide to setup mysql-server on Ubuntu or follow my instructions below

Once you have Ubuntu installed on your Windows machine, open a bash terminal

To install MySQL on Ubuntu

```bash
sudo apt install mysql-server
```

After installation, start the MySQL server:

```bash
sudo service mysql start
```

After installing, run the security script with `sudo`

```bash
sudo mysql_secure_installation
```

This will take you through a series of prompts where you can make some changes to your MySQL installation’s security options. The first prompt will ask whether you’d like to set up the Validate Password Plugin, which can be used to test the password strength of new MySQL users before deeming them valid.

Lastly, before running the app, you must create the database that you will use

```bash
sudo mysql -u root -p
mysql> CREATE DATABASE test;
```

If you are getting permission denied errors in the app when trying to connect to the db using root, use the following command to fix the issue (set the password to whatever you like)

```bash
sudo myswl -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';
```

### Installing Redis

You will need to install Redis to test RQ jobs and test retailer availability code

```bash
sudo apt install redis-server
```

After installation, start the redis server:

```bash
sudo service redis-server start
```

## Running the App

Once your development environment is set up, you are now ready to run the app and start developing.

Start the webserver

```bash
cd ~/repos/PS5Tracker
pipenv shell
uvicorn run:app --reload
```

Start the RQ worker

```bash
cd ~/repos/PS5Tracker
pipenv shell
python run-worker-default.py
```

Start RQ scheduler

```bash
cd ~/repos/PS5Tracker
pipenv shell
rqscheduler
```
