import os

import listener
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO
from models import User, db

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
socketio = SocketIO(app, async_mode='threading')


CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)
app.logger.info('database is initialized')

thread1 = listener.myThread("db listener", 1)
thread1.daemon = True
thread1.start()


@app.route("/")
def root():
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
        app.logger.info(
            "User with name %s added. user id=%s" % (name, user.id))
        return "User with name %s added. user id=%s" % (name, user.id), 201
    except Exception as e:
        app.logger.error(str(e))
        return (str(e)), 500


@app.route("/update/<id_>", methods=['PUT'])
def update_user(id_):
    name = request.args.get('name')
    if User.query.filter_by(id=id_).first():
        try:
            User.query.filter_by(id=id_).update({"name": name})
            db.session.commit()
            app.logger.info(
                "User with id %s updated. Got new name: %s" % (id_, name))
            return "User with id %s updated" % (id_), 200
        except Exception as e:
            app.logger.error(str(e))
            return(str(e)), 500
    else:
        return "User with id %s does not exist" % (id_), 404


@app.route("/delete/<int:id_>", methods=['DELETE'])
def del_user(id_):
    if User.query.filter_by(id=id_).first():
        try:
            User.query.filter_by(id=id_).delete()
            db.session.commit()
            return "User with id %s deleted" % (id_), 200
        except Exception as e:
            app.logger.error(str(e))
            return(str(e))
    else:
        return "User with id %s does not exist" % (id_), 404


@app.route("/users", methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users]), 200
    except Exception as e:
        app.logger.error(str(e))
        return(str(e)), 500


@app.route("/user/<int:id_>", methods=['GET'])
def get_by_id(id_):
    if User.query.filter_by(id=id_).first():
        try:
            user = User.query.filter_by(id=id_).first()
            return jsonify(user.serialize()), 200
        except Exception as e:
            app.logger.error(str(e))
            return (str(e)), 500
    else:
        return "User with id %s does not exist" % (id_), 404


def send_op_msg(msg):
    with app.test_request_context('/'):
        socketio.emit('testtask1', msg, namespace='/')


if __name__ == '__main__':
    socketio.run(app)
