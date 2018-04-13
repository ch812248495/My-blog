from flask_mysqldb import MySQL
from flask_mail import Mail

def database_config(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '812248'
    app.config['MYSQL_DB'] = 'SocialBlog'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)
    return mysql


def mail_config(app):
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'caoheng1994@outlook.com'
    app.config['MAIL_PASSWORD'] = 'a812248495'

    mail = Mail(app)
    return mail


