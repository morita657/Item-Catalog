#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app
from utils import *
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort

from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import requests
import httplib2
from utils import *


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32))
    login_session['state'] = state
    print 'login_session: ', login_session
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:

        # Upgrade the authorization code into a credentialas object

        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps('Failed to upgrade the authorization\
             code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

        # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps("Token's user ID doesn't match given \
            user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps("Token's Client ID does not \
            match"), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already \
            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store the access token in the session for later use.

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        '" style="width: 300px; height: 300px; border-radius: 150px;\
        -webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash('you are now logged in as %s' % login_session['username'])
    print "login_session['username']: ", login_session['username']
    return output


# DISCONNECT  - Revoke a current user's token and rest their login_session

@app.route('/gdisconnect')
def gdisconnect():

    # Only disconnect a coneccted user.

    credentials = login_session.get('credentials')
    if credentials is None:
        response = \
            make_response(json.dumps('Current user not connected.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request request to revoke current token.

    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':

        # Result the user's session.

        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        response = make_response(json.dumps('Successfully \
        disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        # For whatever reason, the given token was invalid.

        response = \
            make_response(json.dumps('Failed to revoke token for given \
            user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
