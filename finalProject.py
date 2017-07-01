#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from project import app

# app = Flask(__name__)
app.secret_key = 'super'
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True
# app.run(host='0.0.0.0', port=5000)
