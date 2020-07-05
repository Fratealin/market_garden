# Doesn't work

from market_garden import db
db.create_all()
from market_garden.models import User, Voyage
from flask import Flask

app = Flask(__name__)

user_1 = User(username='Ali', email='a@a.com', password='password')