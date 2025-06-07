from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '1234pr'
app.config['UPLOAD_FOLDER'] = 'static/images'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mysql123",
        database="helphive"
    )

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['email'] = user['email']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))  # Redirect to home page after login
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access dashboard.')
        return redirect(url_for('login'))
    return f"Welcome {session['user_name']}! <br><a href='/logout'>Logout</a>"


# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Server-side validation
        errors = []
        if not name:
            errors.append("Name is required.")
        if not email or '@' not in email:
            errors.append("Valid email is required.")
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')

        # Hash password and save to DB
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
            """, (name, email, password_hash))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')  # 👈 This shows the real error
            return render_template('register.html')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')


# ---------- HOME ----------
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', user_name=session['user_name'])
    return render_template('home.html', user_name=None)

# ---------- SERVICES ----------
@app.route('/services')
def services():
    services_list = [
        {'name': 'Cleaning', 'image': 'images/cleaning.jpg'},
        {'name': 'Electrician', 'image': 'images/electrician.jpg'},
        {'name': 'Doctor Visit', 'image': 'images/doctor.jpg'},
        {'name': 'Salon & Spa', 'image': 'images/salon&spa.jpg'},
        {'name': 'Home Painting', 'image': 'images/homepainting.jpg'}
    ]
    return render_template('services.html', services=services_list)

# ---------- PROVIDERS ----------
@app.route('/provider_cleaning')
def provider_cleaning():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    cleaning_providers = [provider for provider in provider_data if provider.get('category', '').lower() == 'cleaning']

    for provider in cleaning_providers:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'

    return render_template('provider_cleaning.html', providers=cleaning_providers)

@app.route('/provider_electrician')
def provider_electrician():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_electrician = [p for p in provider_data if p.get('category', '').lower() == 'electrician']

    for provider in provider_electrician:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'

    return render_template('provider_electrician.html', providers=provider_electrician)

@app.route('/provider_plumber')
def provider_plumber():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_plumber = [p for p in provider_data if p.get('category', '').lower() == 'plumber']

    for provider in provider_plumber:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'

    return render_template('provider_plumber.html', providers=provider_plumber)

@app.route('/provider_daycare')
def provider_daycare():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_daycare = [p for p in provider_data if p.get('category', '').lower() == 'daycare']

    for provider in provider_daycare:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'
    return render_template('provider_daycare.html', providers=provider_daycare)

@app.route('/provider_doctor')
def provider_doctor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_doctor = [p for p in provider_data if p.get('category', '').lower() == 'doctor']

    for provider in provider_doctor:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'
    return render_template('provider_doctor.html', providers=provider_doctor)


# ---------- BOOKING ----------
@app.route('/book/<int:provider_id>', methods=['GET', 'POST'])
def book(provider_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM providers WHERE provider_id = %s", (provider_id,))
    provider = cursor.fetchone()

    if not provider:
        cursor.close()
        conn.close()
        return "Provider not found", 404

    cursor.execute("SELECT service_name, description FROM services WHERE service_name = %s", (provider['category'],))
    service = cursor.fetchone()
    service_name = service['service_name'] if service else 'Unknown'
    service_description = service['description'] if service else 'No description available.'

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        date = request.form['date']
        time = request.form['time']
        scheduled_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        cursor.execute("""
            INSERT INTO bookings (customer_name, provider_name, service_name, scheduled_time)
            VALUES (%s, %s, %s, %s)
        """, (customer_name, provider['name'], service_name, scheduled_time))
        conn.commit()

        cursor.close()
        conn.close()
        return '''
            <script>
            alert("Booking confirmed!");
            window.location.href = "/";
            </script>
        '''

    cursor.close()
    conn.close()
    return render_template('book.html', provider=provider, service_name=service_name, service_description=service_description)

# ---------- RUN ----------
if __name__ == '__main__':
    app.secret_key = '1234pr'
    app.run(debug=True)
