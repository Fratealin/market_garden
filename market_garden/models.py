from market_garden import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

# This decorator reloads the user from the user id stored in a session.
# Need this in order for login_manager to work.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_json_data(what_you_want):
    with open('market_garden/cost_per_mile.json') as json_file:
        data = json.load(json_file)
        if what_you_want == 'cost_per_mile':
            return data['cost_per_mile']
        elif what_you_want == 'owner':
            return data['owner']
        elif what_you_want == 'our_veg':
            return data['our_veg']
        elif what_you_want == 'our_prices':
            return data['our_prices']

        else:
            return data['weather_url']


#UserMixin is added here because the UserMixin extension expects the User model to have four attributes.
class User(db.Model, UserMixin):
    #Automatically has a table name set to 'user'
    #Within user model, add columns for table.
    # Primary key means it is a unique id for the user.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)

    password = db.Column(db.String(60), nullable=False)

    box_size = db.Column(db.String(10), default="")

    pickup_time = db.Column(db.String(10), default="")

    address = db.Column(db.String(60), default="")

    # The following attribute has a relationship to Voyage model. When we go on a voyage, we use author attribute to get the User who embarked on a voyage.
    #voyages = db.relationship('Voyage', backref='author', lazy=True)

    # Magic method. Specify repr method: How our object is printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.box_size}', '{self.pickup_time}', '{self.address}')"



#Voyage class to hold Voyage chronicles.
class Veg_descriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veg_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    author = db.Column(db.String(20), nullable=False, default='')

    # Magic method. Specify repr method: How our object is printed out
    def __repr__(self):
        return f"Veg('{self.veg_name}', '{self.description}', '{self.image_file}', '{self.author}')"

class Veg_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veg_name = db.Column(db.String(100), nullable=False)
    wholesale_price = db.Column(db.String(100), default="")
    farm_price = db.Column(db.String, default="")
    supermarket_price = db.Column(db.String, default="")
    our_price=db.Column(db.String, default="")
    in_stock = db.Column(db.Boolean, default=True)

    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    # Magic method. Specify repr method: How our object is printed out
    def __repr__(self):
        return f"Veg_model('{self.veg_name}', '{self.wholesale_price}', '{self.farm_price}', , '{self.supermarket_price}', '{self.our_price}', '{self.in_stock}')"

