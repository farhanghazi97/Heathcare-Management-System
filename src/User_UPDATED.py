from abc import ABC , abstractmethod
from flask_login import UserMixin
from src.booking import *
from datetime import datetime
from src.UnauthorisedAccess import *
import time

class User(ABC , UserMixin):

    __id = -1

    def __init__(self, name, email, currentBookings, password):
        self._id = self._generate_id()
        self._name = name
        self._email = email
        self._currentBookings = []
        self._password = password

    def add_booking(self, booking):
        self._currentBookings.append(booking)

    def print_currBookings(self):
        for booking in self._currentBookings:
            print(booking)

    def get_username(self):
        return self._email

    def get_name(self):
        return self._name

    def get_bookings(self):
        return self._currentBookings

    def set_username(self , username):
        self._email = username

    def set_password(self , password):
        self._password = password

    def get_past_bookings(self):
        currDate = time.strftime("%Y-%m-%d")
        currTime = time.strftime("%H:%M")
        lst = []
        for b in self._currentBookings:
            print(self._currentBookings)
            if datetime.strptime(b.getDate(), '%Y-%m-%d') < datetime.strptime(currDate, '%Y-%m-%d'):
                lst.append(b)
            elif datetime.strptime(b.getDate(), '%Y-%m-%d') == datetime.strptime(currDate, '%Y-%m-%d'):
                if datetime.strptime(b.getTime(), '%H:%M') <= datetime.strptime(currTime, '%H:%M'):
                    lst.append(b)

        return lst

    def get_future_bookings(self):
        currDate = time.strftime("%Y-%m-%d")
        currTime = time.strftime("%H:%M")
        lst = []
        for b in self._currentBookings:
            if datetime.strptime(b._date, '%Y-%m-%d') > datetime.strptime(currDate, '%Y-%m-%d'):
                lst.append(b)
            elif datetime.strptime(b.getDate(), '%Y-%m-%d') == datetime.strptime(currDate, '%Y-%m-%d'):
                if datetime.strptime(b.getTime(), '%H:%M') > datetime.strptime(currTime, '%H:%M'):
                    lst.append(b)
        return lst

    @abstractmethod
    def can_view_appointments(self, other_user):
        pass

    # search in a user's list of bookings for a booking with the same time and date as the input parameters. If such a booking exists, true is returned. Otherwise false is returned.

    def search_bookings(self, time, date):
        counter = 0

        if len(self._currentBookings) == 0:
            return True
        else:
            for i in range (0, len(self._currentBookings)):
                if (str(time) == self._currentBookings[i]._time) and (str(date) == self._currentBookings[i]._date):
                    counter = counter + 1
            if (counter == 0):
                return True
            return False


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def _generate_id(self):
        User.__id += 1
        return User.__id

    def validate_password(self, password):
        return self._password == password

    @abstractmethod
    def is_provider(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class HealthCareProvider(User):

    def __init__(self, name, email, currentBookings, password, providerNum, profession, affiliated_centres):
        super().__init__(name, email, currentBookings, password)
        self._providerNum = providerNum
        self._profession = profession
        self._ratings = {}
        self._avg_rating = "not yet rated"
        self._HCCentres = affiliated_centres
        self._patients = []

    @property
    def get_profession(self):
        return self._profession

    @property
    def get_HCP_name(self):
        return self._name

    @property
    def get_HCP_email(self):
        return self._email

    def add_patient(self, patient_email):
        self._patients.append(patient_email)

    #whether or not a user is a patient of this particular provider
    def has_patient(self, patient_email):
        for patient in self._patients:
            if patient_email == patient:
                return True
        return False

    def get_past_bookings(self):
        return User.get_past_bookings(self)

    def get_future_bookings(self):
        return User.get_future_bookings(self)

    @property
    def get_aff_HCC_centers(self):
        return self._HCCentres

    @property
    def get_provider_num(self):
        return self._providerNum

    def get_ratings(self):
        return self._ratings

    def get_avg_rating(self):
        print(self._ratings)
        return self._avg_rating

    def set_rating(self, avg_rating):
        self._avg_rating = avg_rating

    def can_view_appointments(self, other_user):
        if not (other_user.get_username() == self._email):
            raise UnauthorisedAccess()
        else:
            return True

    def is_provider(self):
        return True

    def print_HCCs(self):
        print(self._email)
        for x in self._HCCentres:
            print(x)

    def add_HCCentre(self, centre_name):
        self._HCCentres.append(centre_name)

    def __str__(self):
        return "Current bookings"


class Patient(User):

    def __init__(self, name, email, currentBookings, password, medicareNo, pastBookings):
        super().__init__(name, email, currentBookings, password)
        self._medicareNo = medicareNo
        self._pastBookings = []


    @property
    def get_pastBookings(self):
        return self._pastBookings

    def get_past_bookings(self):
        return User.get_past_bookings(self)

    def get_future_bookings(self):
        return User.get_future_bookings(self)

    def can_view_appointments(self, other_user):
        if (not other_user.is_provider()) and other_user.get_username() != self._email:
            raise UnauthorisedAccess()
        elif other_user.is_provider() and not (other_user.has_patient(self._email)):
            raise UnauthorisedAccess()
        else:
            return True

    def is_provider(self):
        return False
    '''
    def add_booking(self, booking):
        self._currentBookings.append(booking)
    '''
    @property
    def get_patient_name(self):
        return self._name

    @property
    def get_patient_email(self):
        return self._email

    @property
    def get_patient_medicareNo(self):
        return self._medicareNo

    def __str__(self):
        return "Name: {}\nEmail: {}\nPassword: {}\nCurrent bookings: {}\nMedicare Number: {}\nPast bookings: {}\n".format(self._name, self._email, self._password , self._currentBookings , self._medicareNo , self._pastBookings)
