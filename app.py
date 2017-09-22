"""
The Messer message web service

TODO:
* Add URI:s?
* Add ways to list users and create them?

"""
from datetime import datetime
from flask import Flask, jsonify, request, redirect, url_for, abort, make_response
from playhouse.shortcuts import model_to_dict

from models import User, Message

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


def get_object_or_404(object, object_id):
    try:
        return object.get(id = object_id)
    except object.DoesNotExist:
        abort(404)


# TODO: Check for each of the filters. Maybe make into one instead like ?range=1,3
# Get messages for a user. Ex: GET /users/1/messages?start_id=1&end_id=3
@app.route('/users/<int:user_id>/messages', methods = ['GET'])
def list(user_id):
    start_id = request.args.get('start_id')
    end_id = request.args.get('end_id')

    # Is it needed to first get the user? Maybe just query the messages
    u = get_object_or_404(User, user_id)

    messages = u.messages
    if (start_id is not None and end_id is not None):
        # Check for end_id >= start_id?
        try:
            messages = u.messages.where(Message.id >= int(start_id) and Message.id <= int(end_id)).order_by(Message.date)
        except Message.DoesNotExist:
            abort(404)

    return jsonify([model_to_dict(m) for m in messages])


# Get unread messages and mark them as read. Ex: POST /users/1/messages/read
@app.route('/users/<int:user_id>/messages/read', methods = ['POST'])
def read(user_id):
    user = get_object_or_404(User, user_id)
    unread_messages = [model_to_dict(m) for m in user.messages.select().where(Message.read == False)]

    # Set messages to read. Not very atomic?
    if (len(unread_messages) > 0):
        query = Message.update(read=True).where(Message.receiver == user_id and Message.read == False)
        query.execute()

    return jsonify(unread_messages)


# Send a message to a user. Ex: POST /users/1/messages. POST body should contain parameter 'text' containing the message to be sent.
@app.route('/users/<int:user_id>/messages', methods = ['POST'])
def send(user_id):
    u = get_object_or_404(User, user_id)
    text = request.form['text']

    if text is None:
        abort(400)

    m = Message.create(text = text, date = datetime.now(), read = False, receiver = u)

    return jsonify(model_to_dict(m)), 201


# Add semi-colon separated list of message ids. Ex: DELETE /messages/1;2;3
# TODO: Add users to route?
@app.route('/messages/<string:message_ids>', methods = ['DELETE'])
def delete(message_ids):
    try:
        id_list = [int(m) for m in message_ids.split(';')]
    except ValueError:
        abort(400)

    # Check that all messages exist before deleting them.
    message_list = []
    for id in id_list:
        message_list.append(get_object_or_404(Message, id))

    for message in message_list:
        message.delete_instance()
    
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)