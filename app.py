import os
import subprocess
from flask_mail import Mail
from flask import make_response, Flask, render_template, request, redirect, send_from_directory, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, UserForm, DeleteForm, RegisterForm
from flask_table import Table, Col
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
mail = Mail(app)
                           
#let website reload properly 
app.config['ASSETS_DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = 'mOon_jElLy wAs oRiGiNa11y g0nNa b3 SuP3r MaRi0 gAlAxY' # need to change later
# im not mocking Aidan, this key actually needs to be secure which is why it looks all crazy
# I feel personally attacked

db = SQLAlchemy(app) # wow we have a database
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create our database model. 
class User(UserMixin, db.Model):

  __tablename__ = "users"

  # Each user (doctor) will have all these things attributed to him or her
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.Text, unique=True)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)
  is_admin = db.Column(db.Boolean)
  is_cardio = db.Column(db.Boolean)
  initial = db.Column(db.Text)
  password = db.Column(db.Text)

  # initialize the object
  def __init__(self, email, first_name, last_name, is_admin, is_cardio, password):
    self.email = email
    self.first_name = first_name
    self.last_name = last_name
    self.is_admin = is_admin
    self.is_cardio = is_cardio
    self.password = password 
    self.initial = first_name[0] + last_name[0]

# this is used to save login states for each user
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# wtf does this do
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)

# database table
class UserTable(Table):
    id = Col('id')
    email = Col('Email')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    is_admin = Col('Administrator?')
    is_cardio = Col('Cardiologist?')
    initials = Col('Initials')
    password = Col('Password')

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


@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
  if current_user.is_admin == None:
    return redirect(url_for('homepage'))
  else:
    # define a form object
    user_form = UserForm()

  if request.method == 'POST': # for some reason request.method is 'GET' now??
    first_name = request.form['first_name'] 
    last_name = request.form['last_name']
    email = request.form['email']
    is_cardio = request.form['is_cardio']
    
    # if the inputs we're all validated by WTforms (improve validation later)
    if user_form.validate(): 
      if is_cardio == 'True':
        is_cardio = True
      else:
        is_cardio = False
      new_user = User(email, first_name, last_name, False, is_cardio, 'lolwat')
      db.session.add(new_user) # add to database
      db.session.commit() # for some reason we also need to commit it otherwise it won't add
      return redirect(url_for('homepage')) # go to homepage again 
    else:
      print("Invalid input(s)!")
  else:
    print(request.method)
  return render_template('add.html', form = user_form)




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
        return redirect(url_for('schedule'))
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
@login_required
def schedule():
  # current_user is where the logged in user is stored

  u = User.query.all()
  utable = UserTable(u)
  #cardi = User.query.filter_by(specialty="cardiologist").all()
  return render_template('schedule.html', users=u, utable=utable)

#test to print out the first names of users 
@app.route('/users')
def users():
  u = User.query.all()
  utable = UserTable(u)
  return render_template('users.html', utable=utable)

#return render_template('home.html', form = user_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
