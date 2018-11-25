class UnauthorisedAccess(Exception):
    def __init__(self):
        self._message = "You are not authorised to access this page"
        
    def get_message(self):
        return self._message
