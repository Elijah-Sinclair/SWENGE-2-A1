from App.database import db
from App.models import User

class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    def