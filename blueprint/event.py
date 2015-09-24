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

@bp_event.route('/clear')
def clear_event():
    result = db.events.drop()
    return jsonify({'status': 'ok'})


@bp_event.route('')
def event():
    insert_today()
    users = list(db.users.find({'is_admin': True}).sort('order'))
    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    # get start and end date from query parameter
    start_date_str = request.args.get('start', '2015-08-31')
    end_date_str = request.args.get('end', '2015-09-30')
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    # get last event
    events = list(db.events.find().sort('start', pymongo.DESCENDING).limit(1))
    last_user_name = events[0]['title']
    last_event_date = datetime.strptime(events[0]['start'], "%Y-%m-%d")
    events = []
    while start_date < end_date:
        item = db.events.find_one({'start': start_date.strftime('%Y-%m-%d')})
        if item:
            # current_date <= today
            item['color'] = 'gray'
            events.append(item)
            last_user_name = item['title']
        elif last_event_date < start_date:
            # today < current_date
            user = non_scheduled_next_user(users, start_date, last_user_name)
            events.append({
                'title': user['username'],
                'start': start_date.strftime('%Y-%m-%d'),
                'color': user['color']
            })
            last_user_name = user['username']
        start_date = start_date + timedelta(days=1)
    return dumps(events)


def today_users():
    '''
    本日の当番を主担当から３人選出する
    '''
    insert_today()
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


def insert_today():
    '''
    最後に登録されている当番から本日の当番までを生成する
    '''
    users = list(db.users.find({'is_admin': True}).sort('order'))
    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
    events = list(db.events.find().sort('start', pymongo.DESCENDING).limit(1))
    last_user_name = 'admin'
    last_event_date = datetime.strptime('2015-08-31', "%Y-%m-%d")
    if len(events) > 0:
        last_user_name = events[0]['title']
        last_event_date = datetime.strptime(events[0]['start'], "%Y-%m-%d")
    start_date = last_event_date + timedelta(days=1)
    while start_date < today:
        user = non_scheduled_next_user(users, start_date, last_user_name)
        event = {
            'title': user['username'],
            'start': start_date.strftime('%Y-%m-%d'),
            'color': user['color']
        }
        db.events.update_one({
            "start": start_date.strftime('%Y-%m-%d')
        }, {"$set": event}, upsert=True)
        start_date = start_date + timedelta(days=1)
        last_user_name = user['username']


def non_scheduled_next_user(users, date, last_user_name):
    '''
    指定された日付に予定の無い次のユーザを選出する
    '''
    scheduled_list = []
    while True:
        user = next_user(users, last_user_name)
        if len(scheduled_list) == len(users):
            break # 全員予定がある場合は元の次のメンバを設定
        if not has_schedule(user, date):
            break # 予定がない場合は予定がないメンバを設定
        scheduled_list.append(user)
        last_user_name = user['username']
    return user


def next_user(users, username):
    '''
    次のユーザを選出する
    '''
    for idx in xrange(len(users)):
        if users[idx]['username'] == username:
            break
    if idx + 1 == len(users):
        return users[0]
    return users[idx + 1]


def has_schedule(user, date):
    '''
    指定された日付に予定があるか判定する
    '''
    schedules = list(db.schedules.find({'user': user['username']}))
    if len(schedules) > 0:
        for schedule in schedules:
            if schedule['from_date'] <= date < schedule['to_date']:
                return True
    return False
