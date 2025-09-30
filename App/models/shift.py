from datetime import datetime, date, time
from App.database import db
from sqlalchemy.orm import validates 

class Shift(db.Model):
    __tablename__ = 'shifts'

    id              = db.Column(db.Integer, primary_key=True)
    staff_id        = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date            = db.Column(db.Date, nullable=False)
    start_time      = db.Column(db.Time, nullable=False)
    end_time        = db.Column(db.Time, nullable=False)
    clock_in_at     = db.Column(db.DateTime, nullable=True)
    clock_out_at    = db.Column(db.DateTime, nullable=True)

    staff        = db.relationship('User', back_populates='shifts')

    def __init__(self, staff_id, date, start_time, end_time):
        self.staff_id = staff_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f'<Shift {self.id} for {self.staff.username} on {self.date}>'
    
    @validates('end_time')
    def validate_times(self, key, end_time):
        if hasattr(self, 'start_time') and end_time <= self.start_time:
            raise ValueError('end_time must be after start_time')
        return end_time

    @validates('date')
    def validate_date(self, key, value):
        """Validate date is not in the past"""
        # key = 'date'
        if value < date.today():
            raise ValueError('Shift date cannot be in the past')
        return value

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
    def status(self):
        if not self.clock_in_at:
            return 'scheduled'
        elif self.clock_in_at and not self.clock_out_at:
            return 'in_progress'
        else:
            return 'completed'

    @property
    def duration(self):
        if not (self.clock_in_at and self.clock_out_at):
            return None
        return self.clock_out_at - self.clock_in_at
    
    @property
    def scheduled_duration(self):
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = datetime.combine(self.date, self.end_time)
        return (end_dt - start_dt).total_seconds() / 3600
    
    @property
    def actual_duration_hours(self):
        if not self.duration:
            return 0.0
        return round(self.duration.total_seconds() / 3600, 2)

    def overlaps(self, other: 'Shift') -> bool:
        if self.date != other.date:
            return False
        return not (self.end_time <= other.start_time or
                    self.start_time >= other.end_time)
    
    def get_json(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'staff_username': self.staff.username,
            'date': self.date.isoformat(),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'clock_in_at': self.clock_in_at.isoformat() if self.clock_in_at else None,
            'clock_out_at': self.clock_out_at.isoformat() if self.clock_out_at else None,
            'status': self.status,
            'scheduled_duration_hours': self.scheduled_duration,
            'actual_duration_hours': self.actual_duration_hours,
            'is_started': self.is_started,
            'is_completed': self.is_completed
        }