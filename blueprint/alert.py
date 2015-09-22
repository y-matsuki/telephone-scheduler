# -*- coding: utf-8 -*-
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from passlib.apps import custom_app_context as pwd_context

from common import db

import sys, traceback, hashlib
import common, pymongo, json

bp_alert = Blueprint('bp_alert', __name__,
                template_folder='templates')

@bp_alert.route('')
def alert():
    if 'username' in session:
        alerts = list(db.alerts.find().sort('Timestamp', pymongo.DESCENDING))
        for alert in alerts:
            if 'TopicArn' in alert:
                alert['TopicArnHash'] = hashlib.md5(alert['TopicArn']).hexdigest()
        return render_template('alerts.html', alerts=alerts)
    return redirect('/home')


@bp_alert.route('', methods=['POST'])
def add_alert():
    json_data = json.loads(request.data)
    if 'Type' in json_data:
        if json_data['Type'] == 'SubscriptionConfirmation':
            subscribe_url = json_data['SubscribeURL']
            print(subscribe_url)
            return dumps('ok')
        if json_data['Type'] == 'Notification':
            del json_data['MessageAttributes']
    print(json.dumps(json_data))
    try:
        db.alerts.insert(json_data)
    except:
        print "Exception in user code:"
        traceback.print_exc(file=sys.stdout)

    return dumps('ok')


@bp_alert.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id=None):
    if 'username' in session and session['is_admin'] and alert_id != None:
        alert = db.alerts.find_one({"_id":ObjectId(alert_id)})
        if alert:
            db.alerts.delete_one(alert)
    alerts = list(db.alerts.find())
    return render_template('alerts.html', alerts=alerts)
