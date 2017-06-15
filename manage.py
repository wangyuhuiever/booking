import os
from app import create_app, db
from flask_script import Manager, Shell
from app.models import User, Record
from flask_migrate import MigrateCommand, Migrate

app = create_app(os.getenv('BOOKING_CONFIG') or 'default')
manage = Manager(app)
migrate = Migrate(app, db)

def make_context_shell():
    return dict(app=app, db=db, User=User, Record=Record)

manage.add_command('shell', Shell(make_context=make_context_shell))
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()