from datetime import datetime
from App.database import db

class Shift(db.Model):
    __tablename__ = 'shifts'

    id      = db.Column(db.Integer, primary_key=True)
