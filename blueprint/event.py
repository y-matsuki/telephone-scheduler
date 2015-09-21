# -*- coding: utf-8 -*-
import re, copy
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime, timedelta

from common import db

bp_event = Blueprint('bp_event', __name__,
                    template_folder='templates')
users = list(db.users.find())
schedules = list(db.schedules.find())

@bp_event.route('')
def event():
    start_date_str = request.args.get('start', '2015-09-01')
    end_date_str = request.args.get('end', '2015-09-30')
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # TODO get latest event
    user = users[0]

    events = []
    while start_date < end_date:
        user = next_user(start_date, user['username'])
        events.append({
            'title': user['username'],
            'start': start_date.strftime('"%Y-%m-%d"'),
            'color': user['color']
        })
        start_date = start_date + timedelta(days=1)
    return dumps(events)


def next_user(start_date, username):
    copy_user = remove_scheduled_user(copy.copy(users))
    for idx in xrange(len(copy_user)):
        if copy_user[idx]['username'] == username:
            break
    if idx + 1 == len(copy_user):
        return copy_user[0]
    return copy_user[idx + 1]

def remove_scheduled_user(users):
    # TODO implement
    return users
