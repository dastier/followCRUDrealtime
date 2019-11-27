import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO

import listener
from models import User, db

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
socketio = SocketIO(app, async_mode='threading')


CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)

thread1 = listener.myThread("db listener", 1)
thread1.daemon = True
thread1.start()


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/add", methods=['POST'])
def add_user():
    name = request.args.get('name')

    try:
        user = User(
            name=name
        )
        db.session.add(user)
        db.session.commit()
        return "User with name {} added. user id={}".format(name, user.id)
    except Exception as e:
        return(str(e))


@app.route("/del/<int:id_>", methods=['DELETE'])
def del_user(id_):
    if User.query.filter_by(id=id_).first():
        try:
            User.query.filter_by(id=id_).delete()
            db.session.commit()
            return "User with id {} deleted".format(id_)
        except Exception as e:
            return(str(e))
    else:
        return "User with id {} does not exist".format(id_)


@app.route("/getall", methods=['GET'])
def get_all():
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as e:
        return(str(e))


@app.route("/get/<int:id_>", methods=['GET'])
def get_by_id(id_):
    try:
        user = User.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return(str(e))


# TODO: add update function


def send_mymsg(msg):
    with app.test_request_context('/'):
        socketio.emit('testtask1', msg, namespace='/')


if __name__ == '__main__':
    socketio.run(app)
