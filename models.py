from flask.ext.login import UserMixin

class User(UserMixin):
	email = ""

	def __init__(self, userid, password):
	    self.id = userid
	    self.password = password
	