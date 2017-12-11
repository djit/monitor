from app import app, db
from flask import render_template, flash, redirect
from app.forms import CrawlerForm
from bson.objectid import ObjectId
from subprocess import Popen, PIPE


# crawlers index
@app.route('/admin/crawlers/')
def crawlers():
    crawlers = db.crawlers.find()
    return render_template('backend/crawlers/index.html', crawlers=crawlers)

# add new crawlers
@app.route('/admin/crawlers/new/', methods=['GET', 'POST'])
def crawlersNew():
    form = CrawlerForm()
    if form.validate_on_submit():
        db.crawlers.insert_one(form.data)
        flash('New crawler  %s added' %(form.name.data))
        return redirect('/crawlers')
    return render_template('backend/crawlers/edit.html',
                                           form=form,
                                           title='New Crawler')

# view crawler
@app.route('/admin/crawlers/<id>/')
def crawlersView(id):
    crawler = db.crawlers.find_one({ '_id': ObjectId(id) })
    if crawler:
        return render_template('backend/crawlers/view.html',
                                               crawler=crawler)
    else:
        flash('crawler %s not found' %id)
        return redirect('/crawlers')

#edit crawler
@app.route('/admin/crawlers/<id>/edit/', methods=['GET', 'POST'])
def crawlersEdit(id):
    crawler = db.crawlers.find_one({ '_id': ObjectId(id) })
    if crawler:
        form = CrawlerForm(data=crawler)
        if form.validate_on_submit():
            db.crawlers.update({ '_id': ObjectId(id) }, form.data)
            return redirect('/crawlers')
        return render_template('backend/crawlers/edit.html',
                                               form=form,
                                               title='Crawler: '  + crawler['name'])
    else:
        flash('crawler %s not found' %id)
        return redirect('/crawlers')

# delete crawler
@app.route('/admin/crawlers/<id>/delete/')
def crawlersDelete(id):
    db.crawlers.remove(ObjectId(id))
    return redirect('/crawlers')


# run crawler
@app.route('/admin/crawlers/<id>/run/')
def crawlersRun(id):
    try:
        crawler = db.crawlers.find_one({ '_id': ObjectId(id) })
        result = ''
        '''
        if crawler:
            spider = ZawyaSpider(domain='zawya.com')
            crawler = Crawler(Settings())
            crawler.configure()
            crawler.crawl(spider)
            crawler.start()
            log.start()
            reactor.run() # the script will block here
        '''
    except Exception as e:
        print(e)
        return 'KO'

# store crawl result in logs collection
def storeCrawlResult(result):
    print(type(result))
    db.logs.insert_one(result)
