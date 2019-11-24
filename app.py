import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import listener
from models import Book, db

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
socketio = SocketIO(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)

thread1 = listener.myThread(1, 1)
thread1.start()


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/add")
def add_user():
    name = request.args.get('name')
    # author=request.args.get('author')
    # published=request.args.get('published')

    try:
        book = Book(
            name=name
        )
        db.session.add(book)
        db.session.commit()
        return "User with name {} added. user id={}".format(name, book.id)
    except Exception as e:
        return(str(e))


@app.route("/del/<id_>")
def del_user(id_):
    try:
        Book.query.filter_by(id=id_).delete()
        db.session.commit()
        return "User with id {} deleted".format(id_)
    except Exception as e:
        return(str(e))


@app.route("/getall")
def get_all():
    try:
        books = Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return(str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return(str(e))


# TODO: add update function

@socketio.on('connect')  # global namespace
def handle_connect():
    print('Client connected')


@socketio.on('connect', namespace='/somevent')
def handle_chat_connect():
    print('Client connected to chat namespace')
    emit('chat message', 'welcome!')


if __name__ == '__main__':
    socketio.run(app, debug=True)
