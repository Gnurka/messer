"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from datetime import datetime
from flask import Flask, jsonify, request, redirect, url_for, abort, make_response
from playhouse.shortcuts import model_to_dict

from models import User, Message

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


def find_message(message_id):
    message = [m for m in messages if m.id == message_id]
    if (len(message) == 0):
        abort(404)

    return message[0]

def get_user(user_id):
    try:
        return User.get(id = user_id)
    except User.DoesNotExist:
        abort(404)

# Also handle filters like ?start_id=1&end_id=5
@app.route('/users/<int:user_id>/messages', methods = ['GET'])
def list(user_id):
    start_id = request.args.get('start_id')
    end_id = request.args.get('end_id')

    u = get_user(user_id)

    messages = u.messages
    if (start_id is not None and end_id is not None):
        # Check for end_id >= start_id?
        try:
            messages = Message.select().where(Message.id >= int(start_id) and Message.id <= int(end_id))
        except Message.DoesNotExist:
            abort(404)

    return jsonify([model_to_dict(m) for m in messages])


# @app.route('/users/<int:user_id>/messages/unread/', methods = ['GET'])
# def list_unread(user_id):
#     return jsonify([m.json() for m in messages if m.user_id == user_id and m.read == False])

# @app.route('/users/<int:user_id>/messages/read/', methods = ['POST'])
# def read(user_id):
#     unread = [m for m in messages if m.user_id == user_id and m.read == False]
#     for m in unread:
#         m.read = True

#     return jsonify([m.json() for m in unread])

# @app.route('/message/<int:message_id>/', methods = ['GET'])
# def detail(message_id):
#     message = find_message(message_id)
#     return jsonify(message.json())


@app.route('/users/<int:user_id>/messages', methods = ['POST'])
def send(user_id):
    u = get_user(user_id)
    text = request.form['text']

    if text is None:
        abort(400)

    m = Message.create(text = text, date = datetime.now(), read = False, receiver = u)

    return jsonify(model_to_dict(m)), 201


# @app.route('/message/<int:message_id>/', methods = ['DELETE'])
# def delete(message_id):
#     message = find_message(message_id)
#     messages.remove(message)
#     return jsonify({'result': True})


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