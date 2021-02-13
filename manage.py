from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from website import create_app
from website import db

app = create_app()
migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand) #py manage.py db _____

if __name__ == '__main__':
    manager.run()