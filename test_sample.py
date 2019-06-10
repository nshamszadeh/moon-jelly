# content of test_sample.py
import os
import tempfile
import pytest
import flask_migrate

from werkzeug.security import generate_password_hash

from app import app, db, User


@pytest.fixture
def client():
    dburi = 'postgres://postgres:l315l315@localhost/moon_jelly_test'
    app.config['SQLALCHEMY_DATABASE_URI'] = dburi
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False 
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()

    admin = User(first_name='Test', last_name='Admin', email='test@admin.com', is_admin=True, is_cardio=True, password='asdf')
    admin.password = generate_password_hash('asdf', method = 'sha256')
    db.session.add(admin)
    
    user1 = User(first_name='Test', last_name='User', email='test@user.com', is_admin=False, is_cardio=False, password='asdf')
    user1.password = generate_password_hash('asdf', method = 'sha256')
    db.session.add(user1)
    db.session.commit()

    yield client

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Plan Your Future' in rv.data

def test_register(client):
    rv = client.post('/register', data=dict(
        first_name='a',
        last_name='a',
        email='12345678@gmail.com',
        is_cardio='1',
        password='abc123'
    ),follow_redirects=True)

    assert b'Sign In' in rv.data 

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def users(client):
    return client.get('/users',follow_redirects=True)

def test_login_logout(client):
    """Make sure login and logout works."""
    

    rv = login(client, "test@user.com", "asdf")
    #print(rv.data)
    assert b'Logout' in rv.data

    rv = logout(client)
    assert b'Sign In' in rv.data
   
def test_add_user(client):
    rv = login(client, "test@admin.com", "asdf")
    assert b'Logout' in rv.data

    oldcount = User.query.count()

    client.post('/add', data=dict(
        first_name='b',
        last_name='b',
        email='b@gmail.com',
        is_cardio='1',
        is_admin='0'
    ),follow_redirects=True)

    newcount = User.query.count()
    assert newcount == oldcount + 1
'''
import pytest
from app import User

@pytest.fixture(scope='module')
def new_user():
    user = User('hi@gmail.com', 'first', 'last', 'specialty')
    return user

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, name, and specialty are good to go
    """
    assert new_user.email == 'hi@gmail.com'
    assert new_user.first_name == 'first'
    assert new_user.last_name == 'last'
    assert new_user.specialty == 'specialty'
'''
    
