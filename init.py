from flask import Flask
from flask_mail import Mail
from flask_mysqldb import MySQL

import configuration


def initiation():
    app = Flask(__name__)
    mysql = configuration.database_config(app)
    mail = configuration.mail_config(app)
    return app, mysql, mail
