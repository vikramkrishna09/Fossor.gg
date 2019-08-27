from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from op_gg.Summoner import Summoner
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = os.urandom(31)
app.config['SESSION_TYPE'] = 'filesystem'
apikey = "RGAPI-9096e972-751b-436c-ab39-5fca1aef6fa4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config.from_object(__name__)
Session = Session()
Session.init_app(app)
from op_gg import routes