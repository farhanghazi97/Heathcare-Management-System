from src.booking import *
from datetime import datetime, timedelta
from src.User_UPDATED import *
from src.booking_exceptions import *
from src.BookingManager import bookingManager
from flask_login import login_required, current_user
from server import system

#*** SECTION 1: INPUT TESTS *** #

#1.1 test valid input works
def test_valid_date():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    date = "2019-10-10"
    time = "9:30"
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    try:
        booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
        assert(True)
    except BookingError as e:
        assert(e is not defined)

#1.2 Test the date is not in the past
def test_invalid_date():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    date = "2016-10-10"
    time = "9:30"
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    try:
        booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
        assert(False)
    except BookingError as e: 
        assert(e._error_message == "Please select a date that is not in the past")

#1.3 Test empty date
def test_empty_date():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    date = ""
    time = "9:30"
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    try:
        booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
        assert(False)
    except BookingError as e: 
        assert(e._error_message == "Please select a valid date")
        
#1.4 Test empty time
def test_empty_time():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    date = "2019-10-10"
    time = ""
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    try:
        booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
        assert(False)
    except BookingError as e: 
        assert(e._error_message == "Please select a valid time")

#1.5 Test date and time (test that the date and time is not in the past) 
def test_date_and_time():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    date = datetime.now().strftime("%Y-%m-%d")
    print(date)
    future_time = datetime.now() - timedelta(minutes = 30)
    time = future_time.strftime('%H:%M')
    print(time)
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    try:
        booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
        assert(False)
    except BookingError as e: 
        print(e._error_message)
        assert(e._error_message == "Please select a time and date that is not in the past")

#*** SECTION 1 INPUT TESTING COMPLETE ***#

#*** SECTION 2: MULTIPLE BOOKING RESTRICTION TESTING ***#

#2.1 Test a patient cannot have multiple bookings at different times
def test_patient_multiple_booking_different_times():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    date = "2019-10-10"
    time = "9:30"
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    time2 = "10:30"
    try:
        booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
        BM.append_to_user(booking, HCP, patient)
        booking2 = BM.createBooking(time2, date, HCP._email, patient._email, HCC, patient)
        assert(True)
    except BookingError as e:
        assert(e is not defined)

#2.2 Test a patient cannot have two bookings at the same time
def test_patient_multiple_booking_same_time():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    booking1 = BM.createBooking("15:30", "2019-11-10", HCP._email, patient._email, HCC, patient)
    BM.append_to_user(booking1, HCP, patient)

    try:
        booking = BM.createBooking("15:30", "2019-11-10", HCP._email, patient._email, HCC, patient)
        assert(False)
    except BookingError as e:
        assert(e._error_message == "Sorry. You cannot book two appointments at the same time")

#2.3 Test a provider can have multiple bookings at different times
def test_provider_multiple_booking_different_time():
    UM = system.get_UserManager()
    patient = UM.get_patient("jack@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    booking1 = BM.createBooking("16:00", "2019-02-10", HCP._email, patient._email, HCC, patient)
    BM.append_to_user(booking1, HCP, patient)

    try:
        booking = BM.createBooking("15:30", "2019-03-10", HCP._email, patient._email, HCC, patient)
        assert(True)
    except BookingError as e:
        assert(e is not defined)

#2.4 Test a provider cannot have multiple bookings at the same time
def test_provider_multiple_booking_same_time():
    UM = system.get_UserManager()
    patient1 = UM.get_patient("jack@gmail.com")
    patient2 = UM.get_patient("hao@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    booking1 = BM.createBooking("17:00", "2019-02-10", HCP._email, patient1._email, HCC, patient1)
    BM.append_to_user(booking1, HCP, patient1)
    for booking in BM._bookings:   
        print(booking._time)
        print(booking._date)

    try:
        booking = BM.createBooking("17:00", "2019-02-10", HCP._email, patient2._email, HCC, patient2)
        BM.append_to_user(booking, HCP, patient1)
        assert(False)
    except BookingError as e:
        assert(e._error_message == "Sorry. The provider is booked at this time. Please select another time or a different provider")
        
#*** SECTION 2 MULTIPLE BOOKING RESTRICTION TESTING COMPLETE ***#

#*** SECTION 3: USER RESTRICTION TESTING ***#
#3.1 Test that a provider cannot book an appointment if they are logged in as a provider
def test_provider_restriction():
    UM = system.get_UserManager()
    HCP = UM.get_HCP("toby@gmail.com")
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()

    try:
        booking = BM.createBooking("17:00", "2019-02-10", HCP._email, HCP._email, HCC, HCP)
        assert(False)
    except BookingError as e:
        assert(e._error_message == "A provider is not allowed to make bookings. Please login as a patient to make bookings")
        
#3.2 Test a provider is able to book an appointment with another provider if they are logged in as a patient 
def test_provider_can_book_as_patient():
    UM = system.get_UserManager()
    patient = UM.get_patient("toby@gmail.com")
    HCP = UM.get_HCP("anna@gmail.com")
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    
    try:
        booking = BM.createBooking("17:00", "2019-05-10", HCP._email, patient._email, HCC, patient)
        BM.append_to_user(booking, HCP, patient)
        assert(True)
    except BookingError as e:
        assert(e is not defined)

#3.3 Test a provider cannot book with themselves (if they have logged in as a patient) 
def test_provider_cannot_book_themselves():
    UM = system.get_UserManager()
    patient = UM.get_patient("toby@gmail.com")
    HCP = UM.get_HCP("toby@gmail.com")
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    
    try:
        booking = BM.createBooking("18:00", "2019-05-10", HCP._email, patient._email, HCC, patient)
        BM.append_to_user(booking, HCP, patient)
        assert(False)
    except BookingError as e:
        assert(e._error_message == "Sorry. A provider is not able to make an appointment with themselves")

# 3.4 Test that a provider cannot book an appointment as a patient at a time they have an appointment 
#NEED TO TEST A PROVIDER CANNOT MAKE A BOOKING AT A TIME IF THEY HAVE AN APPOINTMENT AS A DOCTOR AT THAT TIME - difficult to implement
#THEIR RESPONSIBILITY TO MAKE SURE THEY CAN'T BOOK AT THE SAME TIME
