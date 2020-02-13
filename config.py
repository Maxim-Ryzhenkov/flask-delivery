import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret_key'
    RECAPTCHA_PUBLIC_KEY = "qwerty123"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ROOT_DIR = basedir

    # Настройки Flask-Mail
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ryzhenkov.maksim@yandex.ru'
    MAIL_PASSWORD = 'xxxxxxxxxxxx'

