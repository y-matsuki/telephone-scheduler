# -*- coding: utf-8 -*-
from bson.json_util import dumps
from flask import request, redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify, session
from datetime import datetime

from common import db

bp_home = Blueprint('bp_home', __name__,
                    template_folder='templates')

@bp_home.route('')
def home():
    if 'username' in session:
        next_user = db.users.find_one({'username':session['username']})
        print(next_user)
        return render_template('home.html', next_user=next_user)
    else:
        return render_template('login.html')
