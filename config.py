import os

class BaseConfig(object):
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
	DEBUG=False
	TESTING=False
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['your-email@example.com']

class DevelopmentConfig(BaseConfig):
	DEBUG=True
	TESTING=True

class TestingConfig(BaseConfig):
	DEBUG=False
	TESTING=True