import os
import subprocess
from flask import make_response, Flask, render_template, request, redirect, send_from_directory, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, UserForm, DeleteForm, RegisterForm, ScheduleForm, ScheduleEntryForm, NumberUsersForm
from flask_table import Table, Col
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# URL should be whatever database URL is being used (if testing on your own use a database different from the team's )
                           
#let website reload properly 
app.config['ASSETS_DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ricculxqdypnfh:d8283cc0c6d1c05d5874a972d5176b29c24751188711916086c6e4537f035274@ec2-23-21-136-232.compute-1.amazonaws.com:5432/dfuo44q4pq80o6'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = 'mOon_jElLy wAs oRiGiNa11y g0nNa b3 SuP3r MaRi0 gAlAxY' # need to change later
# im not mocking Aidan, this key actually needs to be secure which is why it looks all crazy
# I feel personally attacked
# w

db = SQLAlchemy(app) # wow we have a database
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create our database model. 
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

  # initialize the object
  def __init__(self, email, first_name, last_name, is_admin, is_cardio, password):
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.is_admin = is_admin
    self.is_cardio = is_cardio
    self.password = password 
    self.initials = first_name[0] + last_name[0]

class Number_Users(db.Model):

  __tablename__ = "number_users_db"

  
  id = db.Column(db.Integer, primary_key=True)
  number_usersSu = db.Column(db.Integer)
  number_usersM = db.Column(db.Integer)
  number_usersT = db.Column(db.Integer)
  number_usersW = db.Column(db.Integer)
  number_usersTh = db.Column(db.Integer)
  number_usersF = db.Column(db.Integer)
  number_usersS = db.Column(db.Integer)
  #is_current = dbColumn(db.Boolean)

  # initialize the object
  def __init__(self, number_usersSu, number_usersM, number_usersT, number_usersW, number_usersTh, number_usersF, number_usersS):
    self.number_usersSu = number_usersSu
    self.number_usersM = number_usersM
    self.number_usersT = number_usersT
    self.number_usersW = number_usersW
    self.number_usersTh = number_usersTh
    self.number_usersF = number_usersF
    self.number_usersS = number_usersS
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
  #is_current = dbColumn(db.Boolean)

  # initialize the object
  def __init__(self, Su1, M1, T1, W1, Th1, F1, S1):
    self.Su1 = Su1
    self.M1 = M1
    self.T1 = T1
    self.W1 = W1
    self.Th1 = Th1
    self.F1 = F1
    self.S1 = S1
    #self.is_current = True

# database table
class UserTable(Table):
    id = Col('id')
    email = Col('Email')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    initials = Col('initials')
    is_admin = Col('Administrator?')
    is_cardio = Col('Cardiologist?')
    password = Col('Password')

# this is used to save login states for each user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# wtf does this do
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)

# This is the main homepage for now. GET and POST are for web forms.

@app.route('/add', methods = ['GET', 'POST'])

def add(): 
  # define a form object
  user_form = UserForm()

  # if we are posting a form, i.e. submitting a form, store all the info in these variables
  if request.method == 'POST':
    email = request.form['email']
    first_name = request.form['first_name'] 
    last_name = request.form['last_name']
    is_cardio = False

    # if the inputs we're all validated by WTforms (improve validation later)
    if user_form.validate(): 
      # then store info in an initialized User object and store the object in the database
      new_user = User(email, first_name, last_name, is_admin = False, is_cardio = is_cardio, password = "abc" )
      db.session.add(new_user) # add to database
      db.session.commit() # for some reason we also need to commit it otherwise it won't add
      return redirect('/users')#go to schedule after submit
    else:
      print("Invalid input(s)!")

  # add html file here
  return render_template('add.html', form = user_form)

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
  return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html')

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
def users():
  u = User.query.all()
  utable = UserTable(u)
  return render_template('users.html', utable=utable)

  #create a schedule page
@app.route('/make', methods=['GET', 'POST'])
def make():

  numuForm = NumberUsersForm()


  if request.method == 'POST':

    if(request.form['NumberUsersM'].isdigit()):
      number_usersM = int(request.form['NumberUsersM'])

    if(request.form['NumberUsersT'].isdigit()):
      number_usersT = int(request.form['NumberUsersT'])
    
    if(request.form['NumberUsersW'].isdigit()):
     number_usersW = int(request.form['NumberUsersW'])
    
    if(request.form['NumberUsersTh'].isdigit()):
     number_usersTh = int(request.form['NumberUsersTh'])
    
    if(request.form['NumberUsersF'].isdigit()):
      number_usersF = int(request.form['NumberUsersF'])
    
    if(request.form['NumberUsersS'].isdigit()):
     number_usersS = int(request.form['NumberUsersS'])
    
    if(request.form['NumberUsersSu'].isdigit()):
      number_usersSu = int(request.form['NumberUsersSu'])
   

    if numuForm.validate(): 
      new_number_users = Number_Users(number_usersSu, 
                                      number_usersM, 
                                      number_usersT, 
                                      number_usersW, 
                                      number_usersTh, 
                                      number_usersF, 
                                      number_usersS)
      db.session.add(new_number_users)
      db.session.commit()

      return redirect('/make2')
  return render_template('make.html', numuForm = numuForm)

@app.route('/make2', methods=['GET', 'POST'])
def make2():

  #global variables for making schedule

  Su1 = []
  M1= []
  T1 = []
  W1 = []
  Th1 = []
  F1 = []
  S1 = []


  NU = Number_Users.query.all()

  userfirstNamesSu = ["first_name"]*NU[-1].number_usersSu
  userfirstNamesM = ["first_name"]*NU[-1].number_usersM
  userfirstNamesT = ["first_name"]*NU[-1].number_usersT
  userfirstNamesW = ["first_name"]*NU[-1].number_usersW
  userfirstNamesTh = ["first_name"]*NU[-1].number_usersTh
  userfirstNamesF = ["first_name"]*NU[-1].number_usersF
  userfirstNamesS = ["first_name"]*NU[-1].number_usersS
  SchedForm = ScheduleForm(request.form,
                           userfirstNamesSu=userfirstNamesSu,
                           userfirstNamesM=userfirstNamesM,
                           userfirstNamesT=userfirstNamesT,
                           userfirstNamesW=userfirstNamesW,
                           userfirstNamesTh=userfirstNamesTh,
                           userfirstNamesF=userfirstNamesF,
                           userfirstNamesS=userfirstNamesS)
  


  if request.method == 'POST':
    
    for entry in SchedForm.userfirstNamesSu.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Su1.append(U1.id)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesM.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        M1.append(U1.id)
      else:
        print("not a valid first name")
    
    for entry in SchedForm.userfirstNamesT.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        T1.append(U1.id)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesW.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        W1.append(U1.id)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesTh.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        Th1.append(U1.id)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesF.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        F1.append(U1.id)
      else:
        print("not a valid first name")

    for entry in SchedForm.userfirstNamesS.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        U1 = User.query.filter_by(first_name=entry.data.get("first_name")).first()
        S1.append(U1.id)
      else:
        print("not a valid first name")


    if SchedForm.validate(): 
      new_users_that_day = Users_That_Day(Su1, M1, T1, W1, Th1, F1, S1)
      db.session.add(new_users_that_day) # add to database
      db.session.commit()
      return(redirect('/schedule'))
  
  print("SchedForm.errors = ", SchedForm.errors)
  #print("Su1 = ",Su1)

  return render_template('make2.html', schedForm = SchedForm)

@app.route('/schedule')
@login_required
def schedule():
  
  UTD = Users_That_Day.query.all()
  print("UTD = ", UTD)

  if(UTD == []):
    return render_template('schedule.html', Suulist = None, 
                                         Mulist = None, 
                                         Tulist = None, 
                                         Wulist = None, 
                                         Thulist = None, 
                                         Fulist = None, 
                                         Sulist = None)
  else:
    Su1 = UTD[-1].Su1
    M1 = UTD[-1].M1
    T1 = UTD[-1].T1
    W1 = UTD[-1].W1
    Th1 = UTD[-1].Th1
    F1 = UTD[-1].F1
    S1 = UTD[-1].S1
    return render_template('schedule.html', Suulist = Su1, 
                                         Mulist = M1, 
                                         Tulist = T1, 
                                         Wulist = W1, 
                                         Thulist = Th1, 
                                         Fulist = F1, 
                                         Sulist = S1)

def sorter(Su1, M1, T1, W1, Th1, F1, S1):
  print("<User1> type = ", type(Su1[0]))
  print("<User1> name = ", Su1[0].first_name)

  #if(Su1[0] != User.query.filter_by(first_name="Test1").first()):
    #print("Su1 first shouldnt be Test1")
  print("Su1 = ", Su1)
  print("M1 = ", M1)
  print("T1 = ", T1)
  print("W1 = ", W1)
  print("Th1 = ", Th1)
  print("F1 = ", F1)
  print("S1 = ", S1)

  return()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))



if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
