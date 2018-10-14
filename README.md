# API Base

A very simple API base framework made with Flask.

## Getting Started

### Prerequisites

- Python3
- Pipenv

### Installing

```
$ git clone git@bitbucket.org:keisukefd/api_base.git
$ cd api_base/
$ # If needed pre-install the right python version from your system, example:
$ # pipenv --python /usr/local/Cellar/python/3.6.5_1/bin/python3
$ pipenv install
```

### Configuration

```
configs/
|- default.py
|- development.py
|- production.py
```

##### Run migration
```
$ pipenv shell
$ python model.py db upgrade
```

##### Runing dev
```
$ pipenv shell
$ export FLASK_ENV=development
$ flask run
or
$ python app.py
```

##### Seeds
```
$ pipenv shell
$ # Must run migration first.
$ python model.py seed
```

### Built with
- [Flask](http://flask.pocoo.org/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-Json-Schema](https://github.com/sanjeevan/flask-json-schema)
- [JsonWebToken](https://jwt.io/)
