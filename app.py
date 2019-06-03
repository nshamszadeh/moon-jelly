import os
import subprocess
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, UserForm, DeleteForm, RegisterForm, SetPasswordForm, EmailForm, ScheduleForm, ScheduleEntryForm, NumberUsersForm

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from io import StringIO
from xhtml2pdf import pisa


import csv
from flask import Flask, make_response, render_template
from flask import Flask, request, jsonify
#import flask_excel as excel

import pdfkit 

from flask import Flask, flash, request, redirect, url_for
from flask_table import Table, Col 
from flask import Flask, render_template, redirect, url_for
#from flask_mail import Mail, Message

from flask_mail import Mail, Message
from flask import make_response, Flask, render_template, request, redirect, send_from_directory, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_table import Table, Col
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import psycopg2
#import pandas
import os.path

app = Flask(__name__)
#mail = Mail(app)


# youve got mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'moonjelly323@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD'] # lol no password for u
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


#let website reload properly 
app.config['ASSETS_DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = 'mOon_jElLy wAs oRiGiNa11y g0nNa b3 SuP3r MaRi0 gAlAxY' # need to change later
# im not mocking Aidan, this key actually needs to be secure which is why it looks all crazy
# I feel personally attacked



mail = Mail(app)


db = SQLAlchemy(app) # wow we have a database
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create our database model. 


#QI use this one
class User(UserMixin, db.Model):

  __tablename__ = "users" ##what does this do?

  # Each user (doctor) will have all these things attributed to him or her
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.Text, unique=True)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)
  is_admin = db.Column(db.Boolean)
  is_cardio = db.Column(db.Boolean)
  initials = db.Column(db.Text)
  password = db.Column(db.Text)
  firstam = db.Column(db.Integer)
  firstpm = db.Column(db.Integer)
  second = db.Column(db.Integer)
  third = db.Column(db.Integer)
  forth = db.Column(db.Integer)
  fifth = db.Column(db.Integer)
  sixth = db.Column(db.Integer)
  seventh = db.Column(db.Integer)
  postcall = db.Column(db.Boolean)
  

  #QI you're probably gonna need to add variables like the one below: 
  #first_AM = db.Column(db.Integer)
  

  # some uh methods for things and stuff 
  def get_reset_token(self, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get(user_id)

  # initialize the object
  def __init__(self, email, first_name, last_name, is_admin, is_cardio, password):
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.is_admin = is_admin
    self.is_cardio = is_cardio
    self.password = password 

    self.firstam = 0
    self.firstpm = 0
    self.second = 0
    self.third = 0
    self.forth = 0
    self.fifth = 0
    self.sixth = 0
    self.seventh = 0
    self.postcall = 0

    self.initials = first_name[0] + last_name[0]

class Number_Users(db.Model):

  __tablename__ = "number_users_db"

  
  id = db.Column(db.Integer, primary_key=True)
  number_usersSu1 = db.Column(db.Integer)
  number_usersM1 = db.Column(db.Integer)
  number_usersT1 = db.Column(db.Integer)
  number_usersW1 = db.Column(db.Integer)
  number_usersTh1 = db.Column(db.Integer)
  number_usersF1 = db.Column(db.Integer)
  number_usersS1 = db.Column(db.Integer)
  
  number_usersSu2 = db.Column(db.Integer)
  number_usersM2 = db.Column(db.Integer)
  number_usersT2 = db.Column(db.Integer)
  number_usersW2 = db.Column(db.Integer)
  number_usersTh2 = db.Column(db.Integer)
  number_usersF2 = db.Column(db.Integer)
  number_usersS2 = db.Column(db.Integer)

  number_usersSu3 = db.Column(db.Integer)
  number_usersM3 = db.Column(db.Integer)
  number_usersT3 = db.Column(db.Integer)
  number_usersW3 = db.Column(db.Integer)
  number_usersTh3 = db.Column(db.Integer)
  number_usersF3 = db.Column(db.Integer)
  number_usersS3 = db.Column(db.Integer)
  #is_current = dbColumn(db.Boolean)

  # initialize the object
  def __init__(self, number_usersSu1, 
                number_usersM1, 
                number_usersT1, 
                number_usersW1, 
                number_usersTh1, 
                number_usersF1, 
                number_usersS1,
                number_usersSu2,
                number_usersM2, 
                number_usersT2, 
                number_usersW2, 
                number_usersTh2, 
                number_usersF2, 
                number_usersS2,
                number_usersSu3,
                number_usersM3, 
                number_usersT3, 
                number_usersW3, 
                number_usersTh3, 
                number_usersF3, 
                number_usersS3):
    self.number_usersSu1 = number_usersSu1
    self.number_usersM1 = number_usersM1
    self.number_usersT1 = number_usersT1
    self.number_usersW1 = number_usersW1
    self.number_usersTh1 = number_usersTh1
    self.number_usersF1 = number_usersF1
    self.number_usersS1 = number_usersS1

    self.number_usersSu2 = number_usersSu2
    self.number_usersM2 = number_usersM2
    self.number_usersT2 = number_usersT2
    self.number_usersW2 = number_usersW2
    self.number_usersTh2 = number_usersTh2
    self.number_usersF2 = number_usersF2
    self.number_usersS2 = number_usersS2

    self.number_usersSu3 = number_usersSu3
    self.number_usersM3 = number_usersM3
    self.number_usersT3 = number_usersT3
    self.number_usersW3 = number_usersW3
    self.number_usersTh3 = number_usersTh3
    self.number_usersF3 = number_usersF3
    self.number_usersS3 = number_usersS3
    #self.is_current = True


class Users_That_Day(db.Model):

  __tablename__ = "Users_That_Day_db"

  
  id = db.Column(db.Integer, primary_key=True)
  Su1 = db.Column(ARRAY(db.Integer))
  M1 = db.Column(ARRAY(db.Integer))
  T1 = db.Column(ARRAY(db.Integer))
  W1 = db.Column(ARRAY(db.Integer))
  Th1 = db.Column(ARRAY(db.Integer))
  F1 = db.Column(ARRAY(db.Integer))
  S1 = db.Column(ARRAY(db.Integer))

  Su2 = db.Column(ARRAY(db.Integer))
  M2 = db.Column(ARRAY(db.Integer))
  T2 = db.Column(ARRAY(db.Integer))
  W2 = db.Column(ARRAY(db.Integer))
  Th2 = db.Column(ARRAY(db.Integer))
  F2 = db.Column(ARRAY(db.Integer))
  S2 = db.Column(ARRAY(db.Integer))

  Su3 = db.Column(ARRAY(db.Integer))
  M3 = db.Column(ARRAY(db.Integer))
  T3 = db.Column(ARRAY(db.Integer))
  W3 = db.Column(ARRAY(db.Integer))
  Th3 = db.Column(ARRAY(db.Integer))
  F3 = db.Column(ARRAY(db.Integer))
  S3 = db.Column(ARRAY(db.Integer))
  #is_current = dbColumn(db.Boolean)

  # initialize the object
  def __init__(self, Su1, M1, T1, W1, Th1, F1, S1, Su2, M2, T2, W2, Th2, F2, S2, Su3, M3, T3, W3, Th3, F3, S3):
    self.Su1 = Su1
    self.M1 = M1
    self.T1 = T1
    self.W1 = W1
    self.Th1 = Th1
    self.F1 = F1
    self.S1 = S1

    self.Su2 = Su2
    self.M2 = M2
    self.T2 = T2
    self.W2 = W2
    self.Th2 = Th2
    self.F2 = F2
    self.S2 = S2

    self.Su3 = Su3
    self.M3 = M3
    self.T3 = T3
    self.W3 = W3
    self.Th3 = Th3
    self.F3 = F3
    self.S3 = S3
    #self.is_current = True


#Qi use this one ##CHANGE FITH
class Day(db.Model):

  __tablename__ = "Days" ##what does this do?

  # Each day of sechedule will have all these things
  id = db.Column(db.Date, primary_key=True)

  first_AM = db.Column(db.Integer)
  first_PM = db.Column(db.Integer)
  second = db.Column(db.Integer)
  third = db.Column(db.Integer)
  fourth = db.Column(db.Integer)
  fith = db.Column(db.Integer)
  sixth = db.Column(db.Integer)
  seventh = db.Column(db.Integer)
  PostCall = db.Column(db.Integer)
  Is_Weekend = db.Column(db.Boolean)


  # initialize the object
  def __init__(self, Is_Weekend, first_AM, first_PM, second, third, fourth, fith, sixth, seventh, PostCall):
    
    self.Is_Weekend = Is_Weekend

    self.first_AM = first_AM
    self.first_PM = first_PM
    self.second = second
    self.third = third
    self.fourth = fourth
    self.fith = fith
    self.sixth = sixth
    self.seventh = seventh
    self.PostCall = PostCall


# database table
class UserTable(Table):
    id = Col('Id')
    email = Col('Email')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    initials = Col('initials')
    is_admin = Col('Administrator?')
    is_cardio = Col('Cardiologist?')
    password = Col('Password',show=False)
    firstam = Col('firstam')
    firstpm= Col('firstpm')
    second = Col('second')
    third = Col('third')

# this is used to save login states for each user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# wtf does this do
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)


@app.route('/<name>/<location>')

def PrintSchedule(name,location):
  s = slots.query.all()

  grid = []
  for i in range(0, len(s), 7):
     grid.append(s[i:i+7])

  rendered=render_template('schedule.html', matrix=grid, name=name, Location=location)  
  css=['img/style.css']
  pdf=pdfkit.from_string(rendered,False,css=css)

  response=make_response(pdf)
  response.headers['Content-Type']='application/pdf'
  response.headers['Content-Disposition']='attachment; filename=output.pdf'
  
  return response

@app.route('/')
def homepage():
  if db.session.query(User).first() == None: # if there are no registered users
    return render_template('home.html') # link the sign up page
  else:
    if not current_user.is_authenticated:
      return render_template('home2.html') # else link the login page (admins add users)
    else:
      return redirect(url_for('logged_in_homepage'))

@app.route('/logged_in_homepage')
@login_required
def logged_in_homepage():
  return render_template('logged_home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == 'POST' and form.validate():
    user = User.query.filter_by(email=form.email.data).first()
    if user: # if we have found the email
      if check_password_hash(user.password, form.password.data): # check if the password is valid
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage')) 
      else:
        form.password.errors.append('Invalid Passowrd!')
    else:
      form.email.errors.append('Invalid Email!')
  return render_template('login.html', form=form)


@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_password():
  form = EmailForm()
  if request.method == 'POST' and form.validate():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_email(user)
      flash('An email should be sent shortly.')
    else:
      flash('Email address not recognized.')
  else:
    print('something isnt riiight')
  return render_template('reset_password.html', form = form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
  # define a form object
  register_form = RegisterForm()

  if request.method == 'POST': # for some reason request.method is 'GET' now??
    first_name = request.form['first_name'] 
    last_name = request.form['last_name']
    email = request.form['email']
    is_cardio = request.form['is_cardio']
    password = request.form['password']
    
    # if the inputs we're all validated by WTforms (improve validation later)
    if register_form.validate(): 
      # first hash the password
      hashed_password = generate_password_hash(password, method = 'sha256') 
      # then store info in an initialized User object and store the object in the database
      if is_cardio == 'True':
        is_cardio = True
      else:
        is_cardio = False
      new_user = User(email, first_name, last_name, True, is_cardio, hashed_password)
      db.session.add(new_user) # add to database
      db.session.commit() # for some reason we also need to commit it otherwise it won't add
      return redirect(url_for('homepage')) # go to homepage again 
    else:
      print("Invalid input(s)!")
       # first hash the password
      hashed_password = generate_password_hash(password, method = 'sha256') 
      # then store info in an initialized User object and store the object in the database
      if is_cardio == 'True':
        is_cardio = True
      else:
        is_cardio = False
      new_user = User(email, first_name, last_name, True, is_cardio, hashed_password)
      db.session.add(new_user) # add to database
      db.session.commit() # for some reason we also need to commit it otherwise it won't add
      return redirect(url_for('homepage')) # go to homepage again 
  else:
    print(request.method)
      
  # add html file here
  return render_template('register.html', form = register_form)



def send_password_email(user):
  token = user.get_reset_token()
  msg = Message('Set ur goddamn Password here',
                sender='moonjelly323@gmail.com',
                recipients=[user.email])
  msg.body = f'''To set your password, visit the following link:
{url_for('set_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
  mail.send(msg)


@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
  user_form = UserForm()
  if current_user.is_admin == None:
    return redirect(url_for('homepage'))
  else:
    if request.method == 'POST': # for some reason request.method is 'GET' now??
      first_name = request.form['first_name'] 
      last_name = request.form['last_name']
      email = request.form['email']
      is_cardio = request.form['is_cardio']
      is_admin = request.form['is_admin']
      
      # if the inputs we're all validated by WTforms (improve validation later)
      if user_form.validate(): 
        if is_cardio == 'True':
          is_cardio = True
        else:
          is_cardio = False
        if is_admin == 'True':
          is_admin = True
        else:
          is_admin = False
        new_user = User(email, first_name, last_name, is_admin, is_cardio, 'lolwat')
        db.session.add(new_user) # add to database
        db.session.commit() # for some reason we also need to commit it otherwise it won't add
        send_password_email(new_user)
        return redirect(url_for('users')) # go to homepage again 
      else:
        print("alright this dont work")
        if is_cardio == 'True':
          is_cardio = True
        else:
          is_cardio = False
        if is_admin == 'True':
          is_admin = True
        else:
          is_admin = False
        new_user = User(email, first_name, last_name, is_admin, is_cardio, 'lolwat')
        db.session.add(new_user) # add to database
        db.session.commit() # for some reason we also need to commit it otherwise it won't add
        send_password_email(new_user)
        return redirect(url_for('users')) # go to homepage again 
    else:
      print(request.method)
  return render_template('add.html', form = user_form)


@app.route("/set_password/<token>", methods=['GET', 'POST'])
def set_token(token):
  if current_user.is_authenticated:
    flash("You must first log out!")
    return redirect(url_for('logged_in_homepage'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('homepage'))
  form = SetPasswordForm()
  if form.validate():
    password = request.form['password']
    hashed_password = generate_password_hash(password, method = 'sha256') 
    user.password = hashed_password
    db.session.commit()
    flash('Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('login'))
  return render_template('set_password.html', form=form)


@app.route('/remove', methods = ['GET', 'POST'])
@login_required
def remove():
  
  delete_form = DeleteForm()

  if request.method == 'POST':
    Name2Rm = request.form['first_name']
   
    if delete_form.validate(): 
      if User.query.filter_by(first_name = Name2Rm).first() != None:
        toRM = User.query.filter_by(first_name = Name2Rm).first()
        db.session.delete(toRM)
        db.session.commit()
        return redirect('/users')
      else:
        print("User First Name Not Found")
    else:
      print("Invalid input(s)!")

  return render_template('remove.html', delete_form = delete_form)

@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)

@app.route('/about')
def about():
  try:
    message = subprocess.check_output(['about'], shell=True)
  except:
    message = "Sorry, we coundn't run that command..."
  #dir:command you want to run(name)
  if not current_user.is_authenticated: # if not logged in
    return render_template('about.html', message=message)
  else:
    return render_template('logged_about.html')


@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html')

@app.route('/Jenny')
def Jenny():
  return render_template('Jenny.html')

@app.route('/contact')
def contact():
  try:
    message = subprocess.check_output(['hi'], shell=True)
  except:
    message = "Sorry, we coundn't run that command..."
  #dir:command you want to run(name)
  return render_template('contact.html', message=message)

#test to print out the first names of users 
@app.route('/users')
@login_required
def users():
  u = User.query.all()
  utable = UserTable(u)
  return render_template('users.html', utable=utable)

@app.route('/slots')
def slots():
  u = slots.query.all()
  utable = SlotTable(u)
  return render_template('users.html', utable=utable)

  #create a schedule page
@app.route('/make', methods=['GET', 'POST'])
def make():

  numuForm = NumberUsersForm()


  if request.method == 'POST':

    if(request.form['NumberUsersSu1'].isdigit()):
      number_usersSu1 = int(request.form['NumberUsersSu1'])

    if(request.form['NumberUsersM1'].isdigit()):
      number_usersM1 = int(request.form['NumberUsersM1'])

    if(request.form['NumberUsersT1'].isdigit()):
      number_usersT1 = int(request.form['NumberUsersT1'])
    
    if(request.form['NumberUsersW1'].isdigit()):
     number_usersW1 = int(request.form['NumberUsersW1'])
    
    if(request.form['NumberUsersTh1'].isdigit()):
     number_usersTh1 = int(request.form['NumberUsersTh1'])
    
    if(request.form['NumberUsersF1'].isdigit()):
      number_usersF1 = int(request.form['NumberUsersF1'])
    
    if(request.form['NumberUsersS1'].isdigit()):
     number_usersS1 = int(request.form['NumberUsersS1'])


    if(request.form['NumberUsersSu2'].isdigit()):
      number_usersSu2 = int(request.form['NumberUsersSu2'])

    if(request.form['NumberUsersM2'].isdigit()):
      number_usersM2 = int(request.form['NumberUsersM2'])

    if(request.form['NumberUsersT2'].isdigit()):
      number_usersT2 = int(request.form['NumberUsersT2'])
    
    if(request.form['NumberUsersW2'].isdigit()):
     number_usersW2 = int(request.form['NumberUsersW2'])
    
    if(request.form['NumberUsersTh2'].isdigit()):
     number_usersTh2 = int(request.form['NumberUsersTh2'])
    
    if(request.form['NumberUsersF2'].isdigit()):
      number_usersF2 = int(request.form['NumberUsersF2'])
    
    if(request.form['NumberUsersS2'].isdigit()):
     number_usersS2 = int(request.form['NumberUsersS2'])


    if(request.form['NumberUsersSu3'].isdigit()):
      number_usersSu3 = int(request.form['NumberUsersSu3'])

    if(request.form['NumberUsersM3'].isdigit()):
      number_usersM3 = int(request.form['NumberUsersM3'])

    if(request.form['NumberUsersT3'].isdigit()):
      number_usersT3 = int(request.form['NumberUsersT3'])
    
    if(request.form['NumberUsersW3'].isdigit()):
     number_usersW3 = int(request.form['NumberUsersW3'])
    
    if(request.form['NumberUsersTh3'].isdigit()):
     number_usersTh3 = int(request.form['NumberUsersTh3'])
    
    if(request.form['NumberUsersF3'].isdigit()):
      number_usersF3 = int(request.form['NumberUsersF3'])
    
    if(request.form['NumberUsersS3'].isdigit()):
     number_usersS3 = int(request.form['NumberUsersS3'])


       
    if numuForm.validate(): 
      new_number_users = Number_Users(number_usersSu1, 
                                      number_usersM1, 
                                      number_usersT1, 
                                      number_usersW1, 
                                      number_usersTh1, 
                                      number_usersF1, 
                                      number_usersS1,
                                      number_usersSu2, 
                                      number_usersM2, 
                                      number_usersT2, 
                                      number_usersW2, 
                                      number_usersTh2, 
                                      number_usersF2, 
                                      number_usersS2,
                                      number_usersSu3, 
                                      number_usersM3, 
                                      number_usersT3, 
                                      number_usersW3, 
                                      number_usersTh3, 
                                      number_usersF3, 
                                      number_usersS3)
      db.session.add(new_number_users)
      db.session.commit()
      return redirect('/make2')
  return render_template('make.html', numuForm = numuForm)

@app.route('/make2', methods=['GET', 'POST'])
def make2():

  allslots = slots.query.all()
  if allslots != []:
    db.session.query(slots).delete()
    db.session.commit()
    #.slots.query().delete()

  Su1 = []
  M1 = []
  T1 = []
  W1 = []
  Th1 = []
  F1 = []
  S1 = []

  Su2 = []
  M2 = []
  T2 = []
  W2 = []
  Th2 = []
  F2 = []
  S2 = []

  Su3 = []
  M3 = []
  T3 = []
  W3 = []
  Th3 = []
  F3 = []
  S3 = []


  Su1_id = []
  M1_id = []
  T1_id = []
  W1_id = []
  Th1_id = []
  F1_id = []
  S1_id = []

  Su2_id = []
  M2_id = []
  T2_id = []
  W2_id = []
  Th2_id = []
  F2_id = []
  S2_id = []

  Su3_id = []
  M3_id = []
  T3_id = []
  W3_id = []
  Th3_id = []
  F3_id = []
  S3_id = []

  NU = Number_Users.query.all()

  userfirstNamesSu1 = ["first_name"]*NU[-1].number_usersSu1
  userfirstNamesM1 = ["first_name"]*NU[-1].number_usersM1
  userfirstNamesT1 = ["first_name"]*NU[-1].number_usersT1
  userfirstNamesW1 = ["first_name"]*NU[-1].number_usersW1
  userfirstNamesTh1 = ["first_name"]*NU[-1].number_usersTh1
  userfirstNamesF1 = ["first_name"]*NU[-1].number_usersF1
  userfirstNamesS1 = ["first_name"]*NU[-1].number_usersS1

  userfirstNamesSu2 = ["first_name"]*NU[-1].number_usersSu2
  userfirstNamesM2 = ["first_name"]*NU[-1].number_usersM2
  userfirstNamesT2 = ["first_name"]*NU[-1].number_usersT2
  userfirstNamesW2 = ["first_name"]*NU[-1].number_usersW2
  userfirstNamesTh2 = ["first_name"]*NU[-1].number_usersTh2
  userfirstNamesF2 = ["first_name"]*NU[-1].number_usersF2
  userfirstNamesS2 = ["first_name"]*NU[-1].number_usersS2

  userfirstNamesSu3 = ["first_name"]*NU[-1].number_usersSu3
  userfirstNamesM3 = ["first_name"]*NU[-1].number_usersM3
  userfirstNamesT3 = ["first_name"]*NU[-1].number_usersT3
  userfirstNamesW3 = ["first_name"]*NU[-1].number_usersW3
  userfirstNamesTh3 = ["first_name"]*NU[-1].number_usersTh3
  userfirstNamesF3 = ["first_name"]*NU[-1].number_usersF3
  userfirstNamesS3 = ["first_name"]*NU[-1].number_usersS3

  SchedForm = ScheduleForm(request.form,
                           userfirstNamesSu1=userfirstNamesSu1,
                           userfirstNamesM1=userfirstNamesM1,
                           userfirstNamesT1=userfirstNamesT1,
                           userfirstNamesW1=userfirstNamesW1,
                           userfirstNamesTh1=userfirstNamesTh1,
                           userfirstNamesF1=userfirstNamesF1,
                           userfirstNamesS1=userfirstNamesS1,
                           userfirstNamesSu2=userfirstNamesSu2,
                           userfirstNamesM2=userfirstNamesM2,
                           userfirstNamesT2=userfirstNamesT2,
                           userfirstNamesW2=userfirstNamesW2,
                           userfirstNamesTh2=userfirstNamesTh2,
                           userfirstNamesF2=userfirstNamesF2,
                           userfirstNamesS2=userfirstNamesS2,
                           userfirstNamesSu3=userfirstNamesSu3,
                           userfirstNamesM3=userfirstNamesM3,
                           userfirstNamesT3=userfirstNamesT3,
                           userfirstNamesW3=userfirstNamesW3,
                           userfirstNamesTh3=userfirstNamesTh3,
                           userfirstNamesF3=userfirstNamesF3,
                           userfirstNamesS3=userfirstNamesS3)
  


  if request.method == 'POST':
    
    for entry in SchedForm.userfirstNamesSu1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Su1_id.append(U1.id)

        Su1.append(U1) #bug here, said M1.append(U1)

      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesM1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        M1_id.append(U1.id)
        M1.append(U1)
      else:
        print("not a valid first name")
    
    for entry in SchedForm.userfirstNamesT1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        T1_id.append(U1.id)
        T1.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesW1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        W1_id.append(U1.id)
        W1.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesTh1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Th1_id.append(U1.id)
        Th1.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesF1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        F1_id.append(U1.id)
        F1.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesS1.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        S1_id.append(U1.id)
        S1.append(U1)
      else:
        print("not a valid first name")



    for entry in SchedForm.userfirstNamesSu2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Su2_id.append(U1.id)
        Su2.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesM2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        M2_id.append(U1.id)
        M2.append(U1)
      else:
        print("not a valid first name")
    
    for entry in SchedForm.userfirstNamesT2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        T2_id.append(U1.id)
        T2.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesW2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        W2_id.append(U1.id)
        W2.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesTh2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Th2_id.append(U1.id)
        Th2.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesF2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        F2_id.append(U1.id)
        F2.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesS2.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        S2_id.append(U1.id)
        S2.append(U1)
      else:
        print("not a valid first name")




    for entry in SchedForm.userfirstNamesSu3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Su3_id.append(U1.id)
        Su3.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesM3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        M3_id.append(U1.id)
        M3.append(U1)
      else:
        print("not a valid first name")
    
    for entry in SchedForm.userfirstNamesT3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        T3_id.append(U1.id)
        T3.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesW3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        W3_id.append(U1.id)
        W3.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesTh3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Th3_id.append(U1.id)
        Th3.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesF3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        F3_id.append(U1.id)
        F3.append(U1)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesS3.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        S3_id.append(U1.id)
        S3.append(U1)
      else:
        print("not a valid first name")


    if SchedForm.validate(): 
      new_users_that_day = Users_That_Day(Su1_id, M1_id, T1_id, W1_id, Th1_id, F1_id, S1_id, Su2_id, M2_id, T2_id, W2_id, Th2_id, F2_id, S2_id, Su3_id, M3_id, T3_id, W3_id, Th3_id, F3_id, S3_id)
      db.session.add(new_users_that_day) # add to database


      #sorter2(Su1, M1, T1, W1, Th1, F1, S1, Su2, M2, T2, W2, Th2, F2, S2) 
      #print("min_val(Su1, second) = ", min_val(Su1, 'second'))
      #M, nw1, nw2 = sorter(parameter)

      matrix, nw1, nw2 = sorter(Su1, M1, T1, W1, Th1, F1, S1, None, None)    
      for row in matrix:
        for slot in row:
          db.session.add(slot)

      matrix2, nw3, nw4 = sorter(Su2, M2, T2, W2, Th2, F2, S2, nw1, nw2)    
      for row in matrix2:
        for slot in row:
          db.session.add(slot)
      

      matrix3 = sorter(Su3, M3, T3, W3, Th3, F3, S3, nw3, nw4)[0]
      for row in matrix3:
        for slot in row:
          db.session.add(slot)
      

      db.session.commit()
      return(redirect('/schedule'))

  
  print("SchedForm.errors = ", SchedForm.errors)
  #print("Su1 = ",Su1)
  
  # s = slots.query.all()
  # grid = []
  # for i in range(0, len(s), 7):
  #  grid.append(s[i:i+7])

  return render_template('make2.html',schedForm = SchedForm)


class slots(db.Model):


  __tablename__ = "slots_db"

  id = db.Column(db.Integer, primary_key=True)
  
  daynumber = db.Column(db.Integer)
  shiftnumber = db.Column(db.Integer)
  doctorID = db.Column(db.Integer, ForeignKey('users.id'))
  doctor = relationship("User")

  # initialize the object
  def __init__(self, daynumber, shiftnumber, doctorID):
    self.daynumber = daynumber
    self.shiftnumber = shiftnumber
    self.doctorID = doctorID

class SlotTable(Table):
   id = Col('db id')
   daynumber = Col('day #')
   shiftnumber = Col('shift #')
   doctorID = Col('Doctor id')

def sorter(Su1, M1, T1, W1, Th1, F1, S1, notweekend1, notweekend2):
  #construct a schedule table with slots
  spotlist = ["third", "forth", "fifth", "sixth", "seventh", "postcall"]


  #allusers = User.query.all()

  matrix = [[None for y in range(0,7)] for x in range(0,9)]
  for i in range(0,9):
   for j in range(0,7):
    matrix[i][j] = slots(j + 1, i + 1, doctorID = None)

  #monday 1
  firstam = min_firstam(M1)
  firstpm = min_firstpm(M1, firstam)
  second = min_second(M1, firstam, firstpm)
  matrix[0][0].doctorID = firstam.id
  matrix[1][0].doctorID = firstpm.id
  matrix[2][0].doctorID = second.id

  k = 3 
  excludelist = [firstam.id, firstpm.id, second.id]
  for i in range(0 , len(M1)-3 ):
    #print("i = ", i, "      :     nextslot = min_val(M1,", spotlist[i],",excludelist) = ", min_val(M1, spotlist[i],excludelist))
    nextslot = min_val(M1, spotlist[i], excludelist)
    matrix[k][0].doctorID = nextslot.id
    excludelist.append(nextslot.id)
    k += 1

  #tuesday 1
  firstam = min_firstam(T1)
  firstpm = min_firstpm(T1, firstam)
  second = min_second(T1, firstam, firstpm)
  matrix[0][1].doctorID = firstam.id
  matrix[1][1].doctorID = firstpm.id
  matrix[2][1].doctorID = second.id
  
  k = 3 
  excludelist = [firstam.id, firstpm.id, second.id]
  for i in range(0 , len(T1)-3 ):
    nextslot = min_val(T1, spotlist[i], excludelist)
    matrix[k][0].doctorID = nextslot.id
    excludelist.append(nextslot.id)
    k += 1
  matrix[8][1].doctorID = matrix[1][0].doctorID

  #wednesday 1 
  firstam = min_firstam(W1)
  firstpm = min_firstpm(W1, firstam)
  second = min_second(W1, firstam, firstpm)
  matrix[0][2].doctorID = firstam.id
  matrix[1][2].doctorID = firstpm.id
  matrix[2][2].doctorID = second.id
  
  k = 3 
  excludelist = [firstam.id, firstpm.id, second.id]
  for i in range(0 , len(W1)-3 ):
    nextslot = min_val(W1, spotlist[i], excludelist)
    matrix[k][0].doctorID = nextslot.id
    excludelist.append(nextslot.id)
    k += 1
  matrix[8][2].doctorID = matrix[1][1].doctorID


  #Thursday 1
  firstam = min_firstam(Th1)
  firstpm = min_firstpm(Th1, firstam)
  second = min_second(W1, firstam, firstpm)
  matrix[0][3].doctorID = firstam.id
  matrix[1][3].doctorID = firstpm.id
  matrix[2][3].doctorID = second.id
  
  k = 3 
  excludelist = [firstam.id, firstpm.id, second.id]
  for i in range(0 , len(Th1)-3 ):
    nextslot = min_val(Th1, spotlist[i], excludelist)
    matrix[k][0].doctorID = nextslot.id
    excludelist.append(nextslot.id)
    k += 1
  matrix[8][3].doctorID = matrix[1][2].doctorID




  #friday 1
  firstam = min_firstam(F1)
  firstpm = min_firstpm(F1, firstam)
  second = min_second(F1, firstam, firstpm)
  matrix[0][4].doctorID = firstam.id
  matrix[1][4].doctorID = firstpm.id
  matrix[2][4].doctorID = second.id
  
  k = 3 
  excludelist = [firstam.id, firstpm.id, second.id]
  for i in range(0 , len(F1)-3 ):
    nextslot = min_val(F1, spotlist[i], excludelist)
    matrix[k][0].doctorID = nextslot.id
    excludelist.append(nextslot.id)
    k += 1
  matrix[8][4].doctorID = matrix[1][3].doctorID


  #saturday 1
  matrix[0][5].doctorID = second.id #second on friday = first am/pm on saturday
  matrix[1][5].doctorID = second.id
  matrix[2][5].doctorID = firstam.id #first am friday = second on saturday
  excludelist = [second.id, firstam.id]
  matrix[3][5].doctorID = min_val(S1, "third", excludelist).id  ###FIX THIS

  #sunday 1
  matrix[0][6].doctorID = firstam.id #firstam on friday = first am/pm on sunday
  matrix[1][6].doctorID = firstam.id
  matrix[2][6].doctorID = second.id #second on friday = second on sunday
  excludelist = [firstam.id, second.id]
  matrix[3][6].doctorID = min_val(Su1, "third", excludelist).id  ###FIX THIS
 
  notweekend1 = matrix[0][5].doctorID = second.id
  notweekend2 = matrix[2][5].doctorID = firstam.id

  return (matrix, notweekend1, notweekend2) 
  
  #sort so every user gets around the same number of spots
  #if there are less users than spots, dont fill the higher numbered spots
  #whoever works 'first_PM' will work 'PostCall' the next day always


def min_firstam(userlist): #gives user with the minimum firstam value from a list of users
  min_firstam = None
  for i in range(0,len(userlist)):
    if i == 0:
      min_firstam = userlist[i]
    else:
      if userlist[i].firstam < min_firstam.firstam:
        min_firstam = userlist[i] 

  #ival = min_firstam.firstam + 1
  #user.update().values(firstam = ival).where(user.id == min_firstam.id)
  min_firstam.firstam += 1
  db.session.commit()

  return(min_firstam)

def min_firstpm(userlist, first_am): #gives user with the minimum firstpm value from a list of users given firstam
  min_firstpm = None

  for i in range(0,len(userlist)):
      if first_am.id != userlist[i].id:  #isnt first_am
        if first_am.is_cardio is True: #dont need 2 cardios
          if userlist[i].is_cardio is False: 
           if min_firstpm == None:
             min_firstpm = userlist[i]
           else:
             if userlist[i].firstpm < min_firstpm.firstpm:
                min_firstpm = userlist[i]
                ###### WHAT IF THERE ARE NO CARDIOS?
          if min_firstpm == None:
            min_firstpm = userlist[i]
          ####elif min_firstpm == None:

        else:                             #if not cardio, we need one
          if userlist[i].is_cardio is True:
            if min_firstpm == None:
              min_firstpm = userlist[i]
            else:
              if userlist[i].firstpm < min_firstpm.firstpm:
                min_firstpm = userlist[i]
          if min_firstpm == None:
            min_firstpm = userlist[i]

  #ival = min_firstpm.firstpm + 1
  #user.update().values(firstpm = ival).where(user.id == min_firstpm.id)
  min_firstpm.firstpm += 1
  db.session.commit()

  return(min_firstpm)

def min_second(userlist, first_am, first_pm): #gives user with the minimum second value from a list of users given firstam and firstpm
  min_second = None

  for i in range(0,len(userlist)):
    if first_am.id != userlist[i].id and first_pm.id != userlist[i].id :  #isnt first_am or first_pm
      if min_second == None:
        min_second = userlist[i]
      else:
        if userlist[i].second < min_second.second:
          min_second = userlist[i]

  #ival = min_second.second + 1
  #user.update().values(second = ival).where(user.id == min_second.id)
  min_second.second += 1
  db.session.commit()
  return(min_second)

def min_val(inputlist, parameter, excludelist): #gives user with the minimum value of a parameter from a list of users
  min_val = None

  #print("parameter = " , parameter)

  userlist = [] 
  for i in range(0,len(inputlist)):
    add = False
    for j in range(0,len(excludelist)):
      # print( "i = ",i,"   j = " ,j)
      if inputlist[i].id == excludelist[j]:
        #print("broke at ", "j = ",j, "i = ",i)
        print("inputlist[",i,"] = ", inputlist[i], "   excludelist[",j,"] = ",excludelist[j])
        break
      else:
        if j == len(excludelist)-1:
          #print ("add = True")
          add = True
    if add == True:
      userlist.append(inputlist[i])

  #print("inputlist = ", inputlist)
  #print("excludelist = ", excludelist)
  #print("userlist = ", userlist)



  for i in range(0,len(userlist)):
    if i == 0:
      min_val = userlist[i]
    else:
      if parameter == "firstam": 
        if userlist[i].firstam < min_val.firstam:
          min_val = userlist[i] 
      if parameter == "firstpm": 
        if userlist[i].firstpm < min_val.firstpm:
          min_val = userlist[i] 
      if parameter == "second": 
        if userlist[i].second < min_val.second:
          min_val = userlist[i] 
      if parameter == "third": 
        if userlist[i].third < min_val.third:
          min_val = userlist[i] 
      if parameter == "fourth": 
        if userlist[i].fourth < min_val.fourth:
          min_val = userlist[i] 
      if parameter == "fifth": 
        if userlist[i].fifth < min_val.fifth:
          min_val = userlist[i] 
      if parameter == "sixth": 
        if userlist[i].sixth < min_val.sixth:
          min_val = userlist[i] 
      if parameter == "seventh": 
        if userlist[i].seventh < min_val.seventh:
          min_val = userlist[i] 
      if parameter == "postcall": 
        if userlist[i].postcall < min_val.postcall:
          min_val = userlist[i]

  if parameter == "firstam":
    min_val.firstam += 1
    #ival = min_val.firstam + 1
    #user.update().values(firstam = ival).where(user.id == min_val.id)
  
  if parameter == "firstpm":
    min_val.firstpm += 1
    #ival = min_val.firstpm + 1
    #user.update().values(firstpm = ival).where(user.id == min_val.id)
  
  if parameter == "second":
    min_val.second += 1
    #ival = min_val.second + 1
    #user.update().values(second = 1).where(user.id == min_val.id)
  
  if parameter == "third":
    #print("min_val.third before iterating =   ", min_val.third)
    min_val.third += 1
    #print("min_val.third after iterating =   ", min_val.third)
    #ival = min_val.third + 1
    #user.update().values(third = ival).where(user.id == min_val.id)

  if parameter == "fourth":
    min_val.fourth += 1
    #ival = min_val.fourth + 1
    #user.update().values(fourth = ival).where(user.id == min_val.id)

  if parameter == "fifth":
    min_val.fifth += 1
    #ival = min_val.fifth + 1
    #user.update().values(fifth = ival).where(user.id == min_val.id)

  if parameter == "sixth":
    min_val.sixth += 1
    #ival = min_val.sixth + 1
    #user.update().values(sixth = ival).where(user.id == min_val.id)

  if parameter == "seventh":
    min_val.seventh += 1
    #ival = min_val.seventh + 1
    #user.update().values(seventh = ival).where(user.id == min_val.id)

  if parameter == "postcall":
    min_val.postcall += 1
    #ival = min_val.postcall + 1
    #user.update().values(postcall = ival).where(user.id == min_val.id)

  db.session.commit()

  return(min_val)


def min_val_check(inputlist, parameter, excludelist): #gives user with the minimum value of a parameter from a list of users, doesnt iterate
  min_val = None

  userlist = [] 
  for i in range(0,len(inputlist)):
    add = False
    for j in range(0,len(excludelist)):
      if inputlist[i] == excludelist[j]:
        break
      elif j == len(excludelist):
        add = True
    if add == True:
      userlist.append(inputlist[i])
          


  for i in range(0,len(userlist)):
    if i == 0:
      min_val = userlist[i]
    else:
      if parameter == "firstam": 
        if userlist[i].firstam < min_val.firstam:
          min_val = userlist[i] 
      if parameter == "firstpm": 
        if userlist[i].firstpm < min_val.firstpm:
          min_val = userlist[i] 
      if parameter == "second": 
        if userlist[i].second < min_val.second:
          min_val = userlist[i] 
      if parameter == "third": 
        if userlist[i].third < min_val.third:
          min_val = userlist[i] 
      if parameter == "fourth": 
        if userlist[i].fourth < min_val.fourth:
          min_val = userlist[i] 
      if parameter == "fifth": 
        if userlist[i].fifth < min_val.fifth:
          min_val = userlist[i] 
      if parameter == "sixth": 
        if userlist[i].sixth < min_val.sixth:
          min_val = userlist[i] 
      if parameter == "seventh": 
        if userlist[i].seventh < min_val.seventh:
          min_val = userlist[i] 
      if parameter == "postcall": 
        if userlist[i].postcall < min_val.postcall:
          min_val = userlist[i]





  return min_val

@app.route('/schedule')
def schedule():
 # NU = Number_Users.query.all()
 # s = []
 # grid = []
  
  #for j in range(1*NU[-1].id, 8*NU[-1].id):
   # s.append(slots.query.filter_by(daynumber=j))

  #for i in range(0,len(s)):
  #  grid.append(s[i:i+7])

  #slots.filter_by()

  s = slots.query.all()

  grid = []
  grid2 = []
  grid3 = []
  for i in range(0, 63, 7):
    grid.append(s[i:i+7])
  for i in range(63, 126, 7):
    grid2.append(s[i:i+7])
  for i in range(126, 189, 7):
    grid3.append(s[i:i+7])
  

  return render_template('schedule.html', matrix = grid, matrix2 = grid2, matrix3 = grid3)

@app.route("/csvout")
@login_required
def csvout():
  #conn = psycopg2.connect("host=localhost dbname=postgres user=postgres") ##??
  #cur = conn.cursor()
  #cur.copy_expert('COPY "Users_That_Day_db" TO STDOUT WITH CSV HEADER', scheduleoutput)
  #schedule = csv.writer(csvfile, delimiter=' ',
  #                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
  #cur.copy_to(schedule, '"Users_That_Day_db"')

  #All_User_Ids = Users_That_Day.query.all()


  #map(lambda x: [x], csvData)


  s = slots.query.all()
  #u = users.quesry.all()
  grid = []
  grid2 = []
  grid3 = []
  for i in range(0, 63, 7):
    grid.append(s[i:i+7])
  for i in range(63, 126, 7):
    grid2.append(s[i:i+7])
  for i in range(126, 189, 7):
    grid3.append(s[i:i+7])
  

  with open(os.path.join(os.path.expanduser('~'),'Desktop','MoonJellySchedule.csv'), 'w') as csvFile:
    fieldnames = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

    writer.writeheader()
    for i in grid:
      print("i[0].doctor = ", i[0].doctor)
      writer.writerow({'Monday': hasfirstname(i[0].doctor),'Tuesday': hasfirstname(i[1].doctor),'Wednesday': hasfirstname(i[2].doctor),'Thursday': hasfirstname(i[3].doctor),'Friday': hasfirstname(i[4].doctor),'Saturday': hasfirstname(i[5].doctor),'Sunday': hasfirstname(i[6].doctor)})
    writer.writeheader()
    for i in grid2:
      writer.writerow({'Monday': hasfirstname(i[0].doctor),'Tuesday': hasfirstname(i[1].doctor),'Wednesday': hasfirstname(i[2].doctor),'Thursday': hasfirstname(i[3].doctor),'Friday': hasfirstname(i[4].doctor),'Saturday': hasfirstname(i[5].doctor),'Sunday': hasfirstname(i[6].doctor)})
    writer.writeheader()
    for i in grid3:
      writer.writerow({'Monday': hasfirstname(i[0].doctor),'Tuesday': hasfirstname(i[1].doctor),'Wednesday': hasfirstname(i[2].doctor),'Thursday': hasfirstname(i[3].doctor),'Friday': hasfirstname(i[4].doctor),'Saturday': hasfirstname(i[5].doctor),'Sunday': hasfirstname(i[6].doctor)})


  #this works
  # with open('Slots.csv', 'w') as csvFile:
  #   writer = csv.writer(csvFile)
  #   writer.writerows(map(lambda x: [x], grid))

  csvFile.close()

  return redirect(url_for('schedule'))
  
def hasfirstname(User):
  if User == None:
    return(None)
  else:
    return(User.first_name)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

#pdfkit.from_url('https://moon-jelly.herokuapp.com/schedule', 'schedule.pdf')  


if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
