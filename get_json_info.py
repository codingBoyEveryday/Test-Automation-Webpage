#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib.request
import json


def get_username():
    username = []
    with urllib.request.urlopen("http://localhost:8080/api/User") as url:
        data = json.loads(url.read().decode())
        for user in data["data"]:
            username.append(user["username"])
    return username


def get_hash_password(username):
    pwd_hash = ''
    with urllib.request.urlopen("http://localhost:8080/api/User") as url:
        data = json.loads(url.read().decode())
        for user in data["data"]:
            if username == user["username"]:
                pwd_hash = user["password_hash"]
                break
            else:
                raise NameError('Invalid username!')
        return pwd_hash


if __name__ == '__main__':
    x = get_username()
    print(x)

    y = get_hash_password('hanrong')
    print(y)

    z = get_hash_password('martin')
    print(z)
