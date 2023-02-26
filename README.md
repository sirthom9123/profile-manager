# Weather Forecast

#### Framework

Built with Django.

#### Libraries

API Used:

- Mapbox (Geolocation coordinates)

## Instructions to get API credentials for Mapbox

- Go to Mapbox https://www.mapbox.com/ and create a developer account
- After registration, create a key (it's free) and add it to your env file.

#### Database
- Postgresql
To install on your machine (Windows/Mac/Linux) follow the link for instructions: https://www.postgresql.org/download/

Command To Execute on Windows:

## Installation

Run `python -m venv venv` to create a virtual environment for the project

Run `venv/Scripts/activate` to activate the virtual environment

Run `pip install -r requirements.txt` to install the dependencies

## Run

### Command to migrate database

Run `python manage.py makemigrations` to make new migrations to db
Run `python manage.py migrate` to migrate to db

### Command to create a superuser

Run `python manage.py createsuperuser`

### Command To Execute on Windows:

Then Run `python manage.py runserver` to start live server on a new shell

## Access Site locally

Add `http://127.0.0.1:8000/` to the URL in the address bar

## Access Admin

Add `http://127.0.0.1:8000/admin` to the URL in the address bar

### Pytest

- Install Library: `pip install pytest-django`
- Make sure you have a pytest.ini file that will identify all test files

- Powershell Run: `$ENV:PYTHONPATH = "<name-of-project>"`
- Linux/Mac to set the environment path `export PYTOHNPATH=<name-of-project>`

Then run `pytest` for simple test summary or `pytest -vv` for detailed test summary
