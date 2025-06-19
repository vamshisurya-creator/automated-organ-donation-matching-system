import os

import jinja2
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

import models
from database import db
from utils import create_admin, generate_matches, populate_dummy_data

# Create and configure the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///organ_donation.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add custom template filters
@app.template_filter('nl2br')
def nl2br(value):
    """Convert newlines to <br> tags for proper display in HTML"""
    if value:
        return jinja2.utils.markupsafe.Markup(value.replace('\n', '<br>'))
    return ""

@login_manager.user_loader
def load_user(user_id):
    return models.Admin.query.get(int(user_id))

# Main routes
@app.route('/')
@app.route('/home')
def home():
    """Home page with system statistics"""
    donors_count = models.Donor.query.filter_by(availability=True).count()
    recipients_count = models.Recipient.query.count()
    matches_count = models.Match.query.count()
    return render_template('home.html', 
                           donors_count=donors_count, 
                           recipients_count=recipients_count, 
                           matches_count=matches_count)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return redirect(url_for('login'))
        
        admin = models.Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Registration routes
@app.route('/donor/register', methods=['GET', 'POST'])
def donor_register():
    """Donor registration page"""
    from forms import DonorForm
    form = DonorForm()
    
    if form.validate_on_submit():
        donor = models.Donor(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            blood_group=form.blood_group.data,
            organ_type=form.organ_type.data,
            contact=form.contact.data,
            availability=form.availability.data
        )
        
        db.session.add(donor)
        db.session.commit()
        
        flash('Thank you for registering as a donor!', 'success')
        return redirect(url_for('home'))
        
    return render_template('donor_register.html', form=form)

@app.route('/recipient/register', methods=['GET', 'POST'])
def recipient_register():
    """Recipient registration page"""
    from forms import RecipientForm
    form = RecipientForm()
    
    if form.validate_on_submit():
        recipient = models.Recipient(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            blood_group=form.blood_group.data,
            required_organ=form.required_organ.data,
            urgency=form.urgency.data,
            contact=form.contact.data
        )
        
        db.session.add(recipient)
        db.session.commit()
        
        flash('You have been registered as a recipient!', 'success')
        return redirect(url_for('home'))
        
    return render_template('recipient_register.html', form=form)

# Feature routes
@app.route('/match', methods=['GET', 'POST'])
def match():
    """Match page to run matching algorithm and display results"""
    if request.method == 'POST':
        new_matches = generate_matches()
        if new_matches:
            flash(f'Generated {len(new_matches)} new potential matches!', 'success')
        else:
            flash('No new matches found at this time.', 'info')
            
    matches = models.Match.query.all()
    return render_template('match.html', matches=matches)

@app.route('/organs')
def organs():
    """Display organ availability tracker"""
    # Get available donors grouped by organ type and blood group
    donors = models.Donor.query.filter_by(availability=True).all()
    
    # Organize data for display
    organ_data = {}
    for organ in models.ORGAN_TYPES:
        organ_data[organ] = {
            'blood_groups': {bg: 0 for bg in models.BLOOD_GROUPS},
            'total': 0
        }
    
    for donor in donors:
        organ_data[donor.organ_type]['blood_groups'][donor.blood_group] += 1
        organ_data[donor.organ_type]['total'] += 1
    
    # Get recipient data by urgency
    recipient_data = {}
    for organ in models.ORGAN_TYPES:
        recipient_data[organ] = {
            'High': 0,
            'Medium': 0,
            'Low': 0,
            'total': 0
        }
    
    recipients = models.Recipient.query.all()
    for recipient in recipients:
        recipient_data[recipient.required_organ][recipient.urgency] += 1
        recipient_data[recipient.required_organ]['total'] += 1
    
    return render_template('organs.html', 
                          organ_data=organ_data, 
                          recipient_data=recipient_data,
                          blood_groups=models.BLOOD_GROUPS)

@app.route('/notifications')
def notifications():
    """Display notifications of recent matches"""
    recent_matches = models.Match.query.order_by(models.Match.created_at.desc()).limit(10).all()
    return render_template('notifications.html', matches=recent_matches)

# Admin routes
@app.route('/admin')
@login_required
def admin():
    """Admin dashboard"""
    donors = models.Donor.query.all()
    recipients = models.Recipient.query.all()
    matches = models.Match.query.all()
    return render_template('admin.html', 
                           donors=donors, 
                           recipients=recipients, 
                           matches=matches)

@app.route('/recipient/edit/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def edit_recipient(recipient_id):
    """Edit recipient information"""
    from forms import RecipientForm
    recipient = models.Recipient.query.get_or_404(recipient_id)
    form = RecipientForm(obj=recipient)
    
    if form.validate_on_submit():
        form.populate_obj(recipient)
        db.session.commit()
        flash('Recipient information updated successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('recipient_edit.html', form=form, recipient=recipient)

@app.route('/donor/edit/<int:donor_id>', methods=['GET', 'POST'])
@login_required
def edit_donor(donor_id):
    """Edit donor information"""
    from forms import DonorForm
    donor = models.Donor.query.get_or_404(donor_id)
    form = DonorForm(obj=donor)
    
    if form.validate_on_submit():
        form.populate_obj(donor)
        db.session.commit()
        flash('Donor information updated successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('donor_edit.html', form=form, donor=donor)

@app.route('/donor/delete/<int:donor_id>')
@login_required
def delete_donor(donor_id):
    """Delete donor"""
    donor = models.Donor.query.get_or_404(donor_id)
    db.session.delete(donor)
    db.session.commit()
    flash('Donor deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/recipient/delete/<int:recipient_id>')
@login_required
def delete_recipient(recipient_id):
    """Delete recipient"""
    recipient = models.Recipient.query.get_or_404(recipient_id)
    db.session.delete(recipient)
    db.session.commit()
    flash('Recipient deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/match/delete/<int:match_id>')
@login_required
def delete_match(match_id):
    """Delete match"""
    match = models.Match.query.get_or_404(match_id)
    db.session.delete(match)
    db.session.commit()
    flash('Match deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/create', methods=['GET', 'POST'])
@login_required
def admin_create():
    """Create new admin user"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin_create'))

        success, message = create_admin(username, email, password)

        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')

        return redirect(url_for('admin'))

    return render_template('admin_create.html')

@app.route('/diagrams')
def diagrams():
    """Display system diagrams"""
    return render_template('diagrams.html')

# Initialize database and create tables
# The before_first_request decorator is deprecated in newer Flask versions
# Using with app.app_context() instead
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Check if we need to populate with initial data
        if models.Admin.query.count() == 0:
            populate_dummy_data()
            # Can't use flash here since we're outside of a request context
            print('Database initialized with sample data.')
    
    app.run(host='0.0.0.0', port=5000, debug=True)
