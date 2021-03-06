#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, Cleverest Technologies"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from gevent import monkey
monkey.patch_all()

import subprocess
import requests
import glob
import os
from flask import Flask, render_template, session, request, json, jsonify, url_for, Markup, redirect
import random
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect
import re
from pprint import pprint
import random
from threading import Lock
import json
import socket
from flask import Markup
import copy
import base64
# import python-mongo library
from pymongo import MongoClient
# import datetime to deal with timestamps
from datetime import datetime


client = MongoClient('mongodb://database:27017/')
db = client.entrance


async_mode = None

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def write_to(request, pin):
    item_doc = {
        'Employee': request.form['FIOin'],
        'Guest': request.form['FIOout'],
        'Room': request.form['room'],
        'Date': datetime.now(),
        'IP': str(request.remote_addr),
        'PIN': pin,
        'GuestIn': False,
        'DateIn': None
    }
    db.zayavki.insert_one(item_doc)


def logit(req):
    item_doc = {
        'Employee': req['Employee'],
        'Guest': req['Guest'],
        'Room': req['Room'],
        'Date': req['Date'],
        'IP': req['IP'],
        'PIN': None,
        'GuestIn': True,
        'DateIn': datetime.now()
    }
    db.zayavki.insert_one(item_doc)


def send_tlg_msg(msg, ids, photo):
    x = 1
    bot = telepot.Bot('636656567:AAGJNwvclwoJLHoice4DJkS_03H3m5Fpmso')
    for id in ids:
        try:
            bot.sendPhoto(str(id), photo, caption=msg)
        except:
            pass


@app.route('/', methods=['GET', 'POST'])
def welcome2():
    return render_template('zayava.html', text="Введите данные:")


@app.route('/check/', methods=['GET', 'POST'])
def welcome3():
    first = random.choice(range(1, 10))
    leftover = set(range(10)) - {first}
    rest = random.sample(leftover, 5)
    digits = [first] + rest
    name = ''
    for let in digits:
        name += str(let)
    print("name is " + str(name))
    write_to(request, name)
    return render_template('zayava.html', text="Код доступа: " + str(name))


if __name__ == '__main__':
    print(os.system("ls"))
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
