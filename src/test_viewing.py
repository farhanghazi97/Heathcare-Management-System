from src.booking import *
from datetime import datetime, timedelta
from src.User_UPDATED import *
from src.UnauthorisedAccess import *
from src.BookingManager import bookingManager
from flask_login import login_required, current_user
from server import system

    

def patient_appointments():
    
    UM = system.get_UserManager()
    patient = UM.get_patient('jack@gmail.com')
    HCP = UM.get_HCP('toby@gmail.com')
    date = "2019-10-15"
    time = "9:30"
    locations = HCP.get_aff_HCC_centers
    HCC = locations[0]
    BM = bookingManager()
    booking = BM.createBooking(time, date, HCP._email, patient._email, HCC, patient)
    unauthorised_HCP = UM.get_HCP('anna@gmail.com')
    
    #anna cannot access jack's appointments because jack is not her patient
    try:
        patient.can_view_appointments(unauthorised_HCP)
        assert(False)
    except UnauthorisedAccess as error:
        assert(error.get_message() == "You are not authorised to access this page")
      
    #HCP toby should be able to access jacks list of past appointments
    try:
        patient.can_view_appointments(HCP)
    except UnauthorisedAccess as error:
        assert(False)
        
    #another patient cannot access jacks list of past appointments
    hao = UM.get_patient('hao@gmail.com') 
    try:
        patient.can_view_appointments(hao)
        assert(False)
    except UnauthorisedAccess as error:
        assert(error.get_message() == "You are not authorised to access this page")
    
def test_unauthorised_provider_note():
    # anna cannot make add any notes to do with the appointment between jack and toby
    
    UM = system.get_UserManager()
    patient = UM.get_patient('jack@gmail.com')
    HCP1 = UM.get_HCP('toby@gmail.com')
    dateA = "2019-10-15"
    timeA = "9:30"
    locations = HCP1.get_aff_HCC_centers
    HCC_A = locations[0]
    BM = bookingManager()
    booking1 = BM.createBooking(timeA, dateA, HCP1._email, patient._email, HCC_A, patient)
    
    HCP2 = UM.get_HCP('anna@gmail.com')
    dateB = '2019-10-16'
    timeB = '9:30'
    locations = HCP2.get_aff_HCC_centers
    HCC_B = locations[0]
    booking2 = BM.createBooking(timeB, dateB, HCP2._email, patient._email,
    HCC_B, patient)
    
    try:
        booking1.can_add_dNote('anna@gmail.com')
        assert(False)
    except UnauthorisedAccess as error:
        assert(error.get_message() == "You are not authorised to access this page")
        
    #toby is authorised to add a note
    try:
        booking1.can_add_dNote('toby@gmail.com')
    except UnauthorisedAccess as error:
        assert(False)
        
    #another patient cannot add a note
    try:
        booking1.can_add_dNote('hao@gmail.com')
        assert(False)
    except UnauthorisedAccess as error:
        assert(error.get_message() == "You are not authorised to access this page")
        
def provider_appointments():
    #no other user can access a providers appointments 
    UM = system.get_UserManager()
    HCP = UM.get_HCP('toby@gmail.com')
    try:
        HCP.can_view_appointments('jack@gmail.com')
        assert(False)
    except UnauthorisedAccess as error:
        assert(error.get_message() == "You are not authorised to access this page")
      
    #another provider cannot access toby's list of appointments
    try:
        HCP.can_view_appointments('ian@gmail.com')
    except UnauthorisedAccess as error:
        assert(error.get_message() == "You are not authorised to access this page")
       
    #toby is able to view his appointments
    try:
        HCP.can_view_appointments('toby@gmail.com')
    except UnauthorisedAccess as error:
        assert(False)
    
    
    
    
    
    
    
    
    
