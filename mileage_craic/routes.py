from mileage_craic.models import User, Voyage
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask import session
from mileage_craic import app, db, bcrypt
from mileage_craic.login_forms import RegistrationForm, LoginForm
from mileage_craic.update_account_form import UpdateAccountForm
from mileage_craic.response_forms import ResponseForm
import mileage_craic.output_generator
import datetime
import json
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import mileage_craic.models

from sqlalchemy import func


weather_text = mileage_craic.output_generator.construct_weather_text()

today = datetime.now()
# Textual month, day and year
date = today.strftime("%B %d, %Y %H:%M")
test_variable= "as"

@app.route('/')
#This means you need to login to get to this route.
#Also need to add location of login page to loginmanager in init
@login_required
def index():
    name = current_user.__getattr__(name="username")
    owner = mileage_craic.models.get_json_data("owner")

    return render_template('index.html', name=name, owner=owner)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        #create database entry then commit to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created {form.username.data.title()}! You are now able to log in', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
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

            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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
    cost_per_mile = current_user.__getattr__(name="cost_per_mile")
    weather_url = current_user.__getattr__(name="weather_url")

    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.cost_per_mile = form.cost_per_mile.data
        current_user.weather_url = form.weather_url.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    # This populates our form with the current users data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.cost_per_mile.data = current_user.cost_per_mile
        form.weather_url.data = current_user.weather_url


    # TODO put this back
    image_file = url_for('static', filename='static/' + current_user.image_file)
    image_file = 'static/default.jpg'


    return render_template('account.html', title='Account', name=name, email=email, image_file=image_file,
                           cost_per_mile=cost_per_mile, weather_url=weather_url,  password=password, form=form)

@app.route("/about")
@login_required
def about():
    #TODO
    from mileage_craic.todo import todos

    return render_template('about.html', title='Account', todos=todos())


@app.route("/log_mileage", methods=["POST"])
def log_mileage():
    distance = request.form.get("distance")
    name = current_user.username
    journey_type = request.form.get("journey_type")
    passengers = request.form.get("passengers")

    if not all([distance, name, passengers]):
        return render_template("failure.html")
    if not journey_type:
        journey_type = "General"
    try:
        cost = float(distance)/int(passengers)*current_user.cost_per_mile
    except ValueError:
        return render_template("failure.html")

    #2dp
    cost = "{:.2f}".format(cost)

    # Write it to a db
    # If you want to do this the consistent way. Watch https://www.youtube.com/watch?v=u0oDDZrDz9U&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=8
    voyage = Voyage(voyage_type=journey_type, passengers=passengers, distance=distance, cost=cost, weather_text=weather_text, date_posted=date, author=current_user)
    db.session.add(voyage)
    db.session.commit()
    return redirect("/mileage_logged", code=307)


    #return render_template("mileage_logged.html", text=text, mydate=mydate, name=name, journey_type=journey_type, passengers= passengers, distance=distance)


@app.route("/get_user_name")
def get_user_name():
    return render_template("get_user_name.html")

@app.route("/name_selected", methods=["POST"])
def name_selected():
    button = request.form.get("total_or_pay")
    if "Pay" in button:
        return redirect(url_for("pay"), code=307)
    else:
        return redirect(url_for("mileage_logged"), code=307)


@app.route("/total", methods=["GET", "POST"])
def total():

    name_selected=request.form.get("name")
    #print(name_selected)


    user_id = current_user.__getattr__(name="id")
    name = current_user.username
    owner = mileage_craic.models.get_json_data("owner")

    total_distance = 0
    total_cost = 0
    filtered_journeys = []
    names = []
    users = []

    if name == owner:
        # get list of all names to put onto name select drop down so that the owner can see what everyone owes.
        names = []
        users = User.query.all()
        for this_user in users:
            names.append(this_user.username.title())

        if not name_selected:
            voyages = Voyage.query.all()

        else:
            #case insensitive search
            user = User.query.filter(func.lower(User.username) == func.lower(name_selected)).first()
            user_id = user.id
            voyages = db.session.query(Voyage).filter(Voyage.user_id == user_id).all()

    else:
        voyages = db.session.query(Voyage).filter(Voyage.user_id == user_id).all()
    for voyage in voyages:
        filtered_journeys.append(
            [voyage.date_posted, voyage.author.username, voyage.voyage_type, voyage.passengers, voyage.distance,
             voyage.cost, voyage.weather_text])
        total_distance += float(voyage.distance)
        total_cost += round(float(voyage.cost), 3)

    total_cost = "{:.2f}".format(total_cost)
    return render_template("total.html", mydate=date, filtered_journeys=filtered_journeys,
                           total_distance=total_distance, total_cost=total_cost, voyages=voyages, owner=owner,
                           name=name, names=names, users=users)


@app.route("/mileage_logged", methods=["GET", "POST"])
def mileage_logged():
    user_id = current_user.__getattr__(name="id")
    name_selected=request.form.get("name")

    name = current_user.username
    owner = mileage_craic.models.get_json_data("owner")
    total_distance = 0
    total_cost = 0

    voyages = db.session.query(Voyage).filter(Voyage.user_id == user_id).all()
    filtered_journeys = []
    for voyage in voyages:
        filtered_journeys.append([voyage.date_posted, voyage.author.username, voyage.voyage_type, voyage.passengers, voyage.distance, voyage.cost, voyage.weather_text])
        total_distance += float(voyage.distance)
        total_cost += round(float(voyage.cost), 3)
    voyage = voyages[-1]

    filtered_journeys = [[voyage.date_posted, voyage.author.username, voyage.voyage_type, voyage.passengers, voyage.distance, voyage.cost, voyage.weather_text]]
    last_voyage = voyages[-1]
    logged_voyage = [voyage.date_posted, voyage.voyage_type, voyage.passengers, voyage.distance, voyage.cost, voyage.weather_text]
    total_cost = "{:.2f}".format(total_cost)
    #print(total_cost, filtered_journeys)
    return render_template("mileage_logged.html", mydate=date, filtered_journeys=filtered_journeys, total_distance=total_distance, total_cost=total_cost, voyages=voyages, owner=owner, name=name, logged_voyage=logged_voyage)


@app.route("/pay")
def pay():
    owner = mileage_craic.models.get_json_data("owner")

    user_id = current_user.id
    voyages = db.session.query(Voyage).filter(Voyage.user_id == user_id).all()



    total_cost = 0
    first_date = ""
    #I don't know how to put the calculation into a function, as this calculation returns three values
    if len(voyages) == 0:
        pass
    else:
        first_date = voyages[0].date_posted
        for voyage in voyages:
            total_cost += float(voyage.cost)

        total_cost = "{:.2f}".format(total_cost)

    return render_template("pay.html", total_cost=total_cost, number_of_journeys=len(voyages), first_date=first_date, owner=owner)


@app.route("/paid")
def paid():
    # Don't know if this is good practice. But it worked!
    user_id = current_user.id
    voyages = db.session.query(Voyage).filter(Voyage.user_id == user_id).all()
    for voyage in voyages:
        db.session.delete(voyage)
        db.session.commit()

    #TODO: clear debts from database
    #(equivalent of the now-removed "zero_csv()" function)

    return render_template("paid.html")

@app.route("/bye")
def bye():
    return render_template("bye.html")

@app.route("/response", methods=["GET", "POST"])
def response():
    name = current_user.__getattr__(name="username")

    form = ResponseForm()

    if 'text' in session:
        new_text = session['text']
        #session.pop('text', None)
        #do some computation with string here
        sorted_charachters = sorted(new_text)
        sorted_string = "".join(sorted_charachters)
        form.answer.data = sorted_string.title()

    if form.validate_on_submit():
        new_text = form.input_text.data
        session['text'] = new_text

        return redirect(url_for('response'))


    # TODO put this back
    image_file = url_for('static', filename='static/' + current_user.image_file)
    image_file = 'static/default.jpg'

    return render_template('response.html', title='Response',  image_file=image_file, name=name, form=form)


@app.route("/make_veg_list", methods=["GET", "POST"])
def make_veg_list():
    with open('mileage_craic/cost_per_mile.json', "r") as f:
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

    with open('mileage_craic/cost_per_mile.json', 'w') as f:
        json.dump(data, f, indent=4)
    import mileage_craic.veg_prices

    veg_list = mileage_craic.veg_prices.get_veg_list()
    return render_template("make_veg_list.html", veg_list=veg_list, our_veg=our_veg, debug=debug)

@app.route("/edit_prices", methods=["GET", "POST"])
def edit_prices():
    with open('mileage_craic/cost_per_mile.json', "r") as f:
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


    import mileage_craic.veg_prices

    veg_list = mileage_craic.veg_prices.get_veg_list()
    prices = []

    our_prices = mileage_craic.models.get_json_data("our_prices")


    for veg in our_veg:
        price_list = mileage_craic.veg_prices.get_unit_price(veg)

        price_list[3] = our_prices[our_veg.index(veg)]
        #print(price_list)

        if len(price_list)<3:

            #if type(price_list[3]) not in [int, float]:
            #    price_list[3] = "Please enter our price"

            debug=veg
            price_list[3] = ""

        #elif type(price_list[3]) != int:
        #    price_list[3] = "Please enter our price"
        prices.append(price_list)
        #our_prices.append(price_list[3])
    #print(our_prices)
    """
    data['our_prices'] = our_prices
    with open('mileage_craic/cost_per_mile.json', 'w') as f:
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


    with open('mileage_craic/cost_per_mile.json', "r") as f:
        data = json.load(f)


    with open('mileage_craic/cost_per_mile.json', 'w') as f:
        data['our_prices'] = updated_prices
        json.dump(data, f, indent=4)




    return redirect(url_for('edit_prices'), code=307)



@app.route('/user_rec', methods=["GET",'POST'])
def user_rec():
    return redirect(url_for('make_veg_list'), code=307)



@app.route("/numbers", methods=["GET", "POST"])
def numbers():
    name = current_user.__getattr__(name="username")

    form = ResponseForm()

    if 'number' in session:
        new_number = session['number']
        #deletes the number
        session.pop('number', None)
        #do some computation with number here
        calculation = new_number / 2
        form.answer.data = calculation



    if form.validate_on_submit():
        new_number = form.number.data
        #saves the number to a session
        session['number'] = new_number

        return redirect(url_for('numbers'))



    # TODO put this back
    image_file = url_for('static', filename='static/' + current_user.image_file)
    image_file = 'static/default.jpg'

    return render_template('numbers.html', title='Practice',  image_file=image_file, name=name, form=form)



