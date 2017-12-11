from app import app
from flask import render_template
from . import index, jobs, api


'''
automatic routing for static page
@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('frontend/%s.html' % page_name)
'''


@app.errorhandler(404)
def page_not_found(e):
    return render_template('frontend/errors/404.html', error=e), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('frontend/errors/500.html', error=e), 500
