from app import app, db
from flask import render_template, flash
from flask_login import LoginManager
from app.forms import LoginForm


app.config['SECRET_KEY'] = 'monkey'
authn = LoginManager(app)


@app.route('/admin/login/')
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('adminIndex'))
    return render_template('backend/auth/login.html', form=form)

def login():
    return render_template('backend/auth/login.html'), 401
