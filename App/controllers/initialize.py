from .user import create_user
from App.database import db
from App.models.staff import Staff
from App.models.admin import Admin


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

    admin = Admin(username='admin', password='adminpass')
    db.session.add(admin)

    staff = Staff(username='staff1', password='staffpass')
    db.session.add(staff)

    staff = Staff(username='staff2', password='staffpass')
    db.session.add(staff)

    staff = Staff(username='staff3', password='staffpass')
    db.session.add(staff)
