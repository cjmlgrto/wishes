from peewee import *

db = SqliteDatabase('members.db')

class Member(Model):
	id = PrimaryKeyField()
	name = CharField()
	wishlist = TextField()
	metrics = TextField()

	class Meta:
		database = db

def init():
	db.connect()
	db.create_tables([Member], safe=True)