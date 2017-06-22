#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from functools import wraps

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'][
    'client_id']
engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def loggedIn(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = login_session.get('user_id')
        if user_id is None:
            print 'not loggedin: ', user_id
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper


def user_authed(uid, sess_id):
    """Tests whether a user is authorized to make CRUD action"""
    if uid != sess_id:
        abort(403)
    else:
        return True


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id
