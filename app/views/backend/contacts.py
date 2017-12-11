from app import app, db
from flask import render_template, flash, redirect, request, jsonify, Response
from app.forms import ContactForm
from bson.objectid import ObjectId
import bson, re
from app.lib.utils import mailer
from app.lib.utils.logger import mongoLogger
import pymongo
from pymongo.errors import PyMongoError
import uuid
from datetime import datetime, timedelta

#logs handler
mongolog = mongoLogger(db)

# contacts index
@app.route('/admin/contacts/')
def contacts():
    notification = request.args.get('notification')
    if notification:
        contacts = db.contacts.find({'preferences.articles_notify': notification})
    else:
        contacts = db.contacts.find()
    return render_template('backend/contacts/index.html',
                            contacts=contacts,
                            count = contacts.count())

# add new contacts
@app.route('/admin/contacts/new/', methods=['GET', 'POST'])
def contactsNew():
    form = ContactForm(request.form)
    if request.is_xhr:
        # ajax request
        data = form.data
        try:
            # search contact doc
            contact = db.contacts.find_one({'firstname': request.form['firstname'], 'email': request.form['email']})
            if contact:
                # add article to contact
                db.contacts.update(
                    {'firstname': request.form['firstname'],'email': request.form['email']},
                    {'$addToSet': {'articles': request.form["article_id"]}}, upsert=True
                )
                return jsonify(status=1, msg='Article added to contact document')
            else:
                # no contact found: create a new one and insert article
                data['articles'] = [request.form["article_id"]]
                data['preferences'] = {'articles_notify': 'default'}
                data['notify_queue'] = []
                db.contacts.insert_one(data)
                return jsonify(status=1, msg='New contact added')
        except PyMongoError as e:
            print(e)
            #data['articles'] = [request.form["article_id"]]
            #db.contacts.insert_one(data)
            return jsonify(status=0, msg='Error:' + e)

    elif request.method == "POST" and form.validate():
        # post request
        db.contacts.replace_one({'firstname': request.form['firstname'], 'email': request.form['email']}, form.data, upsert=True)
        flash('New contact  %s added' %(form.data['firstname']))
        return redirect('/contacts')
    else:
        return render_template('backend/contacts/edit.html',
                                form=form,
                                title='New contact')


# view contact
@app.route('/admin/contacts/<id>/')
def contactsView(id):
    contact = db.contacts.find_one({ '_id': ObjectId(id) })
    if contact:
        articles = db.articles.find({'_id': {'$in': map(ObjectId, contact['articles']) }}).sort('pub_date', pymongo.DESCENDING)
        return render_template('backend/contacts/view.html',
                                contact=contact,
                                articles=articles)
    else:
        flash('contact %s not found' %id)
    return redirect('/contacts')

#edit contact
@app.route('/admin/contacts/<id>/edit/', methods=['GET', 'POST'])
def contactsEdit(id):
    try:
        contact = db.contacts.find_one({ '_id': ObjectId(id) })
        form = ContactForm(data=contact)
        if request.method == "POST" and form.validate():
            form = ContactForm(request.form)
            db.contacts.replace_one({'email': form.data['email']}, form.data, upsert=True)
            return redirect('/admin/contacts')
        else:
            return render_template('backend/contacts/edit.html',
                                    form=form,
                                    title='Contact: ' + contact['firstname'])
    except Exception as e:
        flash("Couldn't update contact %s" %(form.data['firstname']))
        return render_template('backend/contacts/edit.html',
                                form=form,
                                title='New contact')


@app.route('/admin/contacts0/<id>/edit/', methods=['GET', 'POST'])
def contactsEdit0(id):
    form = ContactForm({'test':'ok'})
    return render_template('backend/test.html',
                            form=form)


# delete contact
@app.route('/admin/contacts/<id>/delete/')
def contactsDelete(id):
    db.contacts.remove(ObjectId(id))
    return redirect('/admin/contacts')

# multiple delete article
@app.route('/admin/contacts/<ids>/delete_all/')
def contactsDeleteAll(ids):
    ids = ids.split('$')[:-1]
    ids = [ObjectId(id) for id in ids ]
    db.contacts.remove({ '_id': { '$in': ids } } )
    return redirect('/admin/contacts')


# export contacts list to csv
@app.route('/admin/contacts/export/csv/')
def contactsCsv():
    def generate():
        contacts = db.contacts.find({}, {'firstname': 1, 'lastname': 1, 'email': 1, 'organization': 1, 'position': 1, 'mobile': 1, '_id': 0})
        top_row = 'firstname,lastname,email,mobile,organization,position'
        rows = top_row + '\n'
        for contact in contacts:
            ordered_row = list((contact[x] if x in contact else '') for x in top_row.split(','))
            rows +=  ','.join(ordered_row) + '\n'
        yield rows
    return Response(generate(), mimetype='text/csv')


# contacts live search
@app.route('/admin/contacts/search/', defaults={'query': ''})
@app.route('/admin/contacts/search/<query>')
def contactsSearch(query):
    if len(query) > 0:
        query = re.compile(query, re.IGNORECASE)
        contacts = db.contacts.find({ '$or': [{'firstname': {'$regex': query}}, {'lastname': {'$regex': query}}, {'email': {'$regex': query}}, {'organization': {'$regex': query}} ]})
    else:
        contacts = db.contacts.find()
    data = render_template('backend/contacts/list.html',
                            contacts=contacts)
    return jsonify({'data': data, 'count': contacts.count()})


# add new contact & notify new article
@app.route('/admin/contacts/createandnotify/', methods=['POST'])
def contactsNewNotify():
    form = ContactForm(request.form)
    data = form.data
    try:
        mongolog.add('- ADD CONTACT: adding contact with email ' + data['email'])
        contact = db.contacts.find_one({'email': data['email']})
        if contact:
            contact_notify_preference = contact['preferences']['articles_notify']
            db.contacts.update({'email': data['email']}, {'$addToSet': {'articles': request.form["article_id"]}}, upsert=True)
            data['article_id'] = request.form['article_id'] # add article_id to data list passed to mailer
            if contact_notify_preference != 'unsubscribed':
                if contact_notify_preference == 'default':
                    notifyContact(data, contact['_id'])
                    return jsonify(status=1, msg='Article added to contact document')
                else:
                    db.contacts.update({'email': data['email']}, {'$addToSet': {'notify_queue': data['article_id']}}, upsert=True)
                    db.queues.insert_one({ 'email' : data['email'], 'article_id': data['article_id'], 'frequency': contact_notify_preference })
                    return jsonify(status=1, msg='Article added to contact document and notification queued')
            else:
                return jsonify(status=1, msg='Article added to contact document, but this contact has not subscribed to the alert service.')
        else:
            data['articles'] = [request.form['article_id']]
            data['preferences'] = {'articles_notify': 'default'}
            data['notify_queue'] = []
            result = db.contacts.insert_one(data)
            data['article_id'] = request.form['article_id'] # add article_id to data list passed to mailer
            notifyContact(data, str(result.inserted_id))
            return jsonify(status=1, msg='New contact added')
    except PyMongoError as e:
        mongolog.add('- contactsNewNotify: ERROR - ' + str(e))
        mongolog.store()
        return jsonify(status=0, msg=e)


# send email to contact with new article info
def notifyContact(data, contact_id):
    try:
        article = db.articles.find_one({'_id': ObjectId(data['article_id'])})
        if article:
            token = str(uuid.uuid4())
            params = {}
            params['from'] = 'ALP Content Services <sales@al-arabic.com>'
            params['contact_name'] = data['firstname']
            params['to'] = data['firstname'] + ' ' + data['lastname'] + ' <' + data['email'] + '>'
            params['subject'] = 'Your article "' + article['title'] + '" has been published'
            params['bcc'] = app.config['CRM_BCC'] 
            body = render_template('emails/congrats-3.html',
                                    title=article['title'],
                                    article_link=article['url'],
                                    token=token,
                                    host=app.config['SERVER_URL'],
                                    link=app.config['SERVER_URL'] + '/jobs/' + str(contact_id) + '/' + str(data['article_id']),
                                    contact_name=params['contact_name'])
            params['body'] = body
            mailer.send_email(params)
            mongolog.add('- NOTIFY: sending alert to ' + data['email'])
            mongolog.store()
            db.contacts.update_one({'_id': ObjectId(contact_id)}, {'$set': {'token': token, 'preferences.articles_notify': 'default'}})
        else:
            print('article ' + str(data['article_id']) + ' not found')
            mongolog.add('- ARTICLE NOTIFY: article ' + str(data['article_id']) + ' not found')
            mongolog.store()
        return
    except Exception as e:
        print('Error:', str(e))
        mongolog.add('- notifyContact: ERROR - ' + str(e))
        mongolog.store()
        return

