from App.database import db
from App.models.user import User
from App.models.shift import Shift
from datetime import date

class Staff(User):
    __mapper_args__ = {'polymorphic_identity': 'staff'}

    def get_current_shift(self):
        today = date.today()
        return Shift.query.filter(
            Shift.staff_id == self.id,
            Shift.date == today,
            Shift.clock_out_at.is_(None)
        ).first()

    def clock_in(self):
        shift = self.get_current_shift()
        if not shift:
            raise ValueError('No scheduled shift found for today')
        if shift.clock_in_at:
            raise RuntimeError('Already clocked in')
        
        shift.start()
        db.session.commit()
        return f'Clocked in at {shift.clock_in_at}'

    def clock_out(self):
        shift = self.get_current_shift()
        if not shift or not shift.clock_in_at:
            raise RuntimeError('Not clocked in')
        
        shift.end()
        db.session.commit()
        return f'Clocked out at {shift.clock_out_at}. Duration: {shift.actual_duration_hours} hours'

    def view_roster(self, week_start, week_end):
        return Shift.query.filter(
            Shift.staff_id == self.id,
            Shift.date.between(week_start, week_end)
        ).order_by(Shift.date, Shift.start_time).all()