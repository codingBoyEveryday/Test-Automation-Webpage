#!/usr/bin/python
# -*- coding: UTF-8 -*- 
"""Running IPIT WebServer."""

# import os
# import csv
# import xlsxwriter
# import re
#
# from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
# from flask import send_file
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


# from werkzeug.contrib.fixers import ProxyFix # Added 24-Aug for Gunicorn

from credential import is_valid_username
from credential import is_valid_password
from credential import is_valid_email
from credential import register_user


# Flask app definition
app = Flask(__name__)
# In order to use python functions in Jinja2, they must be declared here.
# app.jinja_env.globals.update(len=len)
# app.jinja_env.globals.update(enumerate=enumerate)
# app.jinja_env.globals.update(showNone=lambda s: "" if s is None else s)
# app.wsgi_app = ProxyFix(app.wsgi_app) # Added 24-Aug for Gunicorn


# ============================== Page Handlers of pages: main, signup, login, set password ==========================
@app.route('/home')
def home():
    """The handle for home page."""
    return render_template('home.html')


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     kwargs = dict(username='', email='', name_error='', pwd_error='', email_error='')
#     if request.method == 'POST':  # User hit the button and send a signup form.
#         # Update variable set and verify inputs.
#         kwargs['username'] = request.form['username']
#         password = request.form['password']
#         repeat_password = request.form['repeat_password']
#         kwargs['email'] = request.form['email']
#         valid_name, kwargs['name_error'] = is_valid_username(kwargs['username'])
#         valid_pwd, kwargs['pwd_error'] = is_valid_password(password, repeat_password)
#         valid_email, kwargs['email_error'] = is_valid_email(kwargs['email'])
#
#         # If all inputs are valid. Register the user and automatically log in.
#         if valid_name and valid_pwd and valid_email:
#
#             # group = 'guest' if valid_email in get_test_manager_email(DBSession, 0) else 'guest'  # 0 means get all emails.
#             group = 'guest'
#
#             register_user(valid_name, valid_pwd, valid_email, group=group)
#             cookie_val = login_user(valid_name, valid_pwd)  # After signup, automatically login.
#             response = make_response(redirect('/', 302))
#             response.set_cookie('user_id', cookie_val)
#             return response
#
#     return render_template('signup.html',**kwargs)


@app.route('/login')
def login():
    kwargs = dict(username='', name_error='', pwd_error='')
    if request.method == 'POST':
        kwargs['username'] = request.form['username']
        password = request.form['password']
        valid_name, kwargs['name_error'] = is_valid_username(kwargs['username'], check_type='login')
        cookie_val = login_user(valid_name, password)
        if cookie_val:  # login successful
            response = make_response(redirect('/', 302))
            response.set_cookie('user_id', cookie_val)
            return response
    return render_template('login.html', **kwargs)


@app.route('/set_pwd')
def set_pwd():
    return render_template('set_pwd.html')


@app.route('/healthcheck')
def healthcheck():
    return render_template('healthcheck.html')


@app.route('/startup')
def startup():
    return render_template('startup.html')


# ====================All Page Handlers for Users ============================================================

# @app.route('/users', methods=['GET', 'POST'])
# def users():
#     """The handler for '/users'."""
#     kwargs = {}
#     kwargs['loggedin'], uname, ugroup = if_logged_in(request)
#     kwargs['block_add'] = False if ugroup in GROUPS_CAN_ADD_USER else True
#     kwargs['all_users'] = show_all_users()
#
#     if not kwargs['block_add'] and request.form.get('user_action') == 'new':
#         return redirect("/new_user", 302)
#     else:
#         return render_template('users.html', **kwargs)
#
#
# @app.route('/user_<int:user_id>', methods=['GET', 'POST'])
# def user_single(user_id):
#     kwargs = {}
#     kwargs['loggedin'], uname, ugroup = if_logged_in(request)
#     kwargs['block_mod'] = False if ugroup in GROUPS_CAN_MOD_USER else True
#     kwargs['block_del'] = False if ugroup in GROUPS_CAN_DEL_USER else True
#     kwargs['user_id'] = user_id
#     user_info = get_user_info(user_id)
#     kwargs['group'] = GROUPS
#     kwargs['user_info'] = user_info
#
#     if request.method == 'POST':
#         if request.form.get('user_info'):
#             if request.form.get('user_info') == 'Change' and not kwargs['block_mod']:# User changed Project static information
#                 valid_name = kwargs['name'] = request.form['name']
#                 valid_email = kwargs['email'] = request.form['email']
#                 if kwargs['name'] != user_info[0][0]:
#                     valid_name, kwargs['name_error'] = is_valid_username(kwargs['name'])
#                 if kwargs['email'] != user_info[0][1]:
#                     valid_email, kwargs['email_error'] = is_valid_email(kwargs['email'])
#
#                 group = request.form.get('group')
#                 if group == "":
#                     kwargs['group_error'] = "This field can't be empty"
#
#                 if valid_name and valid_email and group:
#                     kwargs['upd_msg'] = update_user(user_id, request.form)
#                     #update user info
#                     kwargs['user_info'] = get_user_info(user_id)
#                     #return redirect("/user_{0}".format(user_id), 302)
#             elif request.form.get('user_info') == 'Delete' and not kwargs['block_del']:  # User delete this project
#                 del_user(kwargs['user_info'][0][0])
#                 return redirect("/users", 302)
#             else:
#                 return "Error: user_info takes invalid value."
#         else:
#             return "Error, expect user_info, but get neither."
#     return render_template('user_single.html', **kwargs)
#
#
# @app.route('/new_user', methods=['GET', 'POST'])
# def new_user():
#     kwargs = {}
#     kwargs['loggedin'], uname, ugroup = if_logged_in(request)
#     kwargs['group'] = GROUPS
#     if ugroup not in GROUPS_CAN_ADD_USER:
#         return redirect("/", 302)
#     if request.method == 'POST':
#         # First collect user inputs.
#         kwargs['name'] = request.form['name']
#         password = request.form['pwd']
#         kwargs['email'] = request.form['email']
#         valid_name, kwargs['name_error'] = is_valid_username(kwargs['name'])
#         valid_pwd, kwargs['pwd_error'] = is_valid_password(password, password)
#         valid_email, kwargs['email_error'] = is_valid_email(kwargs['email'])
#         kwargs['nu_group'] = request.form['group']
#
#         #when all inputs are correct then the user is created:
#         if valid_email and valid_name and valid_pwd:
#             kwargs['up_msg'] = add_new_users(kwargs['name'], password, kwargs['email'], kwargs['nu_group'])
#     return render_template('new_user.html', **kwargs)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8070, debug = False)
