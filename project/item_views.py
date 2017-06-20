from project import app
from utils import *
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort
# from functools import wraps
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session
# import json

@app.route('/catalog/<int:id>')
@app.route('/catalog/<int:id>/items')
def showItems(id):
    categories = session.query(Catalog).filter_by(id=id).one()
    print 'categories: ', categories
    creator = getUserInfo(categories.user_id)
    items = session.query(CatalogList).filter_by(menu_id=id).all()
    print 'items: ', items
    if 'username' not in login_session or creator.id\
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
    creator = getUserInfo(categories.user_id)

    if not user_authed(creator.id, login_session['user_id']):
        return render_template('publicShowItemDetail.html', id=id,
                               item_id=item_id, items=items,
                               categories=categories)
    else:
        if request.method == 'POST':
            editItemName = CatalogList(name=request.form['editname'],
                    description=request.form['editdescription'],
                    catalog=request.form['editcategory'])
            editItem.name = editItemName.name
            session.add(editItem)
            session.commit()
            return redirect(url_for('showItems', id=id))
        return render_template('editItemName.html', id=id,
                               item_id=item_id, editItem=editItem)


@app.route('/catalog/<int:id>/<int:item_id>/delete', methods=['GET',
           'POST'])
@loggedIn
def deleteMenuItem(id, item_id):
    items = session.query(Catalog).all()
    deleteItem = session.query(CatalogList).filter_by(id=item_id).one()
    if not user_authed(deleteItem.user_id, login_session['user_id']):
        return "<script>function myFunction() {alert('You are not authorized \
        to delete this item. Please create your own item in order to \
        delete.');}</script><body onload='myFunction()'>"
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
    if 'username' not in login_session or user_authed(creator.id,
            login_session['user_id']):
        return render_template('publicShowItemDetail.html', id=id,
                               item_id=item_id, items=items,
                               categories=categories)
    else:
        return render_template('showItemDetail.html', id=id,
                               item_id=item_id, items=items,
                               categories=categories)
