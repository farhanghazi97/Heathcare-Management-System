from statistics import mean

class HealthCareSystem:

    def __init__(self, UserManager, CentreManager, BookingManager,
                 AuthenticationManager):
        #self._patients = []
        #self._HCPs = []
        self._BookingManager = BookingManager
        self._UserManager = UserManager
        self._CentreManager = CentreManager
        self._AuthenticationManager = AuthenticationManager
        self._Services = set([])
        self._ratings = [1,2,3,4,5]

    def get_UserManager(self):
        return self._UserManager
        
    def calculate_rating(self, user, subject, value):
        # a value is a number between 1-5 which a user assigned a subject as a rating
        # check if the user is in the subject's ratings
        rating_dict = subject.get_ratings()
        username = user.get_username()
        rating_dict[username] = value
        subject.set_rating(mean(rating_dict.values()))
        
    def get_ratings(self):
        return self._ratings

    def get_CentreManager(self):
        return self._CentreManager

    def get_BookingManager(self):
        return self._BookingManager
        
    def search(self, search_type, user_input):
        search_results = []
        if search_type == "suburb_search":
            search_results = self._CentreManager.searchbySuburb(user_input)
        elif search_type == "centre_search":
            search_results = self._CentreManager.searchbyHCC(user_input)
        elif search_type == "provider_search":
            search_results = self._UserManager.searchbyHCP(user_input)
        elif search_type == "service_search":
            search_results = self._UserManager.searchbyService(user_input)           
        return search_results
        
    def get_services(self):
        return self._Services

    def add_service(self, string):
        return self._Services.add(string)

    def add_patient(self , patient):
        self._patients.append(patient)

    def add_HCP(self , HCP):
        self._HCPs.append(HCP)

    def get_user_by_id(self, user_id):
        users = self._UserManager.get_patients() + self._UserManager.get_HCPs()
        for c in users:
            if c.get_id() == user_id:
                return c

    def login_registered_user(self, username , password, login_type):
        if login_type == 'patient':
            patients = self._UserManager.get_patients()
            for patient in patients:
                if self._AuthenticationManager.login(patient, username , password):
                    return True
            return False
        elif login_type == 'hcp':
            HCPs = self._UserManager.get_HCPs()
            for HCP in HCPs:
                if self._AuthenticationManager.login(HCP, username , password):
                    return True
            return False

    #def login_patient(self, username , password):
    #    for patient in self._patients:
    #        if self._AuthenticationManager.login(patient, username , password):
    #            return True
    #    return False

    #def login_HCP(self , username , password):
    #    for HCP in self._HCPs:
    #        if self._AuthenticationManager.login(HCP , username , password):
    #            return True
    #    return False

    #@property
    #def patients(self):
    #    return self._patients

    #@property
    #def HCPs(self):
    #    return self._HCPs
