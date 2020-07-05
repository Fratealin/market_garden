from market_garden.imports_for_forms import *

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
class ContactForm(FlaskForm):
    subject = StringField('Type subject here', render_kw={"placeholder": "Please enter a subject"})

    email = StringField('Email', validators=[DataRequired(), Email()])

    message = TextAreaField('input text', render_kw={"placeholder": "Please enter question"})

    number = FloatField('Number')
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

