#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app
from utils import *
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort, send_from_directory, Response
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session
import json
import urllib
import dicttoxml
from xml.dom.minidom import parseString


@app.route('/catalog/XML')
def downloadCatalog():
    data_store = []
    catalog = session.query(Catalog).all()
    for i in catalog:
         data_store.append(i.serialize)
    data = dicttoxml.dicttoxml(data_store)
    dom = parseString(data)
    prettyxml = dom.toprettyxml()
    # xml = prettyxml
    return Response(
    prettyxml,
    mimetype='text/xml',
    headers={'Content-disposition':'attachment; filename=catalog.xml'})


@app.route('/catalog/<int:id>/XML')
def downloadCatalogItemxml(id):
    data_store = []
    category_item = session.query(CatalogList).filter_by(menu_id=id).all()
    for j in category_item:
        data_store.append(j.serialize)
    data = dicttoxml.dicttoxml(data_store)
    dom = parseString(data)
    prettyxml = dom.toprettyxml()
    # xml = prettyxml
    return Response(
    prettyxml,
    mimetype='text/xml',
    headers={'Content-disposition':'attachment; filename=catalog-item.xml'})


@app.route('/catalog/<int:id>/<int:item_id>/XML')
def downloadItemxml(id, item_id):
    data_store = []
    item_xml = session.query(CatalogList).filter_by(id=item_id).one()
    data = dicttoxml.dicttoxml(item_xml.serialize)
    dom = parseString(data)
    prettyxml = dom.toprettyxml()
    # xml = prettyxml
    return Response(
    prettyxml,
    mimetype='text/xml',
    headers={'Content-disposition':'attachment; filename=item-detail.xml'})
