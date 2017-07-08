#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User

# login_session works like a dictionary. I can store values in it for
# the longevity of a user's session with my server.

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
from category_views import shoCategory, newCategory, editCategory, \
    deleteCategory
from item_views import showItems, newMenuItem, editMenuItem, deleteMenuItem
from make_json import Catalogjson, CatalogItemjson, Itemjson
from make_xml import downloadCatalog, downloadCatalogItemxml, downloadItemxml
from auth import showLogin, gconnect, gdisconnect
from utils import *
