#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app
from utils import *
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session
import json


@app.route('/catalog/JSON')
def Catalogjson():
    catalog = session.query(Catalog).all()
    return jsonify(Catalogs=[i.serialize for i in catalog])


@app.route('/catalog/<int:id>/JSON')
def CatalogItemjson(id):
    items = session.query(CatalogList).filter_by(menu_id=id).all()
    return jsonify(Catalogs=[j.serialize for j in items])


@app.route('/catalog/<int:id>/<int:item_id>/JSON')
def Itemjson(id, item_id):
    items = session.query(CatalogList).filter_by(id=item_id).one()
    return jsonify(Item=[items.serialize])
