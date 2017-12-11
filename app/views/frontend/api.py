from app import app, db
from flask import render_template, flash, redirect, jsonify
from bson.objectid import ObjectId


# update contact articles notification preferences
@app.route('/api/contacts/<token>/p/<settings>', methods=['GET'])
def get_contacts_preferences(token, settings):
    # search contact by token
    contact = db.contacts.find_one({'token': token})
    if contact:
        # only allow these settings to be updated
        if settings in ['unsubscribed','daily', 'weekly']:
            contact['preferences'] = settings
            db.contacts.update_one({'token': token}, {'$set': {'preferences.articles_notify': settings}, '$unset': {'token': ''} })
            if settings == 'unsubscribed':
                msg = 'Thank you.<br><br>You have been unsubscribed from the Monitor service.<br><br>Do no hesitate to contact us at <a href="mailto:sales@al-arabic.com">sales@al-arabic.com</a> for your future inquiries.'
            else:    
                msg = 'Hi ' + contact['firstname'] + '. Your email preferences have been updated.'
        else:
            msg = 'Invalid request'
    else:
        msg = 'The link for this request has expired.<br><br>Contact <a href="mailto:info@al-arabic.com">info@al-arabic.com</a> for assistance.'

    #redirect to confirmation page with message
    flash({'title': 'Updating your preferences', 'text': msg})
    return redirect('/confirm')
