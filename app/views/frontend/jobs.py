from app import app, db
from flask import render_template, flash, redirect, request
from app.forms import JobForm
from bson.objectid import ObjectId
import pymongo
from app.lib.utils import mailer
from flask_weasyprint import HTML, render_pdf
from datetime import datetime


# display new request form
@app.route('/jobs/request/', methods=['GET', 'POST'])
def publicJob():
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.form)
        data = form.data

        # check if reference already exists
        #if data['reference']

        rate = getRate(data['translatefrom'], data['translateto'])
        total = int(data['wordcount'])*rate

        # manage tax
        tax = 'N/A'
        if tax != 'N/A':
            total = total*(1+tax)

        # create reference
        reference = getReference()

        # add info to job document
        data['status'] = 'quote'
        data['timestamp'] = datetime.now()
        data['total'] = total
        data['reference'] = reference

        # save job
        db.jobs.insert_one(data)
        quote_html = render_template('frontend/jobs/quote.html',
                                job=data,
                                rate=rate,
                                tax=tax,
                                reference=reference,
                                today=datetime.now())


        # generate pdf quote from html
        quote_filename = 'quote-' + reference + '.pdf'
        quote_pdf = render_pdf(HTML(string=quote_html))

        # save quote pdf file to disk
        #with open('storage/' + quote_filename, 'wb') as f:
        #    f.write(quote_pdf.get_data())

        # generate pdf text to translate from html
        text_filename = 'text-' + reference + '.pdf'
        text_pdf = render_pdf(HTML(string='<!DOCTYPE html><html lang="en"><body>' + data['text'].replace('\n', '<br>') + '</body></html>'))

        # save text pdf file to disk
        #with open('storage/' + text_filename, 'wb') as f:
        #    f.write(text_pdf.get_data())
        
        # send quote and text by email
        params = {}
        params['from'] = 'ALP Content Services <sales@al-arabic.com>'
        params['to'] = data['name'] + '<' + data['email'] + '>'
        params['reply_to'] = app.config['REPLY_TO']
        params['subject'] = 'ALP Content Services: quote #' + reference
        params['bcc'] = app.config['CRM_BCC']
        params['body'] = 'Dear ' + data['name'] + ',<br><br>Please find attached your quote reference #' + reference + '.<br><br>' \
                         'Reply to this email at <a href="mailto:sales@al-arabic.com">sales@al-arabic.com</a> or call us at +971 4 363 7757 / +971 50 465 8491 to discuss your project.'
        params['attachments'] = {quote_filename: quote_pdf.get_data(), text_filename: text_pdf.get_data()}

        # send email
        mailer.send_email(params)

        # redirect to confirmation page with messsage
        flash({
            'title': 'Quote #' + reference,
            'text': 'Dear ' + data['name'] + ',<br><br>Your quote #' + reference + ' has been sent to ' + data['email'] + '.<br><br>Thank you.'
        })
        return redirect('/confirm')

    else:
        return render_template('frontend/jobs/create.html',
                                contact=None,
                                article=None)


# display new request page with pre-filled data
@app.route('/jobs/<contact_id>/<article_id>/', methods=['GET', 'POST'])
def publicJobArticle(contact_id, article_id):
    # get article & contact
    article = db.articles.find_one({'_id': ObjectId(article_id)})
    contact = db.contacts.find_one({'_id': ObjectId(contact_id)})
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.form)
        data = form.data

        rate = getRate(data['translatefrom'], data['translateto'])
        total = int(data['wordcount'])*rate

        # manage tax
        tax = 'N/A'
        if tax != 'N/A':
            total = total*(1+tax)

        # create reference
        reference = getReference()

        # add info to job document
        data['status'] = 'quote'
        data['timestamp'] = datetime.now()
        data['total'] = total
        data['reference'] = reference
        db.jobs.insert_one(data)

        # calculate total amount
        data['total']=int(data['wordcount'])*rate

        # generate html quote
        quote_html = render_template('frontend/jobs/quote.html',
                                job=data,
                                rate=rate,
                                tax=tax,
                                reference=reference,
                                today=datetime.now())

        # generate pdf quote from html
        quote_filename = 'quote-' + reference + '.pdf'
        quote_pdf = render_pdf(HTML(string=quote_html))

        # generate pdf text to translate from html
        text_filename = 'text-' + reference + '.pdf'
        text_pdf = render_pdf(HTML(string='<!DOCTYPE html><html lang="en"><body>' + data['text'].replace('\n', '<br>') + '</body></html>'))

        # send quote and text by email
        params = {}
        params['from'] = 'ALP Content Services <sales@al-arabic.com>'
        params['to'] = data['name'] + '<' + data['email'] + '>'
        params['reply_to'] = app.config['REPLY_TO']
        params['subject'] = 'ALP Content Services: quote #' + reference
        params['bcc'] = app.config['CRM_BCC']
        params['body'] = 'Dear ' + data['name'] + ',<br><br>Please find attached your quote reference #' + reference + '.<br><br>' \
                         'Reply to this email at <a href="mailto:sales@al-arabic.com">sales@al-arabic.com</a> or call us at +971 4 363 7757 / +971 50 465 8491 to discuss your project.'
        params['attachments'] = {quote_filename: quote_pdf.get_data(), text_filename: text_pdf.get_data()}

        # send email
        mailer.send_email(params)

        # redirect to confirmation page with messsage
        flash({
            'title': 'Quote #' + reference,
            'text': 'Dear ' + data['name'] + ',<br><br>Your quote #' + reference + ' has been sent to ' + data['email'] + '.<br><br>Thank you.'
        })
        return redirect('/confirm')

    return render_template('frontend/jobs/create_article.html',
                                form=form,
                                contact=contact,
                                article=article)

# compute rate for language pair
# need to be moved to db/config
def getRate(lang_from, lang_to):
    if (lang_from, lang_to) == ('arabic', 'english') or (lang_from, lang_to) == ('english', 'arabic'):
        rate = 0.5
    else:
        rate = 0.8

    return rate

# generate quote reference from global counter
def getReference():
    db.refcounter.update({}, {'$inc': {'ct': 1}}, upsert=True)
    counter = db.refcounter.find_one({})
    counter = int(counter['ct'])
    counter = format(counter, "07d")
    #print counter
    return counter


