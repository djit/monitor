from app import app, db
from flask import render_template, flash, redirect, request
from bson.objectid import ObjectId
import pymongo

# job index
@app.route('/admin/jobs/')
def jobs():
    jobs = db.jobs.find().sort('timestamp', pymongo.DESCENDING)
    return render_template('backend/jobs/index.html',
                            jobs=jobs)

# view job
@app.route('/admin/jobs/<id>/')
def jobsView(id):
    job = db.jobs.find_one({'_id': ObjectId(id)})
    if job:
        return render_template('backend/jobs/view.html',
                                job=job)
    else:
        flash('job %s not found' %id)
        return redirect('/backend/jobs')

# delete job
@app.route('/admin/jobs/<id>/delete/')
def jobsDelete(id):
    db.jobs.remove(ObjectId(id))
    return redirect('/admin/jobs')

# delete multiple jobs
@app.route('/admin/jobs/<ids>/delete_all/')
def jobsDeleteAll(ids):
    ids = ids.split('$')[:-1]
    ids = [ObjectId(id) for id in ids ]
    db.jobs.remove({ '_id': { '$in': ids } } )
    return redirect('/admin/jobs')
