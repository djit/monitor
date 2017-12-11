import os, sys
from app import app, db
from flask import render_template, flash, redirect, request
from app.forms import SourceForm
from bson.objectid import ObjectId
import logging

from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings


# sources index
@app.route('/admin/sources/')
def sources():
    sources = db.sources.find()
    return render_template('backend/sources/index.html', sources=sources)

# add new sources
@app.route('/admin/sources/new/', methods=['GET', 'POST'])
def sourcesNew():
    if request.method == 'POST':
        form = SourceForm(request.form)
        if form.validate():
            db.sources.insert_one(form.data)
            flash('New source  %s added' %(form.name.data))
            return redirect('/admin/sources')
        else:
            return render_template('backend/sources/edit.html',
                                    form=form,
                                    title='New source')
    form = SourceForm()
    crawlers = db.crawlers.find()
    form.crawler.choices.extend((str(c['_id']), c['name']) for c in crawlers)
    return render_template('backend/sources/edit.html',
                            form=form,
                            title='New source')


# view source
@app.route('/admin/sources/<id>/')
def sourcesView(id):
    source=db.sources.find_one({ '_id': ObjectId(id) })
    if source:
        return render_template('backend/sources/view.html',
                                source=source)
    else:
        flash('Source %s not found' %id)
        return redirect('/admin/sources')

#edit source
@app.route('/admin/sources/<id>/edit/', methods=['GET', 'POST'])
def sourcesEdit(id):
    source = db.sources.find_one({ '_id': ObjectId(id) })
    if source:
        if request.method == 'POST':
            form = SourceForm(request.form)
            if form.validate():
                db.sources.update({ '_id': ObjectId(id) }, form.data)
                return redirect('/admin/sources')
            else:
                return render_template('backend/sources/edit.html',
                                        form=form,
                                        title='Source: ' + source['name'])
        form=SourceForm(data=source)
        crawlers = db.crawlers.find()
        form.crawler.choices.extend((str(c['_id']), c['name']) for c in crawlers)
        return render_template('backend/sources/edit.html',
                                form=form,
                                title='Source: ' + source['name'])
    else:
        flash('source %s not found' %id)
    return redirect('/admin/sources')
'''

def sourcesEdit(id):
    source = db.sources.find_one({ '_id': ObjectId(id) })
    if source:
        crawlers=db.crawlers.find()
        form=SourceForm(data=source)
        form.crawler.choices = [(c['_id'], c['name']) for c in crawlers]
        if form.validate_on_submit():
            db.sources.update({ '_id': ObjectId(id) }, form.data)
            return redirect('/sources')
        return render_template('backend/sources/edit.html',
                                form=form,
                                title='Source: ' + source['name'])
    else:
        flash('Source %s not found' %id)
        return redirect('/sources')
'''

# delete source
@app.route('/admin/sources/<id>/delete/')
def sourcesDelete(id):
    db.sources.remove(ObjectId(id))
    return redirect('/sources')

# return crawler document for this source
@app.context_processor
def utility_processor():
    def crawler(id):
        crawler=db.crawlers.find_one({ '_id': ObjectId(id) })
        return crawler
    return dict(crawler=crawler)

# run crawler
@app.route('/admin/sources/<id>/crawl')
def crawl(id):
    try:
        # retrieve source document
        source = db.sources.find_one({'_id': ObjectId(id)})
        source_crawler_id = source['crawler']

        # retrieve crawler document
        crawler = db.crawlers.find_one({'_id': ObjectId(source_crawler_id)})
        crawler_name = crawler['name']
        spider_name = crawler['spider']

        # call crawlermgr

        return 'job will get result here'
    except Exception as e:
        logging.exception('error running crawl job')
        return 'error running crawl job'


def spider_closing(spider):
    """Activates on spider closed signal"""
    log.msg("Closing reactor", level=log.INFO)
    reactor.stop()
