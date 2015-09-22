# telephone-scheduler

- https://devcenter.heroku.com/articles/getting-started-with-python-o

## Run local

```
mongod --dbpath data/mongo

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

heroku local
```

## Deploy to heroku

```
heroku login
heroku create
git push heroku master

heroku open
```

## MongoDB

```
heroku addons:create mongolab
heroku run python scripts/init_mongo.py
```

## Twilio setting

```
heroku config:set TWILIO_ACCOUNT_SID=AC00000000000000000000000000000000
heroku config:set TWILIO_AUTH_TOKEN=00000000000000000000000000000000
heroku config:set TWILIO_NUMBER=+815000000000
```
