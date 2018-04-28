from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

CONNECT = 'sqlite://///home/tuti/PycharmProjects/jwt/database/database.db'
app.config['SECRET_KEY'] = b'<\x85b\x05\x90M\xef,\xc11P\xa9\xf6\xe0\x03\xc87\x83\x82\xeaZ\xe1\xeb<'
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
