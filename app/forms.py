from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, HiddenField, FieldList, TextField, TextAreaField
from wtforms.fields.core import UnboundField
from wtforms.validators import DataRequired, InputRequired
from bson.objectid import ObjectId




# Source form
class SourceForm(Form):
    name = StringField('name', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])
    crawler = SelectField('crawler', choices=[('', 'Select a crawler')])

# Crawler form
class CrawlerForm(Form):
    name = StringField('name', validators=[DataRequired()])
    type = SelectField(u'Crawler type', choices=[('web', 'web'), ('xml', 'xml'), ('text', 'Plain Text')])
    status = BooleanField('status', False)
    spider = StringField('spider', validators=[DataRequired()])


#Contact form
class ContactForm(Form):
    

    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[])
    organization = StringField('organization')
    position = StringField('position')
    mobile = StringField('mobile')
    landline = StringField('landline')
    articles = FieldList(TextField('articles'))
    preferences = {'articles_notify': SelectField(u'Notification preferences', choices=[('default', 'default'),
                                                                    ('daily', 'daily'),
                                                                    ('weekly', 'weekly'),
                                                                    ('unsubscribed', 'unsubscribed')
                                                                    ])
    }

# Accounts form
class AccountForm(Form):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

# Job form
class JobForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    organization = StringField('organization')
    translatefrom = SelectField('translatefrom', choices=[])
    translateto = SelectField('translateto', choices=[])
    wordcount = StringField('wordcount')
    text = TextAreaField('text', validators=[DataRequired()])


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
