from src.HealthCareSystem import *
from src.UserManager_UPDATED import UserManager
from src.User_UPDATED import *
from src.HealthCareCentre import *
from src.AuthenticationManager import AuthenticationManager

import csv

def bootstrap_system(user_manager, centre_manager, booking_manager,
                     auth_manager):

    system = HealthCareSystem(user_manager, centre_manager, booking_manager, auth_manager)

    print("Here yeah")

    with open('src/patient.csv') as f:
        reader = csv.DictReader(f)
        COLUMNS = [
        'patient_email'
        'password'
        ]

        for row in reader:
            patient = Patient("name", row['patient_email'], [], row['password'], 0, [])
            user_manager.add_patient(patient)


    with open('src/provider.csv') as f:
        reader = csv.DictReader(f)
        COLUMNS = [
        'provider_email'
        'provider_type'
        'password'
        ]

        for row in reader:
            HCP = HealthCareProvider("name", row['provider_email'], [], row['password'], 0 , row['provider_type'], [])
            HCP_patient = Patient("name", row['provider_email'], [], row['password'], 0, [])
            system.add_service(row['provider_type'])
            user_manager.add_HCP(HCP)
            user_manager.add_patient(HCP_patient)




    with open('src/health_centres.csv') as f:
        reader = csv.DictReader(f)
        COLUMNS = [
        'centre_type',
        'abn',
        'name',
        'phone',
        'suburb',
        ]
        for row in reader:
        #print('Centre type {} ABN {} Name {}'.format(row['centre_type'], row['abn'], row['name']))
            HCC = HealthCareCentre(row['suburb'] , row['name'] , row['phone'] , row['centre_type'] , row['abn'])
            centre_manager.add_HCC(HCC)
            #print(h1)


    with open('src/provider_health_centre.csv') as f:
        reader = csv.DictReader(f)
        COLUMNS = [
        'provider_email',
        'health_centre_name',
        ]
        for row in reader:
            HCPs = user_manager.get_HCPs()
            HCCs = centre_manager.get_HCCs()
            for HCP in HCPs:
                if HCP._email == row['provider_email']:
                    HCP.add_HCCentre(row['health_centre_name'])
            for HCC in HCCs:
                if HCC._name == row['health_centre_name']:
                    provider = user_manager.get_HCP(row['provider_email'])
                    HCC.add_HCP(provider)
                    #HCC.add_HCP(row['provider_email'])
            # find the provider in the user manager
            # add the HCCname to the providers affiliated centres
            # find the centre in the centreManager
            # add the HCP to the centre

    past_booking = booking('12:00', '2017-10-14', 'toby@gmail.com', 'jack@gmail.com', 'Sydney Children Hospital')
    HCP = user_manager.get_HCP('toby@gmail.com')
    patient = user_manager.get_patient('jack@gmail.com')
    booking_manager.add_booking(past_booking)
    booking_manager.append_to_user(past_booking, HCP, patient)

    return system
