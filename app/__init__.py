# Import flask and template operators
from flask import Flask
from flask_pymongo import pymongo
from pymongo import MongoClient
import re
from jinja2 import evalcontextfilter, Markup, escape
from app.lib.utils.logger import mongoLogger
import config


app = Flask(__name__)

app.config.from_object('config')
app.config.from_envvar('ENV_SETTINGS',silent=True)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# nl2br filter
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'<br>'.join(_paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

# mongodb
db = MongoClient(app.config['DB_SERVER'], connect=False)[app.config['DB_NAME']]

# import all modules in views
import views.backend, views.frontend, views.test
