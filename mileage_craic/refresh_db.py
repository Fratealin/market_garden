# Doesn't work

from mileage_craic import db
db.create_all()
from mileage_craic.models import User, Voyage
from flask import Flask

app = Flask(__name__)

user_1 = User(username='Ali', email='a@a.com', password='password')