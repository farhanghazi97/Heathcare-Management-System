import csv
from src.UserManager_UPDATED import UserManager
from src. User_UPDATED import *

def get_patients():
    
    patients = []
    with open('src/patient_UPDATED.csv') as f:
        reader = csv.DictReader(f)
        COLUMNS = [
            'patient_email'
            'password'
        ]
        
        for row in reader:
            patient = Patient("name", row['patient_email'], [], row['password'], 0, [])
            user_manager.add_patient(Patient)
    
    return patients

