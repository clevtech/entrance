#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, Cleverest Technologies"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

import subprocess
import requests
import glob
import base64
import os
from flask import Flask, render_template, session, request, json, jsonify, url_for, Markup, redirect, send_file
import random
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
from binascii import a2b_base64
import os
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect


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
        'PIN': str(pin),
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


def save_face():
    import rtsp
    with rtsp.Client('rtsp://192.168.81.218:8554/live') as client:
        client.read().rotate(270).save("face.png")


def send_tlg_msg(msg, ids):
    for id in ids:
        try:
            from requests import Request, Session

            head = "https://api.telegram.org/bot636656567:AAGJNwvclwoJLHoice4DJkS_03H3m5Fpmso/sendMessage?chat_id=" + \
                   id + "&text=" + msg

            print(requests.get(head))

            head = "https://api.telegram.org/bot636656567:AAGJNwvclwoJLHoice4DJkS_03H3m5Fpmso/sendPhoto?chat_id=" + \
                   id

            file = open('face.png', 'rb')
            files = {"photo": file}

            print(requests.post(head, files=files))



        except:
            print("No connection to telegram")


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


@app.route('/mobile/')
def welcome():
    return render_template('index3.html')


@app.route('/give/', methods=['GET', 'POST'])
def give():
    return render_template('enter.html')


@app.route('/give/check/', methods=['GET', 'POST'])
def chechit():
    if request.method == "POST":
        # print(request)
        print(request.form['kod'])
        kod = request.form['kod']

        result = db.zayavki.find_one({"PIN": str(kod)})
        if result:
            db.zayavki.delete_many({"PIN": kod})
            logit(result)
            data3 = "Заказал пропуск: " + str(result['Employee'])
            data3 += " (с IP: " + str(result['IP']) + ")"
            data3 += ", в кабинет: " + str(result["Room"])
            data3 += ", для гражданина: " + str(result['Guest'])

            # TODO Make it work bitch

            save_face()

            send_tlg_msg(data3, ['-1001403922890'])

            return render_template('index2.html', text=Markup("Входите"))
        else:
            return render_template('index2.html', text=Markup("Вы ввели неправильный пароль"))
    else:
        return render_template('index3.html', text=Markup("Вы ввели неправильный пароль"))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
