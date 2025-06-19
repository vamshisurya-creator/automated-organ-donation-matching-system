import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from database import db

# Constants for organ types and blood groups
ORGAN_TYPES = ['Kidney', 'Liver', 'Heart', 'Lung', 'Pancreas', 'Intestine', 'Cornea']
BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
URGENCY_LEVELS = ['Low', 'Medium', 'High']
GENDER_TYPES = ['Male', 'Female', 'Other']

# Blood compatibility dictionary (recipient blood group: compatible donor blood groups)
BLOOD_COMPATIBILITY = {
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],  # Can receive from all
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+': ['O+', 'O-'],
    'O-': ['O-']  # Can only receive O-
}

class Donor(db.Model):
    """Donor model representing organ donors in the system"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    organ_type = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationship with Match model
    donations = db.relationship('Match', backref='donor', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Donor('{self.name}', '{self.organ_type}', '{self.blood_group}')"

class Recipient(db.Model):
    """Recipient model representing patients who need organ transplants"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    required_organ = db.Column(db.String(20), nullable=False)
    urgency = db.Column(db.String(10), nullable=False)  # Low, Medium, High
    contact = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationship with Match model
    matches = db.relationship('Match', backref='recipient', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Recipient('{self.name}', '{self.required_organ}', '{self.blood_group}', '{self.urgency}')"

class Match(db.Model):
    """Match model representing a potential match between donor and recipient"""
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'), nullable=False)
    match_score = db.Column(db.Float, nullable=False)  # Score based on compatibility factors
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    match_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"Match(Donor ID: {self.donor_id}, Recipient ID: {self.recipient_id}, Score: {self.match_score})"

class Admin(UserMixin, db.Model):
    """Admin user model for system administration"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"
