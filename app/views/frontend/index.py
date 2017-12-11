from app import app
from flask import render_template, redirect, request, send_from_directory


# admin index
@app.route('/')
def publicIndex():
    return redirect('http://al-arabic.com')


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    print request.path[1:]
    return send_from_directory('static', request.path[1:])


# display confirmation message
@app.route('/confirm')
def display_message():
    return render_template('frontend/message.html')