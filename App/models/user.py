from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'users'

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), nullable=False, unique=True)
    password    = db.Column(db.String(256), nullable=False)
    role        = db.Column(db.String(50), nullable=False)
    shifts      = db.relationship('Shift', back_populates='staff', cascade='all, delete-orphan')   

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user',
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_staff_members(cls):
        return cls.query.filter_by(role='staff').all()

    @classmethod
    def get_admins(cls):
        return cls.query.filter_by(role='admin').all()

    def is_staff(self):
        return self.role == 'staff'

    def is_admin(self):
        return self.role == 'admin'