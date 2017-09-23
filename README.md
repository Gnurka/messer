# messer
Message RESTful web service. 

## Requirements
* Flask: http://flask.pocoo.org/
* Peewee: http://docs.peewee-orm.com/

## Usage:
Start local server with:  
`python app.py`

and it can be accessed at http://localhost:5555/

## Commands:
__GET /users/1/messages?start_id=1&end_id=5__  
Gets messages with ids between 1-5 for user 1.

__POST /users/1/messages__  
Send a message to user 1. The body should contain the text to be sent in parameter "text".

__POST /users/1/messages/read__  
Get unread messages for user 1 and mark them as read.

__DELETE /messages/1;2;3__  
Deletes messages 1, 2 and 3.
