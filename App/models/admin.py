from App.database import db
from App.models import User
from App.models.shift import Shift

class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    def create_shift(self, staff_id, start_time=None):
        