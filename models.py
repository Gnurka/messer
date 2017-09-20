from peewee import *

db = SqliteDatabase('db.messages')

class User(Model):
	mail = CharField()

	def __repr__(self):
		return self.mail

	class Meta:
		database = db

class Message(Model):
	text = CharField()
	date = DateTimeField()
	read = BooleanField()
	receiver = ForeignKeyField(User, related_name='messages')

	def __repr__(self):
		return self.text

	class Meta:
		database = db
