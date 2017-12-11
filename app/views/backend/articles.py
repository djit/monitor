from app import app, db
from flask import render_template, flash, redirect, request, jsonify
from bson.objectid import ObjectId
import pymongo
from bson.code import Code
from app.forms import ContactForm
import json, re
from datetime import datetime, timedelta


# articles index
@app.route('/admin/articles/')
def articles():
    status = request.args.get('status')
    today = datetime.today()
    yesterday = datetime.now() - timedelta(days=1)
    articles = db.articles.find({'status': {'$ne': 'archived'}}).sort('pub_date', pymongo.DESCENDING)
    if status:
        if status != 'today':
            articles = db.articles.find({'status': status}).sort('pub_date', pymongo.DESCENDING)
        else:
            articles = db.articles.find({ 'pub_date': { '$gte': today } }).sort('pub_date', pymongo.DESCENDING)
    today = today.date()
    yesterday = yesterday.date()

    return render_template('backend/articles/index.html',
                            articles=articles,
                            count=articles.count(),
                            today=today,
                            yesterday=yesterday)

# view article
@app.route('/admin/articles/<id>/')
def articlesView(id):
    article = db.articles.find_one({ '_id': ObjectId(id) })
    if article:
        form = ContactForm()
        return render_template('backend/articles/view.html',
                                article=article,
                                form=form)
    else:
        flash('article %s not found' %id)
        return redirect('/articles')

# delete article
@app.route('/admin/articles/<id>/delete/')
def articlesDelete(id):
    db.articles.remove(ObjectId(id))
    return redirect('/admin/articles')

# delete multiple articles
@app.route('/admin/articles/<ids>/delete_all/')
def articlesDeleteAll(ids):
    ids = ids.split('$')[:-1]
    ids = [ObjectId(id) for id in ids ]
    db.articles.remove({ '_id': { '$in': ids } } )
    return redirect('/admin/articles')

# ajax update article
@app.route('/admin/articles/<id>/', methods=['PATCH'])
def articlesUpdate(id):
    data = json.loads(request.data)
    db.articles.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({'status': '200', 'message': 'OK'})

# live search
@app.route('/admin/articles/search/', defaults={'query': ''})
@app.route('/admin/articles/search/<query>')
def articlesSearch(query):
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    if len(query) > 0:
        query = re.compile(query, re.IGNORECASE)
        articles = db.articles.find({'$and': [{ 'status': {'$ne': 'archived'} }, { '$or': [{'title': {'$regex': query}}, {'source': {'$regex': query}}, {'body': {'$regex': query}}] } ]}).sort('pub_date', pymongo.DESCENDING)
    else:
        articles = db.articles.find({'status': {'$ne': 'archived'}}).sort('pub_date', pymongo.DESCENDING)
    data = render_template('backend/articles/list.html',
                            articles=articles,
                            count=articles.count(),
                            today=today,
                            yesterday=yesterday)
    return jsonify({
        'data': data,
        'count': articles.count(),
        'today': today,
        'yesterday': yesterday
    })
