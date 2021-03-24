# Login - Hackathon 2021

# Installation

## Clone the repository to your local machine

First, you will have to clone the repository:
```
git clone https://github.com/KelianB/tab-gen.git
cd tab-gen/backend
```

Make sure you are on the main branch, otherwise you can change your branch with the following command:
```
git checkout main
```

Also check that you have Python 3 with a version above 3.6.

## Creation of virtual environments

### Windows 

Before proceeding, make sure to install a Redis server (or a clone), and to launch it.

To create a virtual environment for the project, run the following command:
```
python -m venv venv
```
Once installed, you can activate it as follows:
* Command Prompt
```
venv\Scripts\activate.bat
```
* PowerShell
```
venv\Scripts\Activate.ps1
```
You should see ```(venv)``` before the path.

In the virtual environment, install the requirements:
```
python -m pip install -r requirements.txt
```

Go to the perfectpeach folder:
```
cd perfectpeach
```

Then, follow the steps in **Initialisation of the database** if necessary.

From there, 2 additional commands need to run in this directory at the same time as the server. This can be done by opening 2 new terminals (referred here as **a** and **b**) in the same directory (meaning the folder we're inside is ```perfectpeach```) and running each command in one of the terminals:
* Terminal **a**
```
celery -A perfectpeach beat -l info
```
* Terminal **b**
```
celery -A perfectpeach worker -l info
```

To run the server, in the original terminal, use:
```
python manage.py runserver
```

When you are done, you can leave the virtual environment with the command:
```
deactivate
```

### Linux 

Before proceeding, make sure that virtual environments can be created on your system. You may need to install an additional package before being able to, such as ```python3-venv``` on Debian-based systems.
Please also install a Redis server and launch it. Usually, once installed, it can be done by simply running ```redis-server```.

To create a virtual environment for the project, run the following command:
```
python3 -m venv venv
```
Once installed, you can activate it as follows:
```
source venv/bin/activate
```

In the virtual environment, install the requirements:
```
python -m pip install -r requirements.txt
```

Go to the perfectpeach folder:
```
cd perfectpeach
```

Then, follow the steps in **Initialisation of the database** if necessary.

From there, 2 additional commands need to run in this directory at the same time as the server. This can be done by opening 2 new terminals (referred here as **a** and **b**) in the same directory (meaning the folder we're inside is ```perfectpeach```) and running each command in one of the terminals:
* Terminal **a**
```
celery -A perfectpeach beat -l info
```
* Terminal **b**
```
celery -A perfectpeach worker -l info
```

To run the server, in the original terminal, use:
```
python manage.py runserver
```

When you are done, you can leave the virtual environment with the command:
```
deactivate
```

## Initialisation of the database

Note : this is not necessary if the ```db.sqlite3``` already exists in the project folder.

First of all, the database needs to be initialized. To do so, run:
```
python manage.py migrate
```

To create a superuser which can access the admin panel, use:
```
python manage.py createsuperuser
```
Follow the instruction by choosing a username and a password (you can leave a blank e-mail address if you want).
