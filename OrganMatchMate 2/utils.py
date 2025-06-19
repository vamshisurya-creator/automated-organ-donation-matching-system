import logging
import random

from database import db
from models import BLOOD_COMPATIBILITY, Admin, Donor, Match, Recipient


def calculate_match_score(donor, recipient):
    """
    Calculate match score between donor and recipient based on various factors
    
    Parameters:
    - donor: Donor object
    - recipient: Recipient object
    
    Returns:
    - score: float between 0 and 100, or None if incompatible
    """
    # Check organ type match (must be the same)
    if donor.organ_type != recipient.required_organ:
        return None
    
    # Check blood compatibility
    if donor.blood_group not in BLOOD_COMPATIBILITY[recipient.blood_group]:
        return None
    
    # Calculate base score (out of 100)
    base_score = 70.0
    
    # Add points for exact blood type match
    if donor.blood_group == recipient.blood_group:
        base_score += 10.0
    
    # Add points for urgency
    if recipient.urgency == 'High':
        base_score += 15.0
    elif recipient.urgency == 'Medium':
        base_score += 7.5
    
    # Add points for age similarity (if within 10 years)
    if abs(donor.age - recipient.age) <= 10:
        base_score += 5.0
    
    return round(base_score, 2)

def generate_match_note(donor, recipient, score):
    """Generate a match note detailing why this match was made"""
    notes = [
        f"Organ type match: {donor.organ_type}",
        f"Blood compatibility: {donor.blood_group} -> {recipient.blood_group}"
    ]
    
    if donor.blood_group == recipient.blood_group:
        notes.append("Exact blood type match (+10 points)")
    
    if recipient.urgency == 'High':
        notes.append("High urgency case (+15 points)")
    elif recipient.urgency == 'Medium':
        notes.append("Medium urgency case (+7.5 points)")
    
    if abs(donor.age - recipient.age) <= 10:
        notes.append(f"Age similarity: Donor age {donor.age}, Recipient age {recipient.age} (+5 points)")
    
    notes.append(f"Total match score: {score}")
    
    return "\n".join(notes)

def generate_matches():
    """
    Generate matches between available donors and recipients
    Returns list of newly created Match objects
    """
    # Get all available donors and recipients
    available_donors = Donor.query.filter_by(availability=True).all()
    recipients = Recipient.query.all()
    
    new_matches = []
    
    # Check each donor against each recipient
    for donor in available_donors:
        for recipient in recipients:
            # Skip if already matched
            existing_match = Match.query.filter_by(donor_id=donor.id, recipient_id=recipient.id).first()
            if existing_match:
                continue
            
            match_score = calculate_match_score(donor, recipient)
            
            # If compatible, create a match
            if match_score is not None:
                match_note = generate_match_note(donor, recipient, match_score)
                new_match = Match(
                    donor_id=donor.id,
                    recipient_id=recipient.id,
                    match_score=match_score,
                    match_notes=match_note
                )
                db.session.add(new_match)
                new_matches.append(new_match)
    
    # Commit all new matches to database
    if new_matches:
        db.session.commit()
        logging.info(f"Generated {len(new_matches)} new matches")
    
    return new_matches

def populate_dummy_data():
    """Populate the database with dummy donor and recipient data for testing"""
    # Sample data for donors
    donors = [
        {
            'name': 'John Doe',
            'age': 35,
            'gender': 'Male',
            'blood_group': 'O+',
            'organ_type': 'Kidney',
            'contact': '555-123-4567',
            'availability': True
        },
        {
            'name': 'Jane Smith',
            'age': 42,
            'gender': 'Female',
            'blood_group': 'A-',
            'organ_type': 'Liver',
            'contact': '555-234-5678',
            'availability': True
        },
        {
            'name': 'Robert Johnson',
            'age': 28,
            'gender': 'Male',
            'blood_group': 'B+',
            'organ_type': 'Kidney',
            'contact': '555-345-6789',
            'availability': True
        },
        {
            'name': 'Sarah Williams',
            'age': 31,
            'gender': 'Female',
            'blood_group': 'AB+',
            'organ_type': 'Heart',
            'contact': '555-456-7890',
            'availability': True
        },
        {
            'name': 'Michael Brown',
            'age': 45,
            'gender': 'Male',
            'blood_group': 'O-',
            'organ_type': 'Lung',
            'contact': '555-567-8901',
            'availability': False
        }
    ]
    
    # Sample data for recipients
    recipients = [
        {
            'name': 'Emily Davis',
            'age': 29,
            'gender': 'Female',
            'blood_group': 'A+',
            'required_organ': 'Kidney',
            'urgency': 'High',
            'contact': '555-678-9012'
        },
        {
            'name': 'David Wilson',
            'age': 56,
            'gender': 'Male',
            'blood_group': 'AB+',
            'required_organ': 'Liver',
            'urgency': 'Medium',
            'contact': '555-789-0123'
        },
        {
            'name': 'Lisa Taylor',
            'age': 38,
            'gender': 'Female',
            'blood_group': 'B-',
            'required_organ': 'Kidney',
            'urgency': 'Low',
            'contact': '555-890-1234'
        },
        {
            'name': 'Thomas Martin',
            'age': 42,
            'gender': 'Male',
            'blood_group': 'O+',
            'required_organ': 'Heart',
            'urgency': 'High',
            'contact': '555-901-2345'
        },
        {
            'name': 'Olivia Anderson',
            'age': 24,
            'gender': 'Female',
            'blood_group': 'A-',
            'required_organ': 'Lung',
            'urgency': 'Medium',
            'contact': '555-012-3456'
        }
    ]
    
    # Add donors to database
    for donor_data in donors:
        donor = Donor(**donor_data)
        db.session.add(donor)
    
    # Add recipients to database
    for recipient_data in recipients:
        recipient = Recipient(**recipient_data)
        db.session.add(recipient)
    
    # Commit to database
    db.session.commit()
    
    # Create default admin user if it doesn't exist
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin',
            email='admin@example.com',
        )
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.commit()
        logging.info("Created default admin user")
    
    # Generate initial matches
    generate_matches()

def create_admin(username, email, password):
    """
    Create an admin user with the given credentials
    
    Parameters:
    - username: string
    - email: string
    - password: string
    
    Returns:
    - success: boolean
    - message: string
    """
    # Check if admin already exists
    if Admin.query.filter_by(username=username).first():
        return False, f"Admin with username '{username}' already exists"
    
    if Admin.query.filter_by(email=email).first():
        return False, f"Admin with email '{email}' already exists"
    
    # Create new admin
    admin = Admin(
        username=username,
        email=email
    )
    admin.set_password(password)
    
    try:
        db.session.add(admin)
        db.session.commit()
        logging.info(f"Created new admin user: {username}")
        return True, f"Admin user '{username}' created successfully"
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating admin user: {str(e)}")
        return False, f"Error creating admin: {str(e)}"
