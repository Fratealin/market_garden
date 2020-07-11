from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
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


class OrderForm(FlaskForm):
    vegbox_size = SelectField(label="Vegbox Size", choices =[('Large Box', 'Large Box') , ('Small Box', 'Small Box')])
    login = SubmitField('Login')
    register = SubmitField('Register')


class BookingForm(FlaskForm):
    vegbox_size = SelectField(label="Vegbox Size", choices =[('Large Box', 'Large Box') , ('Small Box', 'Small Box')])
    pickup_time = SelectField(label="Next pickup date: Thursday", choices =[('12pm', '12pm') , ('1pm', '1pm')])
    input_text = TextAreaField('Address if delivery is required', render_kw={"placeholder": "Please have money ready on delivery"})
    submit = SubmitField('Place Order Now')

class VegForm(FlaskForm):
    veg_name = StringField('Produce name', validators =[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image_file = StringField('Image filename', validators=[DataRequired()])
    submit = SubmitField('Upload')




