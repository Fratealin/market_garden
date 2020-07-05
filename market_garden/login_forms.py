from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from market_garden.models import User


"""
#TODO: Make it an environment variable later
Put this line in main file
app.config['SECRET_KEY'] = 'efc2a7367636234467d8d318385c69fc'
Secret key protects against modified cookies, cross site attacks, forgeries, etc.
Toget secret key, go to python command line and type this:
import secrets
secrets.token_hex(16)
"""

#Create a class which inherits from FlaskForm.
#Each form field are imported classes
#Add another requirements, called validators, as arguments. DataRequired means can't be empty
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #vegbox_size = SelectField(label="Vegbox Size", choices =[('Large Box', 'Large Box') , ('Small Box', 'Small Box')])


    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # search to find user with the same name.
        # if one doesn't exist, it will come back as None.
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        # search to find user with the same name.
        # if one doesn't exist, it will come back as None.
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

