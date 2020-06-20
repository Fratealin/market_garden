from mileage_craic.imports_for_forms import *
from flask_login import current_user

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
class UpdateAccountForm(FlaskForm):
    input_text = StringField('Enter text', validators=[DataRequired(), Length(min=2, max=400)])
    text_body = StringField(u'Text', widget=TextArea())
    single_line = StringField('single line', validators=[DataRequired()])

    weather_url = StringField('Your local BBC weather link.\nYou can find it here:\n\thttps://www.bbc.co.uk/weather', validators=[DataRequired(), Length(min=2, max=40)])
    cost_per_mile = StringField('Cost per mile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')
    """

    def validate_username(self, username):
        if username.data != current_user.username:
            # search to find user with the same name.
            # if one doesn't exist, it will come back as None.
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')
    """
    def validate_email(self, email):
        if email.data !=current_user.email:
            # search to find user with the same name.
            # if one doesn't exist, it will come back as None.
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# I think this is not needed



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
