from datetime import datetime
from App.database import db

class Shift(db.Model):
    __tablename__ = 'shifts'

    id      = db.Column(db.Integer, primary_key=True)
    staff_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date         = db.Column(db.Date, nullable=False)
    start_time   = db.Column(db.Time, nullable=False)
    end_time     = db.Column(db.Time, nullable=False)
    clock_in_at  = db.Column(db.DateTime, nullable=True)
    clock_out_at = db.Column(db.DateTime, nullable=True)

    staff        = db.relationship('User', back_populates='shifts')

    def __repr__(self):
        return f'<Shift {self.id} for {self.staff.username} on {self.date}>'
    
    @validates('end_time')
    def validate_times(self, key, end_time):
        if hasattr(self, 'start_time') and end_time <= self.start_time:
            raise ValueError('end_time must be after start_time')
        return end_time

    def start(self):
        if self.clock_in_at:
            raise RuntimeError('Shift already started')
        self.clock_in_at = datetime.now()

    def end(self):
        if not self.clock_in_at:
            raise RuntimeError('Shift not started yet')
        if self.clock_out_at:
            raise RuntimeError('Shift already completed')
        self.clock_out_at = datetime.now()

    @property
    def is_started(self) -> bool:
        return self.clock_in_at is not None

    @property
    def is_completed(self) -> bool:
        return self.clock_out_at is not None

    @property
    def duration(self):
        if not (self.clock_in_at and self.clock_out_at):
            return None
        return self.clock_out_at - self.clock_in_at

    def overlaps(self, other: 'Shift') -> bool:
        if self.date != other.date:
            return False
        return not (self.end_time <= other.start_time or
                    self.start_time >= other.end_time)
