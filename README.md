# messer
Message RESTful web service

Usage:
Start local server with:
python app.py

and it can be accessed at http://localhost:5555/

Commands:
GET /users/1/messages?start_id=1&end_id=5
Gets messages with ids between 1-5 for user 1.

POST /users/1/messages
Send a message to user 1. The body should contain the text to be sent in parameter "text".

POST /users/1/messages/read
Get unread messages for user 1 and mark them as read.

DELETE /messages/1;2;3
Deletes messages 1, 2 and 3.
