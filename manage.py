import os
from imp import reload

from app import create_app, db
from flask_script import Manager, Shell
from app.models import User, Record, Outlay
from flask_migrate import MigrateCommand, Migrate
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = create_app(os.getenv('BOOKING_CONFIG') or 'default')
manage = Manager(app)
migrate = Migrate(app, db)

def make_context_shell():
    return dict(app=app, db=db, User=User, Record=Record, Outlay=Outlay)

manage.add_command('shell', Shell(make_context=make_context_shell))
manage.add_command('db', MigrateCommand)

@manage.command
def deploy():
    from flask_migrate import upgrade

    upgrade()

    Outlay.insert_outlays()

if __name__ == '__main__':
    manage.run()