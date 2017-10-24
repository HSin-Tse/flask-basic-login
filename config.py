# sqlite
import os




class BaseConfig(object):
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dbs/ajstatic.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"
    SECRET_KEY = "SOME SECRET"
    # SECRET_KEY = 'my_precious'
    # DEBUG = False
    # BCRYPT_LOG_ROUNDS = 13
    # WTF_CSRF_ENABLED = True
    # DEBUG_TB_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = False
    # WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    # DEBUG_TB_ENABLED = True
