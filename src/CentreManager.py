import csv
from src.HealthCareCentre import *
import pickle

class CentreManager:

    def __init__(self):
        self._HCCs = []
        self._Suburbs = []

    def add_HCC(self, HCC):
        self._HCCs.append(HCC)

    def print_list(self):
        for x in self._HCCs:
            print(x)

    def get_HCCs(self):
        return self._HCCs

    def getHCCbyUsername(self, name):
        for HCC in self._HCCs:
            if HCC._name == name:
                return HCC

    #SEARCH FUNCTION
    def searchbyHCC(self, string):
        return [i for i in self._HCCs
                if string.lower() in i._name.lower()]

    #SEARCH FUNCTION
    def searchbySuburb(self , string):

        return [i for i in self._HCCs
                if string.lower() in i._suburb.lower()]


    def save_data(self):
        with open('centre_manager.dat', 'wb') as file:
            pickle.dump(self, file)
        file.close()

    @classmethod
    def load_data(cls):
        try:
            with open('centre_manager.dat', 'rb') as file:
                centre_manager = pickle.load(file)
        except FileNotFoundError:
            centre_manager = CentreManager()
        return centre_manager
