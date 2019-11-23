import os
import select
import threading

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

import listener

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
from models import Book

thread1 = listener.myThread(1, 1)
thread1.start()

@app.route("/")
def hello():
    return "Hello tier!"


@app.route("/add")
def add_user():
    name=request.args.get('name')
    # author=request.args.get('author')
    # published=request.args.get('published')
    
    try:
        book=Book(
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
        books=Book.query.all()
        return  jsonify([e.serialize() for e in books])
    except Exception as e:
        return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return(str(e))


if __name__ == '__main__':
    app.run()
