from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            
            mail.send(msg)

        except Exception as e:
            return str(e)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    try:
        
        msg = Message(app.config['OGDENRENT_MAIL_SUBJECT_PREFIX'] + ' ' + subject, 
                    sender=app.config['OGDENRENT_MAIL_SENDER'], 
                    recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        # msg.body = render_template(template + '.txt', 'body')
        msg.html = render_template(template + '.html',  **kwargs)

        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr

    except Exception as e:
        return str(e)

