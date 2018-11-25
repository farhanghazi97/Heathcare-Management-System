class BookingError(Exception):
    def __init__(self, invalid_field, msg):
        self._invalid_field = invalid_field
        self._error_message = msg


