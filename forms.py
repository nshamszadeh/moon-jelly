from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, PasswordField, BooleanField

# some web forms and what not

class LoginForm(FlaskForm):
	email = StringField('Email', [validators.Email(message = 'Please Enter A Valid Email')])
	password = PasswordField('Password')
	remember_me = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
	email = StringField('Email', [validators.Email(message = 'Please Enter A Valid Email')])
	first_name = StringField('First Name', [validators.DataRequired(message = 'Please Enter Something')])
	last_name = StringField('Last Name', [validators.DataRequired(message = 'Please Enter Something')])
	password = PasswordField('Password')
	is_cardio = SelectField('Cardiologist?', choices=[('True', 'Yes'), ('False', 'No')])

class UserForm(FlaskForm):
	first_name = StringField('First Name', [validators.DataRequired(message = 'Please Enter Something')])
	last_name = StringField('Last Name', [validators.DataRequired(message = 'Please Enter Something')])
	email = StringField('Email', [validators.Email(message = 'Please Enter A Valid Email')])
	is_cardio = SelectField('Cardiologist?', choices=[('True', 'Yes'), ('False', 'No')])	
	is_admin = SelectField('Administrator? (can add/remove users)', choices=[('False', 'No'), ('True', 'Yes')])

class DeleteForm(FlaskForm):
	first_name = StringField('First Name', [validators.DataRequired(message = 'Please Enter Something')])
	last_name = StringField('Last Name')
	email = StringField('Email')

class SetPasswordForm(FlaskForm):
	