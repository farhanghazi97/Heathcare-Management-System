class HealthCareCentre:

    def __init__(self , suburb , name , phone, type , ABN):
        self._suburb = suburb
        self._name = name
        self._phone = phone
        self._type = type
        self._ABN = ABN
        self._HCPs = []
        self._ratings = {}
        self._avg_rating = "not yet rated"

    def get_HC_name(self):
        return self._name

    def get_suburb_name(self):
        return self._suburb
        
    def set_rating(self, avg_rating):
        self._avg_rating = avg_rating

    def get_phone(self):
        return self._phone

    def get_type(self):
        return self._type
        
    def get_ratings(self):
        return self._ratings

    def get_avg_rating(self):
        return self._avg_rating

    def add_HCP(self, username):
        self._HCPs.append(username)
        
    def get_ABN(self):
        return self._ABN
        
    def print_HCPs(self):
        print(self._name)
        for x in self._HCPs:
            print(x)
    
    def get_HCPs(self):
        return self._HCPs

    def __str__(self):
        return "\nName: {}\nSuburb: {} \nPhone: {}\nType: {}\nABN: {}".format(self._name , self._suburb , self._phone , self._type , self._ABN)

#HC = HealthCareCentre("randwick", "RPA", "000", "hospital", "123")
#print(HC)
