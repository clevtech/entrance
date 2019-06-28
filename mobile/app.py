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
from flask import Flask, render_template, session, request, json, jsonify, url_for, Markup, redirect
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
import telepot
# import python-mongo library
from pymongo import MongoClient
# import datetime to deal with timestamps
from datetime import datetime


client = MongoClient('mongodb://database:27017/')
db = client.entrance


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


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
        pic = base64.b64decode(request.form["img"])
        result = db.entrance.find_one({"PIN": str(kod)})
        if result:
            db.entrance.delete_one({"PIN": kod})

            data3 = "Заказал пропуск: " + str(result['Employee'])
            data3 += "(с IP: " + str(result['IP']) + ")"
            data3 += ", в кабинет: : " + str(result["Room"])
            data3 += ", для гражданина: : " + str(result['Guest'])
            send_tlg_msg(data3, ['-1001403922890'], pic)

            return render_template('index2.html', text=Markup("Входите"))
        else:
            return render_template('index2.html', text=Markup("Вы ввели неправильный пароль"))
    else:
        return render_template('index3.html', text=Markup("Вы ввели неправильный пароль"))


if __name__ == '__main__':
    print(os.system("ls"))
    app.run(host='0.0.0.0', port=7777, debug=True, ssl_context=('./mobile/cert.pem', './mobile/key.pem'))
