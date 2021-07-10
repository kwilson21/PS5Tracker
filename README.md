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

On Ubuntu, it is recommended that you use pyenv to manage your python versions

To install pyenv

```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Once you have pyenv installed, you will need to add pyenv to your path

```bash
echo -e 'if shopt -q login_shell; then' \
      '\n  export PYENV_ROOT="$HOME/.pyenv"' \
      '\n  export PATH="$PYENV_ROOT/bin:$PATH"' \
      '\n eval "$(pyenv init --path)"' \
      '\nfi' >> ~/.bashrc
echo -e 'if [ -z "$BASH_VERSION" ]; then'\
      '\n  export PYENV_ROOT="$HOME/.pyenv"'\
      '\n  export PATH="$PYENV_ROOT/bin:$PATH"'\
      '\n  eval "$(pyenv init --path)"'\
      '\nfi' >>~/.profile
```

Finally, source your profile to save the changes
```bash
source .profile
```

Install python 3.9.6 (to see other python versions you can install, use `pyenv install --list`)

```bash
pyenv install 3.9.6
```


Next, you will need to set your your repo directory to use python3.9 when in the directory
```bash
cd ~/repos/PS5Tracker
pyenv local 3.9.6
```

It is HIGHLY recommended that you use pipenv when working on this repo

```bash
python -m pip install --user pipenv
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
REDIS_HOST=localhost
REDIS_PORT=6379
APP_ENV=development
URL=https://example.com/
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TEST_EMAIL=test@test.com
TEST_PHONE_NUMBER=+15551234567
WEB_DRIVER=chrome
SECRET_KEY=
```

You can generate a secret key for your local environment using the following command
```bash
python -c "import os; print(os.urandom(24).hex())"
```

### Pre commit

We have a configuration for
[pre-commit](https://github.com/pre-commit/pre-commit), to add the hook run the
following command:

```bash
pre-commit install
```

### Installing MySQL

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
sudo mysql -u root -p
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

### Install Google Chrome and ChromeDriver

PS5Tracker's retailer services relies on Selenium to scrape PS5 availabilities from websites. To do this, it uses Chrome in headless mode. Because of this, we must ensure our environment has Google Chrome and Chromedriver installed so that Selenium can find them.

I created a script to make this process easy

```bash
cd ~/repos/PS5Tracker
sudo bash setup-chrome.sh
```

## Running the App

Once your development environment is set up, you are now ready to run the app and start developing.

Start the webserver

```bash
cd ~/repos/PS5Tracker
pipenv shell
honcho start
```

## Running a task

Once you have the app up and running, you can test out RQ by running a task

```python
from app.rq.jobs import update_retailer_availabilities
from app.constants import RQ_REDIS_CONN, TARGET_RETAILER
from rq import Queue

q = Queue(connection=RQ_REDIS_CONN)
q.enqueue(update_retailer_availabilities, args=[TARGET_RETAILER])
```

This task will get PS5 availabilities from the target website, and store the results in redis.

After updating retailer availabilities, you can query the API to get retailer availabilities by going to http://localhost:5000/docs

![FastAPI](https://i.imgur.com/ZqR1IWb.png)

## Deploying

The app is already pre-configured to be deployed using Heroku. You can check out their documentation for setting up a Python app [here](https://devcenter.heroku.com/articles/getting-started-with-python)
