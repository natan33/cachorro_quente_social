import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-bem-forte'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://user:password@localhost/hotdog_sales_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'noreply@yourdomain.com' # Email de envio padrão

    # Configurações Flask-Executor (opcional, para mais workers)
    EXECUTOR_TYPE = 'thread' # ou 'process', 'eventlet', 'gevent'
    EXECUTOR_MAX_WORKERS = 5