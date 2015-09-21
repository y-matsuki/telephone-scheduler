# telephone-scheduler

- https://devcenter.heroku.com/articles/getting-started-with-python-o

## Run local

```
mongod --dbpath data/mongo

virtualenv venv
source venv/bin/activate

pip install Flask Flask-Session gunicorn passlib pymongo

heroku local
```
