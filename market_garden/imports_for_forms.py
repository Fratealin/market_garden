from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from market_garden.models import User
from wtforms.widgets import TextArea