#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app

app = Flask(__name__)
app.secret_key = 'super'
app.debug = True
