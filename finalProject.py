#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask
from project import app

app.debug = True
port = int(os.environ.get('PORT', 5000))
server_address = ('', port)
app.config.from_object('config')
