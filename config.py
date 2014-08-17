import os
import bcrypt

class Config(object):
    DEBUG = False
    CSRF_ENABLED = False
    CSRF_SESSION_KEY = 'a very secret thing indeed'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = '$2a$12$lNfETttuPMfsXnWR3JKgOO'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False


class HerokuConfig(Config):
    # db config from Config will do, but set any other env vars
    # specific to heroku here
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    URI = os.environ.get('DBURI')
    DB = os.environ.get('DBNAME')
    USER = os.environ.get('DBUSER')
    PASS = os.environ.get('DBPASS')

    # format is dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://%s:%s@%s/%s" %  (USER, PASS, URI, DB)

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
