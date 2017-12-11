from app import app, db
from flask import render_template, flash, redirect, request
from bson.objectid import ObjectId

# sources index
@app.route('/admin/config/')
def config():
    config = db.config.find_one()
    return render_template('backend/config/index.html',
                            config=config)
