import os, sys
from app import app, db
from flask import render_template, flash, redirect, request
from app.forms import AccountForm
from bson.objectid import ObjectId


# accounts index
@app.route('/admin/queues/')
def queues():
    queues = db.queues.find()
    return render_template('backend/queues/index.html', queues=queues)



# delete account
@app.route('/admin/queues/<id>/delete/')
def queuesDelete(id):
    db.queues.remove(ObjectId(id))
    return redirect('/admin/queues')
