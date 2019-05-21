import os
import subprocess

from flask import make_response, Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, UserForm, DeleteForm
from flask_table import Table, Col
from flask import flash, url_for

# Some boilerplate setup stuff.

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

db = SQLAlchemy(app) # wow we have a database
migrate = Migrate(app, db)

# Create our database model. 
class User(db.Model):

  __tablename__ = "users"

  # Each user (doctor) will have all these things attributed to him or her
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.Text, unique=True)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)
  specialty = db.Column(db.Text)

  # initialize the object
  def __init__(self, email, first_name, last_name, specialty):
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.specialty = specialty

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)

class UserTable(Table):
    id = Col('id')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    specialty = Col('Specialty')
    email = Col('Email')
'''
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style) 
    ''' 
#user_form = UserForm()
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
      return redirect('/schedule')#go to schedule after submit  ####This doesn't seem to work?
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
        return redirect('/schedule')
      else:
        print("User First Name Not Found")
    else:
      print("Invalid input(s)!")
      #Mbox('Warning!', 'Email is not correct!', 0)

  # add html file here
  return render_template('remove.html', delete_form = delete_form)


@app.route('/img/<path:path>')

def send_js(path):
    return send_from_directory('img', path)

@app.route('/about')

def about():
  return render_template('about.html')

@app.route('/contact')

def contact():
  try:
    message = subprocess.check_output(['hi'], shell=True)
  except:
    message = "Sorry, we coundn't run that command..."
  #dir:command you want to run(name)
  return render_template('contact.html', message=message)

#create a schedule page
@app.route('/schedule')
def schedule():
  u = User.query.all()
  utable = UserTable(u)
  #cardi = User.query.filter_by(specialty="cardiologist").all()
  return render_template('schedule.html', users=u, utable=utable)

#create a log in page
@app.route('/')

def homepage():
  return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])

def login():
  form = LoginForm()
  if request.method == 'POST' and form.validate():
    email = request.form['email']
    if User.query.filter_by(email=email).first():
      return redirect('/add')#go to schedule after submit 
    else:
      # print("Invalid input(s)!")
      form.email.errors.append('Invalid Email!')

  return render_template('login.html', form=form)

#test to print out the first names of users 
@app.route('/users')

def users():
  u = User.query.all()
  utable = UserTable(u)
  return render_template('users.html', utable=utable)

#return render_template('home.html', form = user_form)

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
