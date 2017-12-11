import os, sys
from app import app, db
from flask import render_template, flash, redirect, request
from app.forms import AccountForm
from bson.objectid import ObjectId


# accounts index
@app.route('/admin/accounts/')
def accounts():
    accounts = db.accounts.find()
    return render_template('backend/accounts/index.html', accounts=accounts)

# add new accounts
@app.route('/admin/accounts/new/', methods=['GET', 'POST'])
def accountsNew():
    if request.method == 'POST':
        form = AccountForm(request.form)
        if form.validate():
            db.accounts.insert_one(form.data)
            flash('New account  %s added' %(form.name.data))
            return redirect('/admin/accounts')
        else:
            return render_template('backend/accounts/edit.html',
                                    form=form,
                                    title='New account')
    form = AccountForm()
    return render_template('backend/accounts/edit.html',
                            form=form,
                            title='New account')

# view account
@app.route('/admin/accounts/<id>/')
def accountsView(id):
    account=db.accounts.find_one({ '_id': ObjectId(id) })
    if account:
        return render_template('backend/accounts/view.html',
                                account=account)
    else:
        flash('account %s not found' %id)
        return redirect('/admin/accounts')

#edit account
@app.route('/admin/accounts/<id>/edit/', methods=['GET', 'POST'])
def accountsEdit(id):
    account = db.accounts.find_one({ '_id': ObjectId(id) })
    if account:
        if request.method == 'POST':
            form = AccountForm(request.form)
            if form.validate():
                db.accounts.update({ '_id': ObjectId(id) }, form.data)
                return redirect('/admin/accounts')
            else:
                return render_template('backend/accounts/edit.html',
                                        form=form,
                                        title='account: ' + account['name'])
        form=accountForm(data=account)
        return render_template('backend/accounts/edit.html',
                                form=form,
                                title='account: ' + account['name'])
    else:
        flash('account %s not found' %id)
    return redirect('/admin/accounts')

# delete account
@app.route('/admin/accounts/<id>/delete/')
def accountsDelete(id):
    db.accounts.remove(ObjectId(id))
    return redirect('/accounts')
