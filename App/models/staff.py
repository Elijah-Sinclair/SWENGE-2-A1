from App.database import db
from App.models import User
class Staff (User):

    
    __mapper_args__ = {'polymorphic_identity': 'staff'}

    def clock_in():

    def clock_out():

    def check_roster():

