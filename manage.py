import os
from app import create_app, db
from flask_script import Manager, Shell
from app.models import User, Record

app = create_app(os.getenv('BOOKING_CONFIG') or 'default')
manage = Manager(app)

def make_context_shell():
    return dict(app=app, db=db, User=User, Record=Record)

manage.add_command('shell', Shell(make_context=make_context_shell))

if __name__ == '__main__':
    manage.run()