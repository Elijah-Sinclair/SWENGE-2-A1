from App.database import db
from App.models import User
from App.models import Shift

class Staff (User):
    __mapper_args__ = {'polymorphic_identity': 'staff'}

    def clock_in(self, shift_id):
        shift = Shift.query.get(shift_id)
        if shift.staff_id != self.id:
            raise PermissionError('Cannot clock in on another user’s shift')
        shift.start()
        db.session.commit()

    def clock_out(self, shift_id):
        shift = Shift.query.get(shift_id)
        if shift.staff_id != self.id:
            raise PermissionError('Cannot clock out on another user’s shift')
        shift.end()
        db.session.commit()

    def check_roster(self, week_start: date, week_end: date):
        return Shift.query.\
            filter(Shift.date.between(week_start, week_end)).\
            order_by(Shift.date, Shift.start_time).\
            all()

