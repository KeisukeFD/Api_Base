# API Base

A very simple API base framework made with Flask.

## Getting Started

### Prerequisites

- Python3.8
- virtualenv

### Installing

```
$ git clone git@bitbucket.org:keisukefd/api_base.git
$ cd api_base/
$ pip install -r requirements.txt
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
$ python model.py db stamp head
$ python model.py db migrate
$ python model.py db upgrade
```

##### Runing dev
```
$ export FLASK_ENV=development
$ flask run
or
$ python app.py
```

##### Seeds
```
$ # Must run migration first.
$ python model.py seed
```

### Built with
- [Flask](http://flask.pocoo.org/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-Json-Schema](https://github.com/sanjeevan/flask-json-schema)
- [JsonWebToken](https://jwt.io/)
