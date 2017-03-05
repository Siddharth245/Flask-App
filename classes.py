#Three classes are used to handle the user activity


from werkzeug import generate_password_hash, check_password_hash

#the user class stores the user details entered while signing in
class user(object):
	
	def __init__(self, first_name, last_name, email, password):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.pwd = self.set_password(password)
	
	def store(self):
		
		my_file = open("database.txt", "a")
		my_file.write(self.first_name+" ")
		my_file.write(self.last_name+" ")
		my_file.write(self.email+" ")
		my_file.write(self.pwd+"\n")	 
		my_file.close()

	def set_password(self, password):
		return generate_password_hash(password)

	
#the login user class handles the user authentication 
class loginuser(object):
	userinfo = []
	
	def __init__(self, email):
		self.email = email

	def existcheck(self,email):
		my_file = open("database.txt", "r")
		for lines in my_file:
			userinfo = lines.split(' ')
			if userinfo[2]==email:
				self.first_name = userinfo[0]
				self.last_name = userinfo[1]
				self.email = userinfo[2]
				pwdhash = userinfo[3]		
				return userinfo
		my_file.close()
		return None		
		

	def check_password(self, password,pwdhash):
		return check_password_hash(pwdhash, password)

#the filesave class is used to save the captions for images in the filecaptions.txt
class filesave(object):

	def __init__(self, caption):
		self.caption = caption	

	def storefile(self):
		my_file = open("filecaptions.txt", "a")
		my_file.write(self.caption+" \n")
