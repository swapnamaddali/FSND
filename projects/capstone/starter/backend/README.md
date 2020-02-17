## Getting Started

### Project Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle postgres database.
Models are defined in  `./src/models.py` which will create the needed migrations.

- [auth] (https://auth0.com) Auth0 is used for validating users JWT token and
providing access accordingly. A custom @requires_auth decorator is used for
getting the authorization from request header and validating the token and permissions.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Run :
Environment variables required for the app (auth and database) are created and maintained
in `./src/setup.sh` file. Running the below command after the virtual env is started
will allow it to set the values in environment.

source setup.sh

```bash
python app.py
```
this will start the local server at 127.0.0.1:5000/

```
## Testing
To run the tests, run
```
dropdb capstone_test
create database capstone_test
psql capstone_test < capstone.psql
    OR (psql -U postgres -d capstone_test -1 -f capstone.psql)
        Path of /FSND/projects/capstone/starter/backend/src/capstone.psql
python test_app.py (Need to execute this the environment created for the project)
```
