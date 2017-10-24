# sqlite
import os


#
# app.config.update(
#     MAIL_SERVER='smtp.partner.outlook.cn',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=True,
#     MAIL_DEFAULT_SENDER=os.environ.get('MAIL_USERNAME'),
#     MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
#     MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
# )

class BaseConfig(object):
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dbs/ajstatic.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"
    SECRET_KEY = "SOME SECRET"

    MAIL_SERVER = '''smtp.partner.outlook.cn''',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME'),
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SECRET_KEY = 'my_precious'
    # DEBUG = Falseａ
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
