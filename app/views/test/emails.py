from app import app, db
from flask import render_template, flash, redirect, request, jsonify, Response
from app.lib.utils import mailer
from app.lib.utils.logger import mongoLogger


# ---------- tests --------------------------

@app.route('/admin/test')
def testEmail():
    return render_template('emails/congrats-2.html',
                            contact_name='SENDER',
                            title="Alghanim Industries Unveils Plans for Wendy's Expansion into Kingdom of Saudi Arabi",
                            article_link='http://www.zawya.com/mena/en/story/ZAWYA20160622055858',
                            link=app.config['SERVER_URL'] + '/jobs/57692085cf370a140ba0ed26/576a2ced0be71c127781d3b5',
                            host=app.config['SERVER_URL'],
                            token='token')
