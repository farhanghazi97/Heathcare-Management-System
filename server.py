from flask import Flask
from flask_login import LoginManager
from src.AuthenticationManager import AuthenticationManager
from src.UserManager_UPDATED import UserManager
from src.CentreManager import CentreManager
from src.HealthCareSystem import HealthCareSystem
from src.client import bootstrap_system
from src.BookingManager import bookingManager

app = Flask(__name__)
app.secret_key = 'very-secret-123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

auth_manager = AuthenticationManager(login_manager)
user_manager = UserManager.load_data()
booking_manager = bookingManager.load_data()
centre_manager = CentreManager.load_data()

if len(user_manager._patients) == 0:
    system = bootstrap_system(user_manager, centre_manager, booking_manager, auth_manager)
else:
    system = HealthCareSystem(user_manager , centre_manager , booking_manager , auth_manager)

@login_manager.user_loader
def load_user(user_id):
    return system.get_user_by_id(user_id)
