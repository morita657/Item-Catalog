#!/usr/bin/python
# -*- coding: utf-8 -*-
from project import app
from utils import *
from item_views import showItemDetail
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify, make_response, abort
from finalProjectDatabase_setup import Base, Catalog, CatalogList, User
from flask import session as login_session


@app.route('/')
@app.route('/catalog')
def shoCategory():
    # Show latest created items and categories
    categories = session.query(Catalog).all()
    items = session.query(CatalogList).order_by("id desc").limit(10).all()
    if 'username' not in login_session:
        return render_template('publicItemList.html', categories=categories,
                               items=items)
    else:
        return render_template('itemlist.html', categories=categories,
                               items=items)


@app.route('/catalog/new', methods=['GET', 'POST'])
@loggedIn
def newCategory():
    # Create new category
    if request.method == 'POST':
        newCategory = Catalog(name=request.form['name'],
                              user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        print 'session: ', session
        return redirect(url_for('shoCategory'))
    return render_template('newform.html')


@app.route('/catalog/<int:id>/edit', methods=['GET', 'POST'])
@loggedIn
def editCategory(id):
    # Edit category information
    editCategory = session.query(Catalog).filter_by(id=id).one()
    creator = getUserInfo(editCategory.user_id)
    items = session.query(CatalogList).filter_by(menu_id=id).all()
    if not user_authed(creator.id, login_session['user_id']):
        return render_template('publicShowItems.html',
                               categories=editCategory, items=items,
                               id=id, creator=creator)
    else:
        if request.method == 'POST':
            editCategoryName = Catalog(name=request.form['editname'], id=id)
            editCategory.name = editCategoryName.name
            session.add(editCategory)
            session.commit()
            return redirect(url_for('shoCategory'))
        return render_template('editCategoryName.html',
                               editCategory=editCategory, id=id)


@app.route('/catalog/<int:id>/delete', methods=['GET', 'POST'])
@loggedIn
def deleteCategory(id):
    # Delete a category and that of items
    categoryItem = session.query(Catalog).filter_by(id=id).one()
    if not user_authed(categoryItem.user_id, login_session['user_id']):
        return "<script>function myFunction() {alert('You are not authorized \
        to delete this category. Please create your own category in order \
        to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(categoryItem)
        session.commit()
        return redirect(url_for('shoCategory', id=id))
    return render_template('delteCategoryName.html',
                           categoryItem=categoryItem, id=id)
