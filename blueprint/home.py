# -*- coding: utf-8 -*-
import pymongo
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime, date

from common import db
from event import today_users

bp_home = Blueprint('bp_home', __name__,
                    template_folder='templates')

@bp_home.route('')
def home():
    if 'username' in session:
        return render_template('home.html', today_users=today_users())
    else:
        return render_template('login.html')
