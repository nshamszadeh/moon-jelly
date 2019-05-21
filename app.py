import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, UserForm, DeleteForm, ScheduleForm, ScheduleEntryForm, NumberUsersForm
from flask_table import Table, Col

# Some boilerplate setup stuff.

app = Flask(__name__)

# URL should be whatever database URL is being used (if testing on your own use a database different from the team's )

#let website reload properly 
app.config['ASSETS_DEBUG'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ricculxqdypnfh:d8283cc0c6d1c05d5874a972d5176b29c24751188711916086c6e4537f035274@ec2-23-21-136-232.compute-1.amazonaws.com:5432/dfuo44q4pq80o6'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = 'mOon_jElLy wAs oRiGiNa11y g0nNa b3 SuP3r MaRi0 gAlAxY' # need to change later
# im not mocking Aidan, this key actually needs to be secure which is why it looks all crazy
# I feel personally attacked

db = SQLAlchemy(app) # wow we have a database
migrate = Migrate(app, db)

#number_users = 3

# Create our database model. 
class User(db.Model):

  __tablename__ = "users" ##what does this do?

  # Each user (doctor) will have all these things attributed to him or her
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.Text, unique=True)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)
  specialty = db.Column(db.Text)
  initials = db.Column(db.Text)

  # initialize the object
  def __init__(self, email, first_name, last_name, specialty):
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.specialty = specialty
    self.initials = first_name[0] + last_name[0]

class UserTable(Table):
    id = Col('id')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    specialty = Col('Specialty')
    email = Col('Email')
    initials = Col('initials')

class ScheduleTable(Table):
    
    Sunday = Col('Sun')
    Monday = Col('Mon')
    Tuesday = Col('Tues')
    Wednesday = Col('Weds')
    Thursday = Col('Thrus')
    Friday = Col("Fri")
    Saturday = Col("Sat")

    #def __init__(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday):




#create a log in page
@app.route('/', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == 'POST':
    email = request.form['email']
    if User.query.filter_by(email=email).first():
      return redirect('/add')#go to schedule after submit 
    else:
      print("Invalid input(s)!")
  return render_template('login.html', form=form)


@app.route('/make', methods=['GET', 'POST'])
def make():
  numuForm = NumberUsersForm()

  global number_usersM  # This is gross, gonna find a way to pass variables from one page to another later
  global number_usersT
  global number_usersW
  global number_usersTh
  global number_usersF
  global number_usersS
  global number_usersSu


  if request.method == 'POST':
    number_usersM = int(request.form['NumberUsersM']) # THIS DOESNT HANDLE EDGE CASES YET, BREAKS IF YOU INPUT A NUMBER, GONNA NEED TO FIX
    number_usersT = int(request.form['NumberUsersT'])
    number_usersW = int(request.form['NumberUsersW'])
    number_usersTh = int(request.form['NumberUsersTh'])
    number_usersF = int(request.form['NumberUsersF'])
    number_usersS = int(request.form['NumberUsersS'])
    number_usersSu = int(request.form['NumberUsersSu'])
    if numuForm.validate():
      return redirect('/make2')
  return render_template('make.html', numuForm = numuForm)

@app.route('/make2', methods=['GET', 'POST'])
def make2():

  #global variables for making schedule
  global Su1 
  global M1
  global T1 
  global W1 
  global Th1
  global F1 
  global S1 

  
  Su1_1 = []
  M1_1 = []
  T1_1 = []
  W1_1 = []
  Th1_1 = []
  F1_1 = []
  S1_1 = []

  userfirstNamesSu = ["first_name"]*number_usersSu
  userfirstNamesM = ["first_name"]*number_usersM
  userfirstNamesT = ["first_name"]*number_usersT
  userfirstNamesW = ["first_name"]*number_usersW
  userfirstNamesTh = ["first_name"]*number_usersTh
  userfirstNamesF = ["first_name"]*number_usersF
  userfirstNamesS = ["first_name"]*number_usersS
  SchedForm = ScheduleForm(request.form,
                           userfirstNamesM=userfirstNamesM,
                           userfirstNamesT=userfirstNamesT,
                           userfirstNamesW=userfirstNamesW,
                           userfirstNamesTh=userfirstNamesTh,
                           userfirstNamesF=userfirstNamesF,
                           userfirstNamesS=userfirstNamesS,
                           userfirstNamesSu=userfirstNamesSu)
  


  if request.method == 'POST':
    
    for entry in SchedForm.userfirstNamesSu.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        Su1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    Su1 = Su1_1

    for entry in SchedForm.userfirstNamesM.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        M1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    M1 = M1_1
    
    for entry in SchedForm.userfirstNamesT.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        T1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    T1 = T1_1

    for entry in SchedForm.userfirstNamesW.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        W1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    W1 = W1_1

    for entry in SchedForm.userfirstNamesTh.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        Th1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    Th1 = Th1_1

    for entry in SchedForm.userfirstNamesF.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        F1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    F1 = F1_1

    for entry in SchedForm.userfirstNamesS.entries:
      if User.query.filter_by(first_name=entry.data.get("first_name")).first() != None:
        S1_1.append(User.query.filter_by(first_name=entry.data.get("first_name")).first())
      else:
        print("not a valid first name")

    S1 = S1_1


    if SchedForm.validate(): 
      return(redirect('/schedule'))
  
  print("SchedForm.errors = ", SchedForm.errors)
  #print("Su1 = ",Su1)

  return render_template('make2.html', schedForm = SchedForm)
  

    
###WRITE A BEEEG SORTING FUNCTION, then export it to qi's table?






@app.route('/schedule2')
def schedule2():
  u = User.query.all()
  utable = UserTable(u)

  return render_template('schedule2.html', users=u, utable=utable)


# This is the main homepage for now. GET and POST are for web forms.
@app.route('/add', methods = ['GET', 'POST'])
def add():
  
  # define a form object
  user_form = UserForm()

  # if we are posting a form, i.e. submitting a form, store all the info in these variables
  if request.method == 'POST':
    first_name = request.form['first_name'] 
    last_name = request.form['last_name']
    email = request.form['email']
    specialty = request.form['specialty']

    # if the inputs we're all validated by WTforms (improve validation later)
    if user_form.validate(): 
      # then store info in an initialized User object and store the object in the database
      new_user = User(email, first_name, last_name, specialty)
      db.session.add(new_user) # add to database
      db.session.commit() # for some reason we also need to commit it otherwise it won't add
      return redirect('/users')#go to schedule after submit
    else:
      print("Invalid input(s)!")

  # add html file here
  return render_template('add.html', form = user_form)


@app.route('/remove', methods = ['GET', 'POST'])
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

  # add html file here
  return render_template('remove.html', delete_form = delete_form)

@app.route('/about')
def about():
  return render_template('about.html')


#test to print out the first names of users 
@app.route('/users')
def users():
  u = User.query.all()
  utable = UserTable(u)
  return render_template('users.html', utable=utable)

  #create a schedule page
@app.route('/schedule')
def schedule():

  #stable = ScheduleTable(Sunday = Su1, Monday = M1, Tuesday = T1, Wednesday = W1, Thursday = Th1, Friday = F1, Saturday = S1)
  Suulistloc = "empty"
  Mulistloc = "empty"
  Tulistloc = "empty"
  Wulistloc = "empty"
  Thulistloc = "empty"
  Fulistloc = "empty"
  Sulistloc = "empty"

  numberSuloc = 0
  numberMloc = 0
  numberTloc = 0
  numberWloc = 0
  numberThloc = 0
  numberFloc = 0
  numberSloc = 0
  
  try: number_usersSu
  except NameError: numberSuloc = None
  if(numberSuloc != None):
    numberSuloc = number_usersSu
  
  try: number_usersM
  except NameError: numberMloc = None
  if(numberMloc != None):
    numberMloc = number_usersM
  
  try: number_usersT
  except NameError: numberTloc = None
  if(numberTloc != None):
    numberMToc = number_usersT
  
  try: number_usersW
  except NameError: numberWloc = None
  if(numberWloc != None):
    numberWloc = number_usersW

  try: number_usersTh
  except NameError: numberThloc = None
  if(numberThloc != None):
    numberThloc = number_usersTh

  try: number_usersF
  except NameError: numberFloc = None
  if(numberFloc != None):
    numberFloc = number_usersF

  try: number_usersS
  except NameError: numberSloc = None
  if(numberSloc != None):
    numberSloc = number_usersS


#dealing with gross global variables LIST NAMES
  try: Su1
  except NameError: Suulistloc = None
  if(Suulistloc != None):
    Suulistloc = Su1
  
  try: M1
  except NameError: Mulistloc = None
  if(Mulistloc != None):
    Mulistloc = M1
  
  try: T1
  except NameError: Tulistloc = None
  if(Tulistloc != None):
    Tulistloc = T1
  
  try: W1
  except NameError: Wulistloc = None
  if(Wulistloc != None):
    Wulistloc = W1

  try: Th1
  except NameError: Thulistloc = None
  if(Thulistloc != None):
    Thulistloc = Th1


  try: F1
  except NameError: Fulistloc = None
  if(Fulistloc != None):
    Fulistloc = F1


  try: S1
  except NameError: Sulistloc = None
  if(Sulistloc != None):
    Sulistloc = S1


  return render_template('schedule.html', Suulist = Suulistloc, 
                                         Mulist = Mulistloc, 
                                         Tulist = Tulistloc, 
                                         Wulist = Wulistloc, 
                                         Thulist = Thulistloc, 
                                         Fulist = Fulistloc, 
                                         Sulist = Sulistloc)

#return render_template('home.html', form = user_form)

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
