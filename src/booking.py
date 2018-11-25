from src.UnauthorisedAccess import *
class booking(object):
    def __init__(self, time, date, HCP, patient, HCC, pNote = "", dNote = ""):
        self._time = time
        self._date = date
        self._HCP = HCP
        self._patient = patient
        self._HCC = HCC
        self._pNote = pNote
        self._dNote = dNote
        self._bookingID = 0
    def __str__(self):
        return "time: {} date: {} provider: {} patient: {} HCC: {} patient's note: {} doctor's notes: {}".format(self._time, self._date, self._HCP, self._patient, self._HCC, self._pNote, self._dNote)
    
    def getPatient(self):
        return self._patient
        
        
    def getHCC(self):
        return self._HCC
    
    def getTime(self):
        return self._time

    def getDate(self):
        return self._date

    def getHCP(self):
        return self._HCP

    def setpNote(self, string):
        self._pNote = string
        
    def setBookingID(self, IDNum):
        self._bookingID = IDNum
        
    def getBookingID(self):
        return self._bookingID
        
    def can_add_dNote(self, other_user):
        if not (other_user == self._HCP):
            raise UnauthorisedAccess()
        else:
            return True

    def setdNote(self, string):
        self._dNote = string

    def getdNote(self):
        return self._dNote

    def getpNote(self):
        return self._pNote
