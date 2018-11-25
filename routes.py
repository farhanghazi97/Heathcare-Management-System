from flask import render_template, request, redirect, url_for, abort , session
from flask_login import login_required, current_user
from src.CentreManager import CentreManager
from src.UserManager_UPDATED import UserManager
from src.booking import *
from src.User_UPDATED import *
from src.HealthCareCentre import *
from server import app, auth_manager, system
from src.HealthCareSystem import *
from src.booking_exceptions import *
from datetime import datetime, timedelta
from src.UnauthorisedAccess import *
import pickle

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
      return render_template("patient_login.html")
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if system.login_registered_user(username , password, 'patient'):
            return render_template("home.html")
        return render_template("patient_login.html")
    else:
        redir = request.args.get('next')
        return redirect(redir or url_for('patient_login'))

@app.route("/hcp_login" , methods = ['GET' , 'POST'])
def hcp_login():
    if request.method == 'GET':
      return render_template("hcp_login.html")
    if request.method == 'POST':
        username = request.form.get("hcp_username")
        password = request.form.get("hcp_password")
        if system.login_registered_user(username , password, 'hcp'):
            if current_user.is_provider() == True:
                return render_template("home.html")
            elif current_user.is_provider() == False:
                return render_template("hcp_login.html")
        return render_template("hcp_login.html")
    else:
        redir = request.args.get('next')
        return redirect(redir or url_for('hcp_login'))

@app.route('/logout')
@login_required
def logout():

    system._UserManager.save_data()
    system._CentreManager.save_data()
    system._BookingManager.save_data()

    auth_manager.logout()
    return redirect(url_for('login'))

@app.route("/home_page" , methods = ['POST' , 'GET'])
@login_required
def home_page():

    if(request.method == 'GET'):

        return render_template("home.html")

@app.route('/my_profile' , methods = ['GET' , 'POST'])
@login_required
def my_profile():

    if (request.method == "GET"):
        UM = system.get_UserManager()
        patients_list = UM.get_patients()
        doctors_list = UM.get_HCPs()
        return render_template("my_profile.html")

@app.route("/update_profile" , methods = ['GET' , 'POST'])
@login_required
def update_patient():
    if request.method == 'GET':
        return render_template("update_user_info.html")
    if request.method == 'POST':
        new_username = request.form.get("new_username")
        new_password = request.form.get("new_password")
        current_user.set_username(new_username)
        current_user.set_password(new_password)
        return render_template("my_profile.html")

@app.route("/patient/<username>/current_bookings" , methods = ['GET' , 'POST'])
@login_required
def current_patient_appointments(username):
    UM = system.get_UserManager()
    patient_username = username
    patient = UM.get_patient(str(patient_username))
    try:
        patient.can_view_appointments(current_user)
    except UnauthorisedAccess as error:
        message = error.get_message()
        return render_template("UnauthorisedAccess.html", error = message)
    #bookings = current_user.get_bookings()
    past_bookings = patient.get_past_bookings()
    future_bookings = patient.get_future_bookings()
    return render_template("current_patient_bookings.html", past_bookings = past_bookings, future_bookings=future_bookings, patient_username = patient_username)

@app.route("/provider/<username>/current_bookings", methods = ['GET', 'POST'])
@login_required
def current_provider_appointments(username):
    UM = system.get_UserManager()
    provider_username = username
    provider = UM.get_HCP(provider_username)
    try:
        provider.can_view_appointments(current_user)
    except UnauthorisedAccess as error:
        message = error.get_message()
        return render_template("UnauthorisedAccess.html", error = message)
    past_bookings = current_user.get_past_bookings()
    future_bookings = current_user.get_future_bookings()
    return render_template("current_provider_bookings.html", past_bookings = past_bookings, future_bookings=future_bookings)

@app.route("/patient/<username>", methods = ["GET", "POST"])
@login_required
def patientProfile(username):
    patient_email = username
    user = current_user

    #check = current_user.has_patient(patient_email)
    #print(check)
    return render_template("patient_profile.html", patient_email=patient_email, user = user)

@app.route("/centers/<HCCname>", methods = ["GET", "POST"])
@login_required
def centerProfile(HCCname):
    CM = system.get_CentreManager()
    HCC = CM.getHCCbyUsername(HCCname)
    ratings = system.get_ratings()
    if not HCC:
        abort(404)

    if request.method == "POST":
        rating = int(request.form['rating'])
        user = current_user
        system.calculate_rating(user, HCC, rating)
        print(rating)

    return render_template('HCC_profile.html', HCC=HCC, ratings = ratings, current_user = current_user)

@app.route("/doctors/<HCPusername>", methods = ["GET", "POST"])
@login_required
def HCPProfile(HCPusername):
    UM = system.get_UserManager()
    ratings = system.get_ratings()
    HCP = UM.get_HCP(HCPusername)
    if not HCP:
        abort(404)

    if request.method == "POST":
        rating = int(request.form['rating'])
        user = current_user
        system.calculate_rating(user, HCP, rating)

    return render_template('HCP_profile.html', HCP = HCP, ratings=ratings, current_user = current_user)

@app.route("/book/<HCPusername>/<location>", methods = ["GET", "POST"])
@login_required
def book(HCPusername,location):
    UM = system.get_UserManager()
    HCP = UM.get_HCP(HCPusername)
    BM = system.get_BookingManager()

    if not HCP:
        abort(404)

    if request.method == "GET":
        return render_template("booking.html")
    elif request.method == "POST":
        selected_date = request.form.getlist('form')[0]
        showtime = True
        time_intervals = BM.get_available_times(HCP._email, selected_date)
    try:
        BM.test_booking_conditions("", selected_date, HCP._email, current_user._email, location)
    except BookingError as e:
        return render_template("booking.html", msg = e._error_message)
    else:
        return render_template("booking.html", date = selected_date, showtime = showtime, time_intervals = time_intervals, HCPusername = HCPusername, location = location)

@app.route("/provider/notes/<bookingId>", methods = ["GET", "POST"])
@login_required
def providersNotes(bookingId):
    BM = system.get_BookingManager()
    UM = system.get_UserManager()
    booking = BM.booking_query(int(bookingId))
    HCP_username = booking.getHCP()
    HCP = UM.get_HCP(HCP_username)
    if request.method == "POST":
        try:
            booking.can_add_dNote(current_user.get_username())
        except UnauthorisedAccess as error:
            message = error.get_message()
            return render_template("UnauthorisedAccess.html", error = message)
        dNote = request.form['dNote']
        booking.setdNote(dNote)
        past_bookings = current_user.get_past_bookings()
        future_bookings = current_user.get_future_bookings()
        return render_template("current_provider_bookings.html", past_bookings=past_bookings, future_bookings=future_bookings)

    return render_template("doctor_note.html")


@app.route("/notes/<HCPusername>/<location>/<time>/<date>", methods = ["GET", "POST"])
@login_required
def add_a_note(HCPusername, location, time, date):
    BM = system.get_BookingManager()
    UM = system.get_UserManager()

    if request.method == 'GET':
        HCP = UM.get_HCP(HCPusername)
        return render_template("patient_note.html")

    if request.method == 'POST':
        HCC = location
        HCP = UM.get_HCP(HCPusername)
        time = time
        pNote = request.form['pNote']
        patient = current_user

        if 'confirm' in request.form:
            try:
                new_booking = BM.createBooking(time, date, HCP._email, current_user._email, location, current_user)
            except BookingError as e:
                return render_template("booking_error.html", msg = e._error_message)
            else:
                BM.append_to_user(new_booking, HCP, patient)
                BM.print_bookings_list()
            return render_template('confirmation.html', booking = new_booking)
        elif 'cancel' in request.form:
            return render_template('cancel_booking.html')
        return render_template("patient_note.html")


@app.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    #services = ["GP", "Physio", "chiro"]
    services = system.get_services()
    CM = system.get_CentreManager()
    UM = system.get_UserManager()
    if request.method == 'POST':
        search_type = request.form['action']
        user_input = request.form[search_type]
        search_results = system.search(search_type, user_input)
        #for x in search_results:
        #    print(x)
        return render_template('search_results.html', search_type = search_type, search_results = search_results)

    return render_template('search.html', services = services)
