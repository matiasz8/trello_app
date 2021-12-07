# trello_app


# Setup

At the begining, install dependencies:

    $ pip install pipenv
    $ pipenv install
    
And then, activate the venv:

    $ pipenv shell

Ensure that your *PYTHONPATH* is being set:

    $ export PYTHONPATH=$PWD

### Environment file

Create an .env file on project root, and add this keys:

    TRELLO_APP_KEY="xcvxgxd5g5d54xdg45xdg5454xdg54"
    TRELLO_APP_TOKEN="54sef54sef454s5ef54a45ef45aef546s"



# Start up

To start the project, run:

    $ python app/main.py

To run test, execute:

    $ pytest

To check linters:

    pre-commit run --all-files
