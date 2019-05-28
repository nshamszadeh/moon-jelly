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
  # firstam = db.Column(db.Integer)
  # firstpm = db.Column(db.Integer)
  # second = db.Column(db.Integer)
  # third = db.Column(db.Integer)
  # forth = db.Column(db.Integer)
  # fifth = db.Column(db.Integer)
  # sixth = db.Column(db.Integer)
  # seventh = db.Column(db.Integer)
  # postcall = db.Column(db.Boolean)
  

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

    # self.firstam = firstam
    # self.firstpm = firstpm
    # self.second = second
    # self.third = third
    # self.forth = forth
    # self.fifth = fifth
    # self.sixth = sixth
    # self.seventh = seventh
    # self.postcall = postcall

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


#Qi use this one
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

# this is used to save login states for each user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# wtf does this do
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)


@app.route('/<name>/<location>')
def Schedule(name,location):
  rendered=render_template('schedule.html', name=name, Location=location)

  
  css=['img/style.css']
  pdf=pdfkit.from_string(rendered,False,css=css)

  response=make_response(pdf)
  response.headers['Content-Type']='application/pdf'
  response.headers['Content-Disposition']='attachment; filename=output.pdf'
  
  return response
  
  #return render_template('Certificate.html')

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
        return redirect(url_for('homepage')) # go to homepage again 
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
        return redirect(url_for('homepage')) # go to homepage again 
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
    message = subprocess.check_output(['hi'], shell=True)
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

      matrix = sorter(Su1, M1, T1, W1, Th1, F1, S1)    
      for row in matrix:
       for slot in row:
        db.session.add(slot)

      db.session.commit()
      return(redirect('/schedule'))

  
  print("SchedForm.errors = ", SchedForm.errors)
  #print("Su1 = ",Su1)
  
  s = slots.query.all()
  grid = []
  for i in range(0, len(s), 7):
   grid.append(s[i:i+7])
  return render_template('make2.html', matrix = grid, schedForm = SchedForm)


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
   shiftnumber = Col('shirft #')
   doctorID = Col('Doctor id')

def sorter(Su1, M1, T1, W1, Th1, F1, S1):
  #construct a schedule table with slots
  matrix = [[None for y in range(0,7)] for x in range(0,9)]
  for i in range(0,9):
   for j in range(0,7):
    matrix[i][j] = slots(j + 1, i + 1, doctorID = None)

  k = 1
  filled = False
  for i in range(0,len(M1)):
   if M1[i].is_cardio is True and filled is False:
    matrix[0][0].doctorID = M1[i].id
    filled = True
   else:
    matrix[k][0].doctorID = M1[i].id
    k += 1
  
  k = 1
  filled = False
  for i in range(0,len(T1)):
   if T1[i].is_cardio is True and filled is False:
    matrix[0][1].doctorID = T1[i].id
    filled = True
   else:
    matrix[k][1].doctorID = T1[i].id
    k += 1
   matrix[8][1].doctorID = matrix[0][0].doctorID

  k = 1
  filled = False
  for i in range(0,len(W1)):
   if W1[i].is_cardio is True and filled is False:
    matrix[0][2].doctorID = W1[i].id
    filled = True
   else:
    matrix[k][2].doctorID = W1[i].id
    k += 1
   matrix[8][2].doctorID = matrix[0][1].doctorID

  k = 1
  filled = False
  for i in range(0,len(Th1)):
   if Th1[i].is_cardio is True and filled is False:
    matrix[0][3].doctorID = Th1[i].id
    filled = True
   else:
    matrix[k][3].doctorID = Th1[i].id
    k += 1
   matrix[8][3].doctorID = matrix[0][2].doctorID

  k = 1
  filled = False
  for i in range(0,len(F1)):
   if F1[i].is_cardio is True and filled is False:
    matrix[0][4].doctorID = F1[i].id
    filled = True
   else:
    matrix[k][4].doctorID = F1[i].id
    k += 1
   matrix[8][4].doctorID = matrix[0][3].doctorID

  k = 1
  filled = False
  for i in range(0,len(S1)):
   if S1[i].is_cardio is True and filled is False:
    matrix[0][5].doctorID = S1[i].id
    filled = True
   else:
    matrix[k][5].doctorID = S1[i].id
    k += 1
   matrix[8][5].doctorID = matrix[0][4].doctorID

  k = 1
  filled = False
  for i in range(0,len(Su1)):
   if Su1[i].is_cardio is True and filled is False:
    matrix[0][6].doctorID = Su1[i].id
    filled = True
   else:
    matrix[k][6].doctorID = Su1[i].id
    k += 1
   matrix[8][6].doctorID = matrix[0][5].doctorID

  return matrix
  #sort so every user gets around the same number of spots
  #if there are less users than spots, dont fill the higher numbered spots
  #whoever works 'first_PM' will work 'PostCall' the next day always



@app.route('/schedule')
def schedule():
  # s = slots.query.all()
  # grid = []
  # for i in range(0, len(s), 7):
  #  grid.append(s[i:i+7])
  # return render_template('schedule.html', matrix = grid)
  return render_template('schedule.html')
  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

#pdfkit.from_url('https://moon-jelly.herokuapp.com/schedule', 'schedule.pdf')  


if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
