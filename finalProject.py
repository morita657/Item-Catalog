#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask
from project import app

# app = Flask(__name__)
# app = Flask(__name__)
# app.secret_key = 'super'
# app.config['SESSION_TYPE'] = 'filesystem'
port = int(os.environ.get('PORT', 5000))
server_address = ('', port)
# httpd = http.server.HTTPServer(server_address, Shortener)
app.config.from_object('config')
# app.debug = True
# app.run(host='0.0.0.0', port=5000)
