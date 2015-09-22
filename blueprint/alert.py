# -*- coding: utf-8 -*-
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from passlib.apps import custom_app_context as pwd_context

from common import db

import common, pymongo, json

bp_alert = Blueprint('bp_alert', __name__,
                template_folder='templates')

@bp_alert.route('')
def alert():
    if 'username' in session:
        alerts = list(db.alerts.find())
        return render_template('alerts.html', alerts=alerts)


@bp_alert.route('', methods=['POST'])
def add_alert():
    json_data = json.loads(request.data)
    print(json_data)
    db.alerts.insert(json_data)
    return dumps('ok')


@bp_alert.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id=None):
    if 'username' in session and session['is_admin'] and alert_id != None:
        alert = db.alerts.find_one({"_id":ObjectId(alert_id)})
        if alert:
            db.alerts.delete_one(alert)
    alerts = list(db.alerts.find())
    return render_template('alerts.html', alerts=alerts)