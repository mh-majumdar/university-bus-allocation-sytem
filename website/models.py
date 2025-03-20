from .extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # One-to-one relationship with Profile
    profile = db.relationship('Profile', backref='user', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Personal Information
    fathers_name = db.Column(db.String(150))
    mothers_name = db.Column(db.String(150))
    date_of_birth = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    guardians_name = db.Column(db.String(150))
    guardians_phone = db.Column(db.String(20))
    hall_for_residence = db.Column(db.String(150))
    hall_for_roll = db.Column(db.String(150))
    blood_group = db.Column(db.String(10))
    religion = db.Column(db.String(50))
    nationality = db.Column(db.String(50))
    nid_number = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(20))
    
    # Present Address
    present_division = db.Column(db.String(100))
    present_district = db.Column(db.String(100))
    present_upazilla = db.Column(db.String(100))
    present_post_office = db.Column(db.String(100))
    present_village = db.Column(db.String(100))
    present_house_name = db.Column(db.String(100))
    present_house_no = db.Column(db.String(30))
    present_road_no = db.Column(db.String(30))
    
    # Permanent Address
    permanent_division = db.Column(db.String(100))
    permanent_district = db.Column(db.String(100))
    permanent_upazilla = db.Column(db.String(100))
    permanent_post_office = db.Column(db.String(100))
    permanent_village = db.Column(db.String(100))
    permanent_house_name = db.Column(db.String(100))
    permanent_house_no = db.Column(db.String(30))
    permanent_road_no = db.Column(db.String(30))
    
    # Academic Information
    academic_level = db.Column(db.String(50))
    faculty = db.Column(db.String(150))
    department = db.Column(db.String(150))
    session = db.Column(db.String(20))
    year_term = db.Column(db.String(30))
    student_id = db.Column(db.String(20))
    
    # Timestamp
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())


class CampusBusBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    # Booking details
    departure_time = db.Column(db.String(10), nullable=False)  # Format: "8:00 AM", "9:30 AM", etc.
    destination = db.Column(db.String(100), nullable=False)    # Destination stop location
    
    # Timestamps
    booking_time = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # Status information
    status = db.Column(db.String(20), default="Confirmed")     # Confirmed, Cancelled, Completed
    
    # Relationship with User model
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    
    # def __repr__(self):
    #     return f"<CampusBusBooking {self.id}: {self.user.username} - {self.departure_time} to {self.destination}>"

class MaijdeeBusBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    # Booking details
    departure_time = db.Column(db.String(10), nullable=False)  # Format: "8:00 AM", "9:30 AM", etc.
    destination = db.Column(db.String(100), nullable=False)    # Destination stop location
    
    # Timestamps
    booking_time = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # Status information
    status = db.Column(db.String(20), default="Confirmed")     # Confirmed, Cancelled, Completed
    
    # Relationship with User model
    user = db.relationship('User', backref=db.backref('maijdee_bookings', lazy=True))
    
    # def __repr__(self):
    #     return f"<CampusBusBooking {self.id}: {self.user.username} - {self.departure_time} to {self.destination}>"