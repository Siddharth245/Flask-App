from flask_wtf import Form, FlaskForm 
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

#signup form class used to initiate object instances to capture the different fields of user information
#passwords are stored in hashes for security
class SignupForm(Form):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  submit = SubmitField('Sign up')

#login form class is used to verify and authenticate the users
class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
	submit = SubmitField('Sign in')

#caption field class is used to obtain the caption and file information for user images 
class CaptionField(FlaskForm):
	photo = FileField('Choose File', validators=[FileRequired()])
	caption = StringField('Caption')
	submit = SubmitField('Upload')
