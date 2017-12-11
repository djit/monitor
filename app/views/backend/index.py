from app import app
from flask import render_template, flash, redirect


# admin index
@app.route('/admin')
def index():
    return render_template('backend/index.html')
