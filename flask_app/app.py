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

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


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
    text = request.form['FIOin'] + ":" + request.form['FIOout'] + ":" + request.form['room'] + \
           ":" + str(request.remote_addr)
    first = random.choice(range(1, 10))
    leftover = set(range(10)) - {first}
    rest = random.sample(leftover, 5)
    digits = [first] + rest
    name = ''
    for let in digits:
        name += str(let)
    print("name is " + str(name))
    print("value is " + text)
    with open('/home/pi/entrance/static/logs/' + name + '.txt', "w") as file:
        data = file.write(text)
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
        kod = request.form['kod']
        try:
            with open('/home/pi/entrance/static/logs/' + kod + '.txt', "r") as file:
                data = file.readline()
                data2 = data.split(":")
                data3 = "Заказал пропуск: " + str(data2[0])
                data3 += ", в кабинет: : " + str(data2[2])
                data3 += ", для гражданина: : " + str(data2[1])
                send_tlg_msg(data3, ['-1001403922890'], open('/home/pi/entrance/static/face.png', "rb"))
            os.system("rm /home/pi/entrance/static/logs/" + kod + '.txt')
        except:
            return render_template('index2.html', text=Markup("Вы ввели неправильный пароль"))
        return render_template('index2.html', text=Markup("Входите"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('cert.pem', 'key.pem'))
