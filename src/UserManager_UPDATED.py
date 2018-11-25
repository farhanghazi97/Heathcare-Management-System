import csv
from src.User_UPDATED import Patient, User, HealthCareProvider
from src.booking import *
import pickle

##

class UserManager:

    def __init__(self):
        self._HCPs = []
        self._patients = []

    def add_HCP(self, HCP):
        self._HCPs.append(HCP)

    def add_patient(self, patient):
        self._patients.append(patient)

    def get_HCPs(self):
        return self._HCPs

    def get_patients(self):
        return self._patients

    def get_HCP(self, username):
        for HCP in self._HCPs:
            HCP_email = HCP.get_username()
            if username == HCP_email:
                return HCP

    def get_patient(self, username):
        for p in self._patients:
            email = p._email
            if username == email:
                return p
            '''
            patient_email = patient.get_username()
            if username == patient_email:
                return patient
            '''



    #DEBUGGING
    def print_HCP_list(self):
        for x in self._HCPs:
            print(x)

    def print_patient_list(self):
        for x in self._patients:
            print(x)


    def searchbyHCP(self, name):
        return [i for i in self._HCPs if name.lower() in i._email.lower()]


    def searchbyService(self, service):
        return [i for i in self._HCPs
            if service.lower() in i._profession.lower()
            ]

    def save_data(self):
        with open('user_manager.dat', 'wb') as file:
            pickle.dump(self, file)
        file.close()

    @classmethod
    def load_data(cls):
        try:
            with open('user_manager.dat', 'rb') as file:
                user_manager = pickle.load(file)
        except FileNotFoundError:
            user_manager = UserManager()
        return user_manager
