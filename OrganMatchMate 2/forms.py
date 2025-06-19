from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField, TelField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from models import ORGAN_TYPES, BLOOD_GROUPS, URGENCY_LEVELS, GENDER_TYPES

class DonorForm(FlaskForm):
    """Form for donor registration"""
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(),
        NumberRange(min=18, max=80, message='Age must be between 18 and 80')
    ])
    
    gender = SelectField('Gender', choices=[(g, g) for g in GENDER_TYPES], validators=[
        DataRequired()
    ])
    
    blood_group = SelectField('Blood Group', choices=[(bg, bg) for bg in BLOOD_GROUPS], validators=[
        DataRequired()
    ])
    
    organ_type = SelectField('Organ Type', choices=[(organ, organ) for organ in ORGAN_TYPES], validators=[
        DataRequired()
    ])
    
    contact = TelField('Contact Number', validators=[
        DataRequired(),
        Length(min=10, max=15, message='Contact number must be between 10 and 15 digits')
    ])
    
    availability = BooleanField('Currently Available for Donation', default=True)
    
    submit = SubmitField('Register as Donor')

class RecipientForm(FlaskForm):
    """Form for recipient registration"""
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(),
        NumberRange(min=0, max=100, message='Age must be between 0 and 100')
    ])
    
    gender = SelectField('Gender', choices=[(g, g) for g in GENDER_TYPES], validators=[
        DataRequired()
    ])
    
    blood_group = SelectField('Blood Group', choices=[(bg, bg) for bg in BLOOD_GROUPS], validators=[
        DataRequired()
    ])
    
    required_organ = SelectField('Required Organ', choices=[(organ, organ) for organ in ORGAN_TYPES], validators=[
        DataRequired()
    ])
    
    urgency = SelectField('Urgency Level', choices=[(level, level) for level in URGENCY_LEVELS], validators=[
        DataRequired()
    ])
    
    contact = TelField('Contact Number', validators=[
        DataRequired(),
        Length(min=10, max=15, message='Contact number must be between 10 and 15 digits')
    ])
    
    submit = SubmitField('Register as Recipient')
