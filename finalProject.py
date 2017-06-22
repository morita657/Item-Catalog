#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app

if __name__ == '__main__':
    app.secret_key = 'super'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
