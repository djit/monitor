from app import app, db
from flask import render_template, flash, redirect, request
from flask_paginate import Pagination
from bson.objectid import ObjectId
import pymongo


# contacts index
@app.route('/admin/logs/')
def logs():
    search = False
    q = request.args.get('q')
    display = 20
    skip = 0
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    #page = min(page, round(logs.count()/display, 0))
    skip = display * (page - 1)
    logs = db.logs.find().sort('timestamp', pymongo.DESCENDING).skip(skip).limit(display);
    pagination = Pagination(page=page, total=logs.count(), search=search, record_name='logs')
    return render_template('backend/logs/index.html',
                            logs=logs,
                            pagination=pagination)

# view contact
@app.route('/admin/logs/<id>/')
def logsView(id):
    log = db.logs.find_one({ '_id': ObjectId(id) })
    if log:
        return render_template('backend/logs/view.html',
                                log=log)
    else:
        flash('log %s not found' %id)
        return redirect('/logs')


# delete logs
@app.route('/admin/logs/<id>/delete/')
def logsDelete(id):
    db.logs.remove(ObjectId(id))
    return redirect('/admin/logs')

# delete multiple logs
@app.route('/admin/logs/<ids>/delete_all/')
def logsDeleteAll(ids):
    ids = ids.split('$')[:-1]
    ids = [ObjectId(id) for id in ids ]
    db.logs.remove({ '_id': { '$in': ids } } )
    return redirect('/admin/logs')
