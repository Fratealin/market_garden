from market_garden.models import User, Veg_descriptions, Veg_model
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask import session
from flask import abort
from market_garden import app, db, bcrypt
from market_garden.login_forms import RegistrationForm, LoginForm
from market_garden.update_account_form import UpdateAccountForm
from market_garden.order_form import OrderForm, BookingForm, VegForm
from market_garden.contact_forms import ContactForm
import market_garden.output_generator
import datetime
import json
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import market_garden.models
import market_garden.conversation

from market_garden import email_manager

from sqlalchemy import func


weather_text = market_garden.output_generator.construct_weather_text()

today = datetime.now()
# Textual month, day and year
date = today.strftime("%B %d, %Y %H:%M")
test_variable= "as"

@app.route('/', methods=["GET", "POST"])
#This means you need to login to get to this route.
#Also need to add location of login page to loginmanager in init
#@login_required
def index():
    #name = current_user.__getattr__(name="username")
    form = OrderForm()
    owner = market_garden.models.get_json_data("owner")

    try:
        vegbox_size = form.vegbox_size.data
        print(vegbox_size + "-------------")
    except:
        print("no")


    if form.validate_on_submit():
        vegbox_size = form.vegbox_size


        if form.register.data:
            return redirect(url_for("register", vegbox_size=vegbox_size))
        else:
            return redirect(url_for("login", vegbox_size=vegbox_size))





    return render_template('index.html', owner=owner, form=form)

@app.route("/register", methods=["GET", "POST"])
def register(vegbox_size="small"):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        #create database entry then commit to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, box_size="", pickup_time="", address="")
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created {form.username.data.title()}! You are now able to log in', 'success')
        return redirect(url_for("login"))
    else:
        flash(f'not successful', 'success')
    return render_template('register.html', title='Register', form=form, vegbox_size=vegbox_size)

@app.route("/login", methods=["GET", "POST"])
def login(vegbox_size="small"):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():


        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log in user
            login_user(user, remember=form.remember.data)
            # args is a dictionary. get returns none if doesn't exist.
            # This finds out if you had tried to access a page before logging in.
            # If so, then we will go there
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('veg_box'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/veg_box", methods=["GET", "POST"])
#@login_required
def veg_box():
    form = BookingForm()

    if form.validate_on_submit():

        current_user.box_size = form.vegbox_size.data
        current_user.pickup_time = form.pickup_time.data
        current_user.address = form.input_text.data
        db.session.commit()


        message_to_customer = email_manager.order_received_message(current_user)
        #TODO: This is to allow for no config file

        try:
            email_manager.send_email(message_to_customer, current_user.email, subject="Thank you for your order")
        except:
            with open("emails/message_to_customer.txt", "w") as file:
                file.write(message_to_customer)




        # get list of all bookings
        users = User.query.all()
        vegbox_orders = []
        for user in users:
            line = "\t".join([user.username, user.box_size, user.pickup_time, user.address])
            vegbox_orders.append(line)
        "\n".join(vegbox_orders)
        message_to_picked = email_manager.new_order_message(current_user, "\n".join(vegbox_orders))
        #TODO: This is to allow for no config file
        try:
            email_manager.send_email(message_to_picked, "alisensei@gmail.com", subject="New order received")
        except:
            with open("emails/New order received.txt", "w") as file:
                file.write(message_to_picked)

        flash(
            f'Your booking has been succesful, and an email reminder has been sent.{message_to_picked} {message_to_customer}',
            'success')

        return redirect(url_for('veg_box'))

    elif request.method == 'GET':
        form.vegbox_size.data = current_user.box_size
        form.pickup_time.data = current_user.pickup_time
        form.input_text.data = current_user.address



    return render_template('veg_box.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    name = current_user.__getattr__(name="username")
    email = current_user.__getattr__(name="email")
    password = current_user.__getattr__(name="password")

    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.send_email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    # This populates our form with the current users data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.send_email


    # TODO put this back
    image_file = url_for('static', filename='static/' + current_user.image_file)
    image_file = 'static/default.jpg'


    return render_template('account.html', title='Account', name=name, email=email, image_file=image_file,
                           password=password, form=form)

@app.route("/about")
@login_required
def todo_page():
    #TODO
    from market_garden.todo import todos

    return render_template('todo.html', title='Todos', todos=todos())

@app.route("/veg")
def veg():
    #TODO
    veg_img_dict =[
                   {"veg":"chard", "image_file":'static/chard.jpg', "text":"Delicious steamed and in salads\nTry me in currys and dahls\nYou can use my stalks instead of celery in stews!"},
                   {"veg":"cavolo nero", "image_file":'static/kale.jpg', "text":"Delicious steamed in kale salad, kale smoothies, dahls etc"},
                    {"veg":"shiso", "image_file":'static/shiso.jpeg', "text":"Japanese Herb fantastic in Asian dishes"}]

    veg_descriptions = Veg_descriptions.query.all()

    return render_template('veg.html', title='About our veg', veg_img_dict=veg_img_dict, veg_descriptions=veg_descriptions)

@app.route("/veg/edit", methods=["GET", "POST"])
@login_required
def edit_veg():
    form = VegForm()
    if form.validate_on_submit():
        veg_description = Veg_descriptions(veg_name=form.veg_name.data, description = form.description.data, image_file = form.image_file.data, author = current_user.username)
        db.session.add(veg_description)
        db.session.commit()
        flash('New veg description has been created!', 'success')
        return redirect(url_for('veg'))

    return render_template('edit_veg.html', title='Edit veg', form=form)

@app.route("/veg/edit/<int:veg_id>")
def veg_update(veg_id):
    # This displays a page with one veg only
    veg = Veg_descriptions.query.get_or_404(veg_id)
    return render_template('veg_update.html', title = veg.veg_name, veg= veg)

@app.route("/veg/edit/<int:veg_id>/update")
def veg_update_details(veg_id):
    veg = Veg_descriptions.query.get_or_404(veg_id)
    if veg.author != current_user:
        abort(403)
    form = VegForm()
    return render_template('edit_veg.html', title='Update veg', form=form)





@app.route("/get_user_name")
def get_user_name():
    return render_template("get_user_name.html")




@app.route("/bye")
def bye():
    return render_template("bye.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():






    form = ContactForm()





    if form.validate_on_submit():
        message = form.message.data
        subject = form.subject.data
        email = form.email.data
        #TODO this is to allow for no config file
        try:
            email_manager.send_email(message, "ali_sensei@gmail.com", subject=subject)
        except:
            print("email")
            with open(f"emails/{subject}.txt", "w") as file:
                file.write(message)


        flash(f'Your question has been sent and a copy has been sent to you.\nWe will try to reply within 365 days.\n{message}', 'success')

        return redirect(url_for('contact'))


    # TODO put this back
    image_file = url_for('static', filename='static/')
    image_file = 'static/default.jpg'

    return render_template('contact.html', title='Contact',  image_file=image_file, form=form)


@app.route("/make_veg_list", methods=["GET", "POST"])
def make_veg_list():
    with open('market_garden/cost_per_mile.json', "r") as f:
        data = json.load(f)
        our_stuff = data['our_veg']
        veg_selected = request.form.getlist('veg')
        veg_not_already_in_list = set(veg_selected) - set(our_stuff)
        our_veg = our_stuff + list(veg_not_already_in_list)
        data['our_veg'] = our_veg
    debug = ""
    if request.form.get("bespoke_selected"):
        if not all([request.form.get("bespoke_veg").title(), request.form.get("unit")]):
            flash('Please select veg name and unit', 'danger')
        else:
            bespoke_veg=request.form.get("bespoke_veg").title() + " (" + request.form.get("unit") + ")"
            our_veg.append(bespoke_veg)
        """
        for item in list(veg_not_already_in_list):
            veg_model = User(veg_name = item)
        db.session.add(veg_model)
        db.session.commit()
        """


    with open('market_garden/cost_per_mile.json', 'w') as f:
        json.dump(data, f, indent=4)
    import market_garden.veg_prices

    veg_list = market_garden.veg_prices.get_veg_list()
    return render_template("make_veg_list.html", veg_list=veg_list, our_veg=our_veg, debug=debug)

@app.route("/edit_prices", methods=["GET", "POST"])
def edit_prices():
    with open('market_garden/cost_per_mile.json', "r") as f:
        data = json.load(f)
        our_veg = data['our_veg']
        #print(our_veg)
        #veg_selected = request.form.getlist('veg')
        #veg_not_already_in_list = set(veg_selected) - set(our_stuff)
        #our_veg = our_stuff + list(veg_not_already_in_list)

        #data['our_veg'] = our_veg
        debug = ""


    import market_garden.veg_prices

    veg_list = market_garden.veg_prices.get_veg_list()
    prices = []

    our_prices = market_garden.models.get_json_data("our_prices")

    import itertools

    for veg, our_price in itertools.zip_longest(our_veg, our_prices):
        price_list = market_garden.veg_prices.get_unit_price(veg)
        #print(len(price_list), veg)


        our_veg_index = our_veg.index(veg)
        #print(our_veg_index)
        # if no our price for this veg, it will fill it in blank
        if len(price_list) < 4:

            #print(veg, len(price_list))
            #price_list = [1, 2, 3, 4]
            if our_price:

                price_list.append(our_price)



            else:
                #print(veg, len(price_list))
                price_list.append("")
                #print(veg, len(price_list))



        else:
            price_list[3] = our_price
        prices.append(price_list)

    """
    data['our_prices'] = our_prices
    with open('market_garden/cost_per_mile.json', 'w') as f:
        json.dump(data, f, indent=4)
    """


    return render_template("edit_prices.html", veg_list=veg_list, our_veg=our_veg, prices=prices, debug=debug)


@app.route('/do_edit_prices', methods=["GET",'POST'])
def do_edit_prices():
    inputted_prices = request.form.getlist("updated_prices")
    updated_prices = []
    for inputted_price in inputted_prices:
        try:
            updated_price = float(inputted_price)
            #make it into currency format
            updated_price = "{:.2f}".format(updated_price)
            updated_prices.append(updated_price)
        except ValueError:
            updated_prices.append("")


    with open('market_garden/cost_per_mile.json', "r") as f:
        data = json.load(f)


    with open('market_garden/cost_per_mile.json', 'w') as f:
        data['our_prices'] = updated_prices
        json.dump(data, f, indent=4)




    return redirect(url_for('edit_prices'), code=307)



@app.route("/weather", methods=["GET", "POST"])
def weather():
    return render_template("weather.html", weather_text = weather_text)






@app.route('/user_rec', methods=["GET",'POST'])
def user_rec():
    return redirect(url_for('make_veg_list'), code=307)


