import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication
from app import app
import base64

# send mail
def send_email(params):
    msg = MIMEMultipart()
    msg['From'] = params['from']
    msg['To'] = str(params['to'])
    msg['Subject'] = params['subject']
    
    cc = None
    if 'cc' in params:
        cc = params['cc']
    bcc = None
    if 'bcc' in params:
        bcc = params['bcc']

    if 'body' in params:
        msg.attach(MIMEText(params['body'], 'html'))
    if 'attachments' in params:
        if len('attachments') > 0:
            for filename, data in params['attachments'].iteritems():
                attachment = MIMEApplication(data, 'pdf')
                attachment.add_header('Content-Disposition', 'attachment; filename=%s' % filename)
                msg.attach(attachment)

    reply_to = None
    if 'reply_to' in params:
        msg.add_header('Reply-To', params['reply_to'])

    # build dest list with cc, bcc is specified
    to = [str(params['to'])]
    if cc:
        if type(cc) in [str, unicode]:
            msg.add_header('Cc', cc)
            cc = [cc]
        else:
            cc = ', '.join(cc)
            msg.add_header('Cc', cc)
        to += cc

    if bcc:
        if type(bcc) in [str, unicode]:
            bcc = [bcc]
        to += bcc

    server = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    text = msg.as_string()
    try:
        server.sendmail(msg['From'], to , text)
    except Exception as e:
        print('Error:', e)
    finally:
        server.quit()
