from app import app, socketio
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
    host='0.0.0.0', port=app.config['PORT']))


@manager.command
def run():
    socketio.run(app,
                 host='0.0.0.0',
                 port=app.config['PORT'])


if __name__ == '__main__':
    manager.run()
