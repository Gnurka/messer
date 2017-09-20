"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from datetime import datetime
from flask import Flask, jsonify, request, redirect, url_for, abort, make_response

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

class Message:
    def __init__(self, id, text, date, user_id):
        self.id = id
        self.text = text
        self.date = date
        self.user_id = user_id
        self.read = False

    def json(self):
        return {
            'id': self.id, 
            'text': self.text, 
            'date': self.date, 
            'user_id': self.user_id, 
            'read': self.read
            }

class User:
    def __init__(self, id, mail):
        self.id = id
        self.mail = mail

    def json(self):
        return {
            'id': self.id, 
            'mail': self.mail
        }

users = [User(1, 'Gustav'), User(2, 'Malin')]
messages = [Message(1, 'Hejsan Malin', datetime(year=2017, month=9, day=19), 2), 
            Message(2, 'Hej Gustav.', datetime(year=2017, month=9, day=20), 1), 
            Message(3, 'Ska vi äta lunch?', datetime(year=2017, month=9, day=21), 2)]

def find_message(message_id):
    message = [m for m in messages if m.id == message_id]
    if (len(message) == 0):
        abort(404)

    return message[0]


# Also handle filters like ?start_id=1&end_id=5
@app.route('/users/<int:user_id>/messages/', methods = ['GET'])
def list(user_id):
    start_id = request.args.get('start_id')
    end_id = request.args.get('end_id')
    user_messages = [m for m in messages if m.user_id == user_id]

    if (start_id is not None and end_id is not None):
        user_messages = [m for m in user_messages if m.id >= int(start_id) and m.id <= int(end_id)]

    return jsonify([m.json() for m in user_messages])


@app.route('/users/<int:user_id>/messages/unread/', methods = ['GET'])
def list_unread(user_id):
    return jsonify([m.json() for m in messages if m.user_id == user_id and m.read == False])

@app.route('/users/<int:user_id>/messages/read/', methods = ['POST'])
def read(user_id):
    unread = [m for m in messages if m.user_id == user_id and m.read == False]
    for m in unread:
        m.read = True

    return jsonify([m.json() for m in unread])

@app.route('/message/<int:message_id>/', methods = ['GET'])
def detail(message_id):
    message = find_message(message_id)
    return jsonify(message.json())


@app.route('/message/', methods = ['POST'])
def send():
    text = request.form['text']
    messages.append(Message(len(messages)+1, text))
    return redirect(url_for('list'))


@app.route('/message/<int:message_id>/', methods = ['DELETE'])
def delete(message_id):
    message = find_message(message_id)
    messages.remove(message)
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)