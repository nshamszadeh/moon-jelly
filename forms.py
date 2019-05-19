from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField, FormField, FieldList, IntegerField
from werkzeug.datastructures import MultiDict

# some web forms and what not

class LoginForm(FlaskForm):
	email = StringField('Email', [validators.Email(message = 'Please Enter A Valid Email')])

class UserForm(FlaskForm):
	specialties = [ ('Pediatrician', 'Pediatrician'), ('Cardiologist', 'Cardiologist'), 
	('General Surgeon', 'General Surgeon'), ('Other', 'Other') ]
	first_name = StringField('First Name', [validators.DataRequired(message = 'Please Enter Something')])
	last_name = StringField('Last Name', [validators.DataRequired(message = 'Please Enter Something')])
	email = StringField('Email', [validators.Email(message = 'Please Enter A Valid Email')])
	specialty = SelectField('Specialty', choices = specialties)

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
	NumberUsersM = IntegerField('# Working on Monday', [validators.DataRequired(message = 'Please Enter Something')])
	NumberUsersT = IntegerField('# Working on Tuesday', [validators.DataRequired(message = 'Please Enter Something')])
	NumberUsersW = IntegerField('# Working on Wednesday', [validators.DataRequired(message = 'Please Enter Something')])
	NumberUsersTh = IntegerField('# Working on Thursday', [validators.DataRequired(message = 'Please Enter Something')])
	NumberUsersF = IntegerField('# Working on Friday', [validators.DataRequired(message = 'Please Enter Something')])
	NumberUsersS = IntegerField('# Working on Saturday', [validators.DataRequired(message = 'Please Enter Something')])
	NumberUsersSu = IntegerField('# Working on Sunday', [validators.DataRequired(message = 'Please Enter Something')])