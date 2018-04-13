#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re, random, hashlib


from string import ascii_letters

from get_json_info import get_username
from get_json_info import get_hash_password


USER_RE = re.compile(r"^[a-zA-Z0-9\._-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")

VALID_EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def make_salt(length = 5):
    return ''.join(random.choice(ascii_letters) for x in range(length))


def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    input_string = name + pw + salt
    h = hashlib.sha256(input_string.encode()).hexdigest()
    return '%s|%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split('|')[0]
    return h == make_pw_hash(name, password, salt)


def is_valid_username(name, check_type='signup'):
    """
    Support function for /signup handler
    Input: name: string or None.
    Output: username: string or None; msg: string
    """
    username, msg = None, ''
    usernames = get_username()
    if not name:
        msg = "User Name can't be empty."
    elif not USER_RE.match(name):
        msg = "Name must be 3 t 20 letters or digits or - or _ or . "
    elif check_type=='signup' and name in usernames:
        msg = "This name already exists."
    elif check_type=='login' and name not in usernames:
        msg = "This username doesn't exists."
    else:
        username = name
    return username, msg


def is_valid_password(pwd, repeat):
    """
    Given two user inputs. Decide if the password is valid.
    Inputs: pwd: string; repeat: string;
    Output: valid_pwd: string; msg: string;
    """
    valid_pwd, msg = None, ""
    if not pwd:
        msg = "Password can't be empty."
    elif not PASS_RE.match(pwd):
        msg = "Password must be 3 to 20 characters long."
    elif pwd != repeat:
        msg = "Password and repeat don't match."
    else:
        valid_pwd = pwd
    return valid_pwd, msg


def is_valid_email(email):
    """Verify if the input is a valid email string."""

    valid_email, msg = None, ''
    if not email:
        msg = "This field can't be empty"
    elif VALID_EMAIL.match(str(email)):
        valid_email = str(email)
    else:
        msg = "This is not an valid email"
    return valid_email, msg


def register_user(username, password, email, group='guest'):
    """
    When called by handler signup, create a record in the sqllite3 credential.db, table User
    Inputs:
      username: string
      password: string
      email: string
      group: string.  ['admin', 'developer', 'guest']
    """
    conn, c = make_conn_c()
    pwd_hash = make_pw_hash(username, password)
    try:
        c.execute(INSERT_SQL.format(username, pwd_hash, email, group))
        conn.commit()
        conn.close()
    except:
        return "ERR: {}".format(sys.exc_info()[0])


def login_user(name, pwd):
    """
    Give a username, a pwd. First verify if it matches.
    set the user's cookie according to the verification.
    Inputs: name, string; pwd, string
    Output: cookie value for name 'user_id' can be ''
    """
    cookie_val = ''

    # conn, c = make_conn_c()
    # q = c.execute("SELECT id, pwd_hash FROM USERS where name = '{0}';".format(name)).fetchall()
    # conn.close()


    if q and valid_pw(name, pwd, q[0][1]):
        cookie_val = make_secure_val(str(q[0][0]))
    return cookie_val


if __name__ == '__main__':
    # name = 'oza'
    # password = '1234'
    # x = make_pw_hash(name, password)
    # print(x)
    # print(x.split('|')[0])
    # salt = x.split('|')[0]

    bool = valid_pw('hanrong', '640519', 'QwZvo|c71989a389c75e042f6fed70ece80bbc2e70da67fc28d4d2968013f691418936')
    print(bool)

    bool = valid_pw('oza', '1234', 'AuYea|9d469f79f7d64c029b5abcd87697958fbd352620fae7ac87f7ed129ba3b76a72')
    print(bool)
