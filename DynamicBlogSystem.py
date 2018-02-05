import os

import pymysql
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from app import create_app, db
from app.models import User

pymysql.install_as_MySQLdb()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
    manager.run()
