import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',         # Change to your MySQL username
    'password': 'mysql123',  # Change to your MySQL password
    'host': 'localhost',
    'raise_on_warnings': True
}

DB_NAME = 'helphive'

TABLES = {}

TABLES['users'] = (
    """
    CREATE TABLE users (
        user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

TABLES['services'] = (
    """
    CREATE TABLE services (
        service_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        service_name VARCHAR(100) NOT NULL,
        description TEXT
    )
    """
)

TABLES['providers'] = (
    """
    CREATE TABLE providers (
        provider_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        bio TEXT,
        photo_url TEXT,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(15),
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

TABLES['bookings'] = (
    """
    CREATE TABLE bookings (
        booking_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(100),
        provider_name VARCHAR(100),
        service_name VARCHAR(100),
        scheduled_time TIMESTAMP,
        status VARCHAR(50) DEFAULT 'Pending'
    )
    """
)


TABLES['reviews'] = (
    """
    CREATE TABLE reviews (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        rating FLOAT,
        review TEXT
    )
    """
)

# Sample data for providers
SAMPLE_PROVIDERS = [
    ("Aarav Mehta", "Experienced in deep home cleaning and sanitization.", "images/cleaning1.jpg", "aarav@example.com", "9876543210", "cleaning"),
    ("Priya Sharma", "Eco-friendly cleaning specialist for homes and offices.", "images/cleaning2.jpg", "priya@example.com", "9876543211", "cleaning"),
    ("Rahul Singh", "Detail-oriented cleaner with 5+ years of experience.", "images/cleaning3.jpg", "rahul@example.com", "9876543212", "cleaning"),
    ("Neha Verma", "Quick and efficient housekeeper with flexible timing.", "images/cleaning4.jpg", "neha@example.com", "9876543213", "cleaning"),
    ("Kabir Patel", "Offers premium cleaning services with high client satisfaction.", "images/cleaning5.jpg", "kabir@example.com", "9876543214", "cleaning"),

    # Daycare
    ("Anjali Mehra", "Certified caregiver with 5+ years of experience in child development.", "images/daycare1.jpg", "anjalimehra@example.com", "9876531110", "daycare"),
    ("Ritika Sharma", "Warm and attentive daycare specialist focused on toddler learning.", "images/daycare2.jpg", "ritikasharma@example.com", "9876531111", "daycare"),
    ("Komal Verma", "Offers safe and fun daycare environment with personalized care.", "images/daycare3.jpg", "komalverma@example.com", "9876531112", "daycare"),
    ("Neha Sinha", "Early childhood educator passionate about nurturing young minds.", "images/daycare4.jpg", "nehasinha@example.com", "9876531113", "daycare"),
    ("Pooja Desai", "Trusted daycare provider with CPR certification and parent references.", "images/daycare5.jpg", "poojadesai@example.com", "9876531114", "daycare"),

    # Plumbers
    ("Deepak Rao", "Specialist in kitchen and bathroom pipe fittings.", "images/plumber1.jpg", "deepakrao@example.com", "9876522220", "plumber"),
    ("Naresh Gupta", "Expert in fixing leaks and installing taps.", "images/plumber2.jpg", "nareshgupta@example.com", "9876522221", "plumber"),
    ("Pintu Lal", "Experienced in residential plumbing and drainage.", "images/plumber3.jpg", "pintulal@example.com", "9876522222", "plumber"),
    ("Sunil Joshi", "Reliable plumber for emergency repairs and maintenance.", "images/plumber4.jpg", "suniljoshi@example.com", "9876522223", "plumber"),
    ("Gopal Mishra", "Affordable services for homes and commercial plumbing.", "images/plumber5.jpg", "gopalmishra@example.com", "9876522224", "plumber"),

    # Doctors
    ("Dr. Asha Mehta", "Pediatrician with over 10 years of experience in child healthcare.", "images/doctor1.jpg", "ashamehta@example.com", "9876511110", "doctor"),
    ("Dr. Rajeev Sharma", "General physician focused on adult medicine and preventive care.", "images/doctor2.jpg", "rajeevsharma@example.com", "9876511111", "doctor"),
    ("Dr. Neha Verma", "Dermatologist specializing in skin treatment and cosmetic care.", "images/doctor3.jpg", "nehaverma@example.com", "9876511112", "doctor"),
    ("Dr. Vikram Sinha", "Cardiologist with expertise in heart-related conditions and care.", "images/doctor4.jpg", "vikramsinha@example.com", "9876511113", "doctor"),
    ("Dr. Priya Nair", "Experienced gynecologist focused on women’s health and wellness.", "images/doctor5.jpg", "priyanair@example.com", "9876511114", "doctor"),

    # Electricians
    ("Ramu Yadav", "Expert in residential wiring and basic electrical repairs.", "images/electrician1.jpg", "ramu@example.com", "9876511110", "electrician"),
    ("Raju Kumar", "Skilled in fan, light, and inverter installations.", "images/electrician2.jpg", "raju@example.com", "9876511111", "electrician"),
    ("Kishor Patil", "Trusted local electrician with fast service.", "images/electrician3.jpg", "kishor@example.com", "9876511112", "electrician"),
    ("Suresh Chauhan", "Experienced in electrical maintenance and troubleshooting.", "images/electrician4.jpg", "suresh@example.com", "9876511113", "electrician"),
    ("Bablu Verma", "Affordable electrician for homes and small shops.", "images/electrician5.jpg", "bablu@example.com", "9876511114", "electrician"),
]

SAMPLE_SERVICES = [
    ("cleaning", "General and deep cleaning services."),
    ("electrician", "Electrical repairs and installations."),
    ("plumber", "Pipe, tap, and drainage solutions."),
    ("day care", "Professional child care services."),
    ("doctor", "General physician and specialized medical care.")
]

SIMPLE_SAMPLE_BOOKINGS = [
    ("Rohit Sharma", "Aarav Mehta", "cleaning", "2025-06-05 10:00:00", "Confirmed"),
    ("Sneha Reddy", "Pintu Lal", "plumber", "2025-06-06 14:00:00", "Pending"),
    ("Ajay Kumar", "Dr. Asha Mehta", "doctor", "2025-06-07 16:00:00", "Completed"),
]


def create_database(cursor):
    try:
        print(f"Dropping database if exists: {DB_NAME}")
        cursor.execute(f"DROP DATABASE IF EXISTS `{DB_NAME}`")
        print(f"Creating database: {DB_NAME}")
        cursor.execute(f"CREATE DATABASE `{DB_NAME}` DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Database {DB_NAME} created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)


def main():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        create_database(cursor)
        cnx.database = DB_NAME

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creating table {table_name}...")
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                print(f"Error creating table {table_name}: {err}")

        print("Inserting sample provider data...")
        provider_insert = (
            "INSERT INTO providers (name, bio, photo_url, email, phone, category) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cursor.executemany(provider_insert, SAMPLE_PROVIDERS)
        cnx.commit()

        print("Database and tables created successfully with sample data.")

        # Insert sample services
        print("Inserting sample services...")
        service_insert = (
            "INSERT INTO services (service_name, description) VALUES (%s, %s)"
        )
        cursor.executemany(service_insert, SAMPLE_SERVICES)
        cnx.commit()

        # Insert simplified sample bookings
        print("Inserting simplified sample bookings...")
        simple_booking_insert = (
            "INSERT INTO bookings (customer_name, provider_name, service_name, scheduled_time, status) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        cursor.executemany(simple_booking_insert, SIMPLE_SAMPLE_BOOKINGS)
        cnx.commit()


        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        print(err)

if __name__ == "__main__":
    main()
