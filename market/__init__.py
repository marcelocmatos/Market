from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/market.db'
app.config['SECRET_KEY'] = '0fb59abbe2bb39814d80f1d1'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'acesso'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Por Favor, acesse antes de prosseguir para a loja'
from market import routes

