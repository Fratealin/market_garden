from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



#not sure what this is for
app = Flask(__name__)

app.config['SECRET_KEY'] = 'efc2a7367636234467d8d318385c69fc'
#TODO: Make it an environment variable later
"""
Secret key protects against modified cookies, cross site attacks, forgeries, etc.
Toget secret key, go to python command line and type this:
import secrets
secrets.token_hex(16)
"""



#Database


# Set location of SQL light database. /// means relative path.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# generate instance of Bcrypt()
bcrypt = Bcrypt(app)

#Create database instance
#Represent structure as classes. Referred to as models.
db = SQLAlchemy(app)

#Makes it really easy to manage user sessions
#Add some functionality to our database models, and the LoginManager handles the sessions for us.
login_manager = LoginManager(app)
#Tell login_manager where login route is located
login_manager.login_view = 'login'
#bootstrap class to give a nice blue info alert
login_manager.login_message_category = "info"

from market_garden import routes