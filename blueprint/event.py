# -*- coding: utf-8 -*-
import re, copy, pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime, timedelta, date

from common import db

bp_event = Blueprint('bp_event', __name__,
                    template_folder='templates')

@bp_event.route('')
def event():
    users = list(db.users.find({'is_admin': True}))

    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), "%Y-%m-%d")

    start_date_str = request.args.get('start', '2015-09-01')
    end_date_str = request.args.get('end', '2015-09-30')
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # get last event
    events = list(db.events.find().sort('start', pymongo.DESCENDING).limit(1))
    last_user_name = 'admin'
    last_event_date = datetime.strptime('2015-09-01', "%Y-%m-%d")
    if len(events) > 0:
        last_user_name = events[0]['title']
        last_event_date = datetime.strptime(events[0]['start'], "%Y-%m-%d")
    events = []
    while start_date < end_date:
        item = db.events.find_one({'start': start_date.strftime('%Y-%m-%d')})
        if item:
            item['color'] = 'teal'
            events.append(item)
        elif last_event_date < start_date:
            while True:
                user = next_user(users, last_user_name)
                if not has_schedule(user, start_date):
                    break
                last_user_name = user['username']

            print str(start_date) + ': ' + user['username']

            event = {
                'title': user['username'],
                'start': start_date.strftime('%Y-%m-%d')
            }
            event['color'] = user['color']
            if start_date < today:
                # insert
                db.events.update_one({
                    "start": start_date.strftime('%Y-%m-%d')
                }, {"$set": event}, upsert=True)
                event['color'] = 'gray'
            events.append(event)
            last_user_name = user['username']
        start_date = start_date + timedelta(days=1)
    return dumps(events)


def next_user(users, username):
    for idx in xrange(len(users)):
        if users[idx]['username'] == username:
            break
    if idx + 1 == len(users):
        return users[0]
    return users[idx + 1]


def has_schedule(user, date):
    schedules = list(db.schedules.find({'user': user['username']}))
    if len(schedules) > 0:
        for schedule in schedules:
            if schedule['from_date'] <= date <= schedule['to_date']:
                return True
    return False
