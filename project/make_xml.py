#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app
from utils import *
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session
import json
import urllib
import dicttoxml


@app.route('/catalog/XML')
def Catalogxml():
    catalog = session.query(Catalog).all()
    for i in catalog:
         catalog_xml = i.serialize
    data = dicttoxml.dicttoxml(catalog_xml)
    return render_template('string.html', data=data)


@app.route('/catalog/<int:id>/XML')
def CatalogItemxml(id):
    category_item = session.query(CatalogList).filter_by(menu_id=id).all()
    for j in category_item:
        items_xml = j.serialize
    data = dicttoxml.dicttoxml(items_xml)
    return render_template('string.html', data=data)


@app.route('/catalog/<int:id>/<int:item_id>/XML')
def Itemxml(id, item_id):
    item_xml = session.query(CatalogList).filter_by(id=item_id).one()
    data = dicttoxml.dicttoxml(item_xml.serialize)
    return render_template('string.html', data=data)
