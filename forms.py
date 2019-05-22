from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, FormField, FieldList, IntegerField, PasswordField, BooleanField
from werkzeug.datastructures import MultiDict

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
	is_cardio = BooleanField('Cardiologist?')

class DeleteForm(FlaskForm):
	first_name = StringField('First Name', [validators.DataRequired(message = 'Please Enter Something')])

class ScheduleEntryForm(FlaskForm):
	first_name = StringField('First Name', [validators.DataRequired(message = 'Please Enter Something')])

class ScheduleForm(FlaskForm):
	userfirstNamesSu = FieldList(FormField(ScheduleEntryForm), min_entries=1)
	userfirstNamesM = FieldList(FormField(ScheduleEntryForm), min_entries=1)
	userfirstNamesT = FieldList(FormField(ScheduleEntryForm), min_entries=1)
	userfirstNamesW = FieldList(FormField(ScheduleEntryForm), min_entries=1)
	userfirstNamesTh = FieldList(FormField(ScheduleEntryForm), min_entries=1)
	userfirstNamesF = FieldList(FormField(ScheduleEntryForm), min_entries=1)
	userfirstNamesS = FieldList(FormField(ScheduleEntryForm), min_entries=1)

class NumberUsersForm(FlaskForm):
	NumberUsersSu = IntegerField('# Working on Sunday', [validators.DataRequired(message = 'Please Enter Something')], default=1)
	NumberUsersM = IntegerField('# Working on Monday', [validators.DataRequired(message = 'Please Enter Something')], default=1)
	NumberUsersT = IntegerField('# Working on Tuesday', [validators.DataRequired(message = 'Please Enter Something')], default=1)
	NumberUsersW = IntegerField('# Working on Wednesday', [validators.DataRequired(message = 'Please Enter Something')], default=1)
	NumberUsersTh = IntegerField('# Working on Thursday', [validators.DataRequired(message = 'Please Enter Something')], default=1)
	NumberUsersF = IntegerField('# Working on Friday', [validators.DataRequired(message = 'Please Enter Something')], default=1)
	NumberUsersS = IntegerField('# Working on Saturday', [validators.DataRequired(message = 'Please Enter Something')], default=1)