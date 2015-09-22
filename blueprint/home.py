# -*- coding: utf-8 -*-
import pymongo
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime, date

from common import db
from event import non_scheduled_next_user

bp_home = Blueprint('bp_home', __name__,
                    template_folder='templates')

@bp_home.route('')
def home():
    if 'username' in session:
        return render_template('home.html', today_users=today_users())
    else:
        return render_template('login.html')


def today_users():
    users = list(db.users.find({'is_admin': True}).sort('order'))
    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    events = list(db.events.find().sort('start', pymongo.DESCENDING).limit(1))
    last_user_name = 'admin'
    if len(events) > 0:
        last_user_name = events[0]['title']
    today_users = []
    for idx in xrange(3):
        user = non_scheduled_next_user(users, today, last_user_name)
        if user not in today_users:
            today_users.append(user)
        last_user_name = user['username']
    return today_users
