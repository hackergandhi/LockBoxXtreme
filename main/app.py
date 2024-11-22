from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
from bcrypt import hashpw, gensalt, checkpw
import os
import secrets
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Encryption key (reuse the same key across sessions)
ENCRYPTION_KEY_FILE = 'encryption_key.key'

if os.path.exists(ENCRYPTION_KEY_FILE):
    with open(ENCRYPTION_KEY_FILE, 'rb') as f:
        ENCRYPTION_KEY = f.read()
else:
    ENCRYPTION_KEY = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, 'wb') as f:
        f.write(ENCRYPTION_KEY)

fernet = Fernet(ENCRYPTION_KEY)
# Models
class MasterPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False)
    encrypted_password = db.Column(db.String(256), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('menu'))
    return render_template('home.html')

@app.route('/set_master_password', methods=['GET', 'POST'])
def set_master_password():
    if MasterPassword.query.first():
        flash('Master password is already set. Please log in.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        master_password = request.form.get('master_password')
        if not master_password:
            flash('Master password is required!', 'error')
            return redirect(url_for('set_master_password'))

        hashed_pw = hashpw(master_password.encode(), gensalt())
        db.session.add(MasterPassword(password_hash=hashed_pw.decode()))
        db.session.commit()
        flash('Master password set successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('set_master_password.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        master_password = request.form.get('master_password')
        master_password_entry = MasterPassword.query.first()

        if not master_password_entry or not checkpw(master_password.encode(), master_password_entry.password_hash.encode()):
            flash('Invalid master password!', 'error')
            return redirect(url_for('login'))

        session['logged_in'] = True
        session['master_password'] = master_password
        flash('Logged in successfully!', 'success')
        return redirect(url_for('menu'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/menu')
def menu():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/store_password', methods=['GET', 'POST'])
def store_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        service_name = request.form.get('service_name')
        password = request.form.get('password')

        if not service_name or not password:
            flash('Service name and password are required!', 'error')
            return redirect(url_for('store_password'))

        encrypted_password = fernet.encrypt(password.encode()).decode()
        db.session.add(PasswordEntry(service_name=service_name, encrypted_password=encrypted_password))
        db.session.commit()
        flash(f'Password for {service_name} stored successfully!', 'success')
        return redirect(url_for('menu'))

    return render_template('store_password.html')

@app.route('/retrieve_password', methods=['GET', 'POST'])
def retrieve_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    passwords = []
    if request.method == 'POST':
        # Get inputs from the form
        service_name = request.form.get('service_name')
        entered_master_password = request.form.get('master_password')

        # Verify master password
        master_password_entry = MasterPassword.query.first()
        if not master_password_entry or not checkpw(entered_master_password.encode(), master_password_entry.password_hash.encode()):
            flash('Master password is incorrect!', 'error')
            return redirect(url_for('retrieve_password'))

        # Fetch and decrypt passwords
        entries = PasswordEntry.query.filter(
            PasswordEntry.service_name.ilike(f'%{service_name}%')
        ).all() if service_name else PasswordEntry.query.all()

        if not entries:
            flash(f'No passwords found{"" if not service_name else f" for {service_name}"}!', 'error')
        else:
            for entry in entries:
                decrypted_password = fernet.decrypt(entry.encrypted_password.encode()).decode()
                passwords.append({
                    'service': entry.service_name,
                    'password': decrypted_password
                })
    
    return render_template('retrieve_password.html', passwords=passwords)

@app.route('/generate_password', methods=['GET'])
def generate_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(16))
    return render_template('generate_password.html', password=password)

@app.route('/update_master_password', methods=['GET', 'POST'])
def update_master_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        master_password_entry = MasterPassword.query.first()

        if not checkpw(current_password.encode(), master_password_entry.password_hash.encode()):
            flash('Current password is incorrect!', 'error')
        else:
            hashed_pw = hashpw(new_password.encode(), gensalt())
            master_password_entry.password_hash = hashed_pw.decode()
            db.session.commit()
            session.clear()  # Log the user out for security
            flash('Master password updated successfully! Please log in again.', 'success')
            return redirect(url_for('login'))

    return render_template('update_master_password.html')

@app.route('/delete_password', methods=['GET', 'POST'])
def delete_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        service_name = request.form.get('service_name')
        master_password = request.form.get('master_password')

        master_password_entry = MasterPassword.query.first()

        if not checkpw(master_password.encode(), master_password_entry.password_hash.encode()):
            flash('Master password is incorrect!', 'error')
        else:
            entry = PasswordEntry.query.filter_by(service_name=service_name).first()
            if not entry:
                flash(f'No password found for {service_name}!', 'error')
            else:
                db.session.delete(entry)
                db.session.commit()
                flash(f'Password for {service_name} deleted successfully!', 'success')

    return render_template('delete_password.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
