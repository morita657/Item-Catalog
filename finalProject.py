#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User

# login_session works like a dictionary. I can store values in it for
# the longevity of a user's session with my server.
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

CLIENT_ID = json.loads(
open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
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
import json
from flask import make_response
import requests
from functools import wraps

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'
]['client_id']

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


@app.route('/catalog/JSON')
def Catalogjson():
    catalog = session.query(Catalog).all()
    return jsonify(Catalogs=[i.serialize for i in catalog])


@app.route('/catalog/<int:id>/JSON')
def CatalogItemjson(id):
    menu = session.query(CatalogList).filter_by(id=id).one()
    return jsonify(Catalogs=[menu.serialize])


@app.route('/<category>')
def hwy(category):
    categoryItem = \
        session.query(Catalog).filter_by(name=category).first()
    print '', categoryItem.id, categoryItem.name
    return 'hey %s' % categoryItem.name


@app.route('/')
@app.route('/catalog')
def shoCategory():

    categories = session.query(Catalog).all()

    items = session.query(CatalogList).all()
    if 'username' not in login_session:
        print 'hi', login_session
        return render_template('publicItemList.html',
                               categories=categories, items=items)
    else:
        print 'hi', login_session
        return render_template('itemlist.html', categories=categories,
                               items=items)


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state
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
            make_response(json.dumps('Failed to upgrade the authorization code.'
                          ), 401)
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
            make_response(json.dumps("Token's user ID doesn't match given user ID."
                          ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps("Token's Client ID does not match"
                          ), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'
                          ), 200)
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
        '" style="width: 300px; height: 300px; border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
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

        response = make_response(json.dumps('Successfully disconnected.'
                                 ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        # For whatever reason, the given token was invalid.

        response = \
            make_response(json.dumps('Failed to revoke token for given user.'
                          ), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/new', methods=['GET', 'POST'])
@loggedIn
def newCategory():
    if request.method == 'POST':
        newCategory = Catalog(name=request.form['name'],
                              user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        print 'session: ', session
        return redirect(url_for('shoCategory'))

    # newCategory =

    return render_template('newform.html')


    # return "This page will be for making a new restaurant"

@app.route('/catalog/<int:id>/edit', methods=['GET', 'POST'])
@loggedIn
def editCategory(id):

    editCategory = session.query(Catalog).filter_by(id=id).one()
    print 'editCategory.id: ', editCategory.name
    if request.method == 'POST':
        editCategoryName = Catalog(name=request.form['editname'], id=id)
        editCategory.name = editCategoryName.name
        session.add(editCategory)
        session.commit()
        print 'Edit name: ', editCategory.name
        return redirect(url_for('shoCategory'))
    return render_template('editCategoryName.html',
                           editCategory=editCategory, id=id)

@app.route('/catalog/<int:id>/delete', methods=['GET', 'POST'])
@loggedIn
def deleteCategory(id):
    categoryItem = session.query(Catalog).filter_by(id=id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(categoryItem)
        session.commit()
        return redirect(url_for('shoCategory', id=id))
    return render_template('delteCategoryName.html',
                           categoryItem=categoryItem, id=id)


@app.route('/catalog/<int:id>')
@app.route('/catalog/<int:id>/items')
def showItems(id):
    categories = session.query(Catalog).filter_by(id=id).one()
    print 'categories: ', categories
    creator = getUserInfo(categories.user_id)
    items = session.query(CatalogList).filter_by(menu_id=id).all()
    print 'items: ', items
    if 'username' not in login_session or creator.id \
        != login_session['user_id']:
        return render_template('publicShowItems.html',
                               categories=categories, items=items,
                               id=id, creator=creator)
    else:
        return render_template('showItems.html', categories=categories,
                               items=items, id=id, creator=creator)


@app.route('/catalog/<int:id>/items/new', methods=['GET', 'POST'])
@loggedIn
def newMenuItem(id):
    if request.method == 'POST':
        newItem = CatalogList(name=request.form['name'],
                              description=request.form['description'],
                              menu_id=id)
        session.add(newItem)
        session.commit()
        print 'session: ', newItem.id, newItem.name, newItem.menu_id
        return redirect(url_for('showItems', id=id))
    return render_template('newItem.html', id=id)


@app.route('/catalog/<int:id>/<int:item_id>/edit', methods=['GET',
           'POST'])
@loggedIn
def editMenuItem(id, item_id):
    categories = session.query(Catalog).filter_by(id=id).one()
    editItem = session.query(CatalogList).filter_by(id=item_id).one()
    if request.method == 'POST':
        editItemName = CatalogList(name=request.form['editname'],
                                   description=request.form['editdescription'
                                   ],
                                   catalog=request.form['editcategory'])
        editItem.name = editItemName.name
        session.add(editItem)
        session.commit()
        return redirect(url_for('showItems', id=id))
    return render_template('editItemName.html', id=id, item_id=item_id,
                           editItem=editItem)

@app.route('/catalog/<int:id>/<int:item_id>/delete', methods=['GET',
           'POST'])
@loggedIn
def deleteMenuItem(id, item_id):
    items = session.query(Catalog).all()
    deleteItem = session.query(CatalogList).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('showItems', id=id))
    return render_template('deleteItemName.html', id=id,
                           item_id=item_id, deleteItem=deleteItem)

@app.route('/catalog/<int:id>/<int:item_id>')
def showItemDetail(id, item_id):
    categories = session.query(Catalog).filter_by(id=id).one()
    print 'categories: ', categories
    creator = getUserInfo(categories.user_id)
    items = session.query(CatalogList).filter_by(id=item_id).one()
    if 'username' not in login_session or creator.id \
        != login_session['user_id']:
        return render_template('publicShowItemDetail.html', id=id,
                               item_id=item_id, items=items,
                               categories=categories)
    else:
        return render_template('showItemDetail.html', id=id,
                               item_id=item_id, items=items,
                               categories=categories)

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
    user = session.query(User).filter_by(email=login_session['email'
            ]).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
