from src.booking import *
from datetime import datetime
from src.User_UPDATED import *
from src.UserManager_UPDATED import *
from src.booking_exceptions import *
from flask_login import login_required, current_user

class bookingManager(object):
    def __init__(self):
        self._bookings = []

    # booking function that tries to raise BookingError
    def createBooking(self, time, date, HCP, patient, HCC, current_user, pNote = "", dNote = ""):

        curr_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"),'%Y-%m-%d')
        curr_time = datetime.strptime(datetime.now().strftime("%H:%M"),'%H:%M')

        if date == "":
            raise BookingError("date", "Please select a valid date")
        if datetime.strptime(date, '%Y-%m-%d') < curr_date:
            raise BookingError("date", "Please select a date that is not in the past")
        if time == "" and date != "":
            raise BookingError("time", "Please select a valid time")
        if time != "" and date != "":
            if datetime.strptime(date, '%Y-%m-%d') == curr_date and datetime.strptime(time, '%H:%M') < curr_time:
                raise BookingError("both", "Please select a time and date that is not in the past")
        if current_user.is_provider() == True:
            raise BookingError("provider", "A provider is not allowed to make bookings. Please login as a patient to make bookings")
        if current_user.search_bookings(time, date) == False:
            raise BookingError("patient", "Sorry. You cannot book two appointments at the same time")
        if current_user._email == HCP:
            raise BookingError("provider", "Sorry. A provider is not able to make an appointment with themselves")
        if self.check_availablity(HCP, date, time) == False:
            raise BookingError("provider", "Sorry. The provider is booked at this time. Please select another time or a different provider")
        else:
            newBooking = booking(time, date, HCP, patient, HCC, pNote, dNote)
            self._bookings.append(newBooking)
            newBooking.setBookingID(len(self._bookings))
            return newBooking

    # for extra security in case the user is accessing the notes URL with parameters that are invalid (prevents the user from pressing 'confirm' booking)
    def test_booking_conditions(self, time, date, HCP, patient, HCC, pNote = "", dNote = ""):

        curr_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"),'%Y-%m-%d')
        curr_time = datetime.strptime(datetime.now().strftime("%H:%M"),'%H:%M')

        if date == "":
            raise BookingError("date", "Please select a valid date")
        if datetime.strptime(date, '%Y-%m-%d') < curr_date:
            raise BookingError("date", "Please select a date that is not in the past")
        if time != "" and date != "":
            if datetime.strptime(date, '%Y-%m-%d') == curr_date and datetime.strptime(time, '%H:%M') < curr_time:
                raise BookingError("both", "Please select a time and date that is not in the past")
        if current_user.is_provider() == True:
            raise BookingError("provider", "A provider is not allowed to make bookings")
        if current_user.search_bookings(time, date) == False:
            raise BookingError("patient", "Sorry. You cannot book two appointments at the same time")
        if current_user._email == HCP:
            raise BookingError("provider", "Sorry. A provider is not able to make an appointment with themselves")
        if self.check_availablity(HCP, date, time) == False:
            raise BookingError("provider", "Sorry. The provider is booked at this time. Please select another time or a different provider")



    def print_bookings_list(self):
        for booking in self._bookings:
            print(booking)

    def booking_query(self, bookingId):
        for bookings in self._bookings:
            ID = booking.getBookingID(bookings)
            if ID == bookingId:
                return bookings


    # checks if the booking time is available or not. returns true if the time is not booked and false otherwise
    def check_availablity(self, HCP, date, time):
        counter = 0

        if len(self._bookings) == 0:
            return True
        else:
            for i in range (0, len(self._bookings)):
                if (str(time) == self._bookings[i]._time) and (str(date) == self._bookings[i]._date) and (str(HCP) == self._bookings[i]._HCP):
                    counter = counter + 1
            if (counter == 0):
                return True
            return False

    # gets the available times of a HCP (i.e. times in which the HCP does not have an existing booking at any HCC)
    def get_available_times(self, HCP, date):
        if date != "":
            curr_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"),'%Y-%m-%d')
        curr_time = datetime.strptime(datetime.now().strftime("%H:%M"),'%H:%M')
        all_times = ['0:00', '0:30', '1:00','1:30','2:00','2:30','3:00','3:30','4:00','4:30','5:00','5:30','6:00','6:30','7:00', '7:30', '8:00','8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '12:00','12:30', '13:00', '13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30', '18:00', '18:30', '19:00', '19:30','20:00','20:30', '21:00','21:30','22:00','22:30','23:00','23:30']
        available_times = []
        final_times = []
        for time in all_times:
            available = self.check_availablity(HCP, date, time)
            if available == True:
                available_times.append(time)

        for time in available_times:
            if date != "":
                if datetime.strptime(date, '%Y-%m-%d') == curr_date:
                    if curr_time <= datetime.strptime(time, '%H:%M'):
                        final_times.append(time)
                else:
                    final_times = list(available_times)

        return final_times

    # appends a booking to the HCP and the patient
    def append_to_user(self, booking, HCP, patient):
        HCP.add_booking(booking)
        patient_email = patient.get_username()
        HCP.add_patient(patient_email)
        patient.add_booking(booking)

    # returns a list of times in which a HCP is booked
    def get_times(self, HCP):
        list = []
        for appointment in HCP._currentBookings:
            list.append(appointment._time)
        return list


    def add_booking(self, booking):
        self._bookings.append(booking)

    def save_data(self):
        with open('booking_manager.dat', 'wb') as file:
            pickle.dump(self, file)
        file.close()

    @classmethod
    def load_data(cls):
        try:
            with open('booking_manager.dat', 'rb') as file:
                booking_manager = pickle.load(file)
        except FileNotFoundError:
            booking_manager = bookingManager()
        return booking_manager
