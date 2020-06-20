from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mileage_craic.models import User
from wtforms.widgets import TextArea