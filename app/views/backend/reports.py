from app import app, db
from flask import render_template, flash, redirect
from bson.objectid import ObjectId

# contacts index
@app.route('/admin/reports/')
def reports():
    reports = db.reports.find()
    return render_template('backend/reports/index.html',
                            reports=reports)

# view contact
@app.route('/admin/reports/<id>/')
def reportsView(id):
    report = db.report.find_one({ '_id': ObjectId(id) })
    if report:
        return render_template('backend/reports/view.html',
                                report=report)
    else:
        flash('report %s not found' %id)
        return redirect('/reports')
