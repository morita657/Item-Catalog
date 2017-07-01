#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app

if __name__ == '__main__':
    app.secret_key = 'super'
    app.debug = True
