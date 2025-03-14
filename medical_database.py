import sqlite3
import os
from datetime import datetime, timedelta
import random

def initialize_medical_database():
    """Create and populate the medical database with sample data"""
    
    # Remove existing database if it exists
    if os.path.exists("medical.db"):
        os.remove("medical.db")
    
    # Connect to SQLite database (will create it if it doesn't exist)
    connection = sqlite3.connect("medical.db")
    
    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()
    
    # Create patients table
    cursor.execute("""
    CREATE TABLE patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        date_of_birth DATE,
        gender VARCHAR(10),
        blood_type VARCHAR(5),
        contact_number VARCHAR(15),
        email VARCHAR(100),
        address TEXT,
        registration_date DATE
    )
    """)
    
    # Create doctors table
    cursor.execute("""
    CREATE TABLE doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        specialization VARCHAR(100),
        license_number VARCHAR(20),
        contact_number VARCHAR(15),
        email VARCHAR(100)
    )
    """)
    
    # Create medications table
    cursor.execute("""
    CREATE TABLE medications (
        medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100),
        manufacturer VARCHAR(100),
        category VARCHAR(50),
        description TEXT,
        standard_dosage VARCHAR(50),
        side_effects TEXT
    )
    """)
    
    # Create medical_records table
    cursor.execute("""
    CREATE TABLE medical_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        diagnosis TEXT,
        treatment_plan TEXT,
        visit_date DATE,
        follow_up_date DATE,
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
    )
    """)
    
    # Create prescriptions table
    cursor.execute("""
    CREATE TABLE prescriptions (
        prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER,
        medication_id INTEGER,
        dosage VARCHAR(50),
        frequency VARCHAR(50),
        start_date DATE,
        end_date DATE,
        instructions TEXT,
        FOREIGN KEY (record_id) REFERENCES medical_records (record_id),
        FOREIGN KEY (medication_id) REFERENCES medications (medication_id)
    )
    """)
    
    # Insert sample patient data
    patients = [
        ('John', 'Smith', '1985-03-20', 'Male', 'A+', '555-123-4567', 'john.smith@email.com', '123 Main St, Anytown', '2023-01-15'),
        ('Sarah', 'Johnson', '1990-07-12', 'Female', 'O-', '555-234-5678', 'sarah.j@email.com', '456 Oak Ave, Somewhere', '2023-02-20'),
        ('Michael', 'Williams', '1978-11-30', 'Male', 'B+', '555-345-6789', 'michael.w@email.com', '789 Pine Rd, Elsewhere', '2023-03-05'),
        ('Emily', 'Brown', '1995-04-25', 'Female', 'AB+', '555-456-7890', 'emily.b@email.com', '101 Cedar Ln, Nowhere', '2023-01-30'),
        ('Robert', 'Jones', '1965-09-18', 'Male', 'A-', '555-567-8901', 'robert.j@email.com', '202 Maple Dr, Anywhere', '2023-02-10')
    ]
    
    cursor.executemany("""
    INSERT INTO patients (first_name, last_name, date_of_birth, gender, blood_type, contact_number, email, address, registration_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, patients)
    
    # Insert sample doctor data
    doctors = [
        ('Elizabeth', 'Taylor', 'Cardiology', 'MD12345', '555-987-6543', 'dr.taylor@hospital.com'),
        ('James', 'Anderson', 'Neurology', 'MD23456', '555-876-5432', 'dr.anderson@hospital.com'),
        ('Patricia', 'Martinez', 'Pediatrics', 'MD34567', '555-765-4321', 'dr.martinez@hospital.com'),
        ('William', 'Garcia', 'Orthopedics', 'MD45678', '555-654-3210', 'dr.garcia@hospital.com'),
        ('Jennifer', 'Lopez', 'Dermatology', 'MD56789', '555-543-2109', 'dr.lopez@hospital.com')
    ]
    
    cursor.executemany("""
    INSERT INTO doctors (first_name, last_name, specialization, license_number, contact_number, email)
    VALUES (?, ?, ?, ?, ?, ?)
    """, doctors)
    
    # Insert sample medication data
    medications = [
        ('Lisinopril', 'Merck', 'ACE Inhibitor', 'Used to treat high blood pressure and heart failure', '10mg once daily', 'Dry cough, dizziness, headache'),
        ('Atorvastatin', 'Pfizer', 'Statin', 'Used to lower cholesterol levels', '20mg once daily', 'Muscle pain, joint pain, digestive issues'),
        ('Amoxicillin', 'GlaxoSmithKline', 'Antibiotic', 'Used to treat bacterial infections', '500mg every 8 hours', 'Diarrhea, rash, nausea'),
        ('Sertraline', 'Pfizer', 'SSRI', 'Used to treat depression and anxiety disorders', '50mg once daily', 'Nausea, insomnia, dizziness'),
        ('Prednisone', 'Novartis', 'Corticosteroid', 'Used to treat inflammation and autoimmune conditions', '20mg daily, tapering', 'Weight gain, mood changes, increased blood sugar')
    ]
    
    cursor.executemany("""
    INSERT INTO medications (name, manufacturer, category, description, standard_dosage, side_effects)
    VALUES (?, ?, ?, ?, ?, ?)
    """, medications)
    
    # Generate sample medical records and prescriptions
    now = datetime.now()
    
    for patient_id in range(1, 6):  # For each patient
        # Generate 1-3 medical records per patient
        for _ in range(random.randint(1, 3)):
            # Random date in the last year
            visit_date = (now - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
            follow_up_date = (datetime.strptime(visit_date, '%Y-%m-%d') + timedelta(days=random.randint(14, 90))).strftime('%Y-%m-%d')
            
            # Random doctor
            doctor_id = random.randint(1, 5)
            
            # Sample diagnoses
            diagnoses = [
                "Essential hypertension",
                "Type 2 diabetes mellitus",
                "Acute upper respiratory infection",
                "Major depressive disorder",
                "Generalized anxiety disorder",
                "Acute bronchitis",
                "Osteoarthritis",
                "Allergic rhinitis",
                "Gastroesophageal reflux disease",
                "Urinary tract infection"
            ]
            
            # Sample treatment plans
            treatment_plans = [
                "Lifestyle modifications and medication",
                "Diet change, exercise, and medication review",
                "Rest, fluids, and antibiotics if bacterial",
                "Cognitive behavioral therapy and medication",
                "Physical therapy and anti-inflammatory medication",
                "Proton pump inhibitor and diet modifications",
                "Antibiotics and increased fluid intake"
            ]
            
            # Sample notes
            notes = [
                "Patient responded well to treatment",
                "Symptoms improving but continue monitoring",
                "Consider referral to specialist if no improvement",
                "Discussed importance of medication adherence",
                "Patient reports side effects from medication",
                "Bloodwork ordered to monitor progress",
                "Patient education provided on condition management"
            ]
            
            # Insert medical record
            cursor.execute("""
            INSERT INTO medical_records (patient_id, doctor_id, diagnosis, treatment_plan, visit_date, follow_up_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id,
                doctor_id,
                random.choice(diagnoses),
                random.choice(treatment_plans),
                visit_date,
                follow_up_date,
                random.choice(notes)
            ))
            
            # Get the inserted record ID
            record_id = cursor.lastrowid
            
            # Maybe add prescriptions (70% chance)
            if random.random() < 0.7:
                # Random number of medications (1-3)
                for _ in range(random.randint(1, 3)):
                    medication_id = random.randint(1, 5)
                    
                    # Sample dosages
                    dosages = ["10mg", "20mg", "25mg", "50mg", "100mg", "500mg"]
                    
                    # Sample frequencies
                    frequencies = ["Once daily", "Twice daily", "Three times daily", "Every 8 hours", "Every 12 hours", "As needed"]
                    
                    # Sample instructions
                    instructions = [
                        "Take with food",
                        "Take on an empty stomach",
                        "Avoid alcohol",
                        "May cause drowsiness",
                        "Complete full course of medication",
                        "Take at the same time each day",
                        "Do not crush or chew tablets"
                    ]
                    
                    start_date = visit_date
                    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d')
                    
                    # Insert prescription
                    cursor.execute("""
                    INSERT INTO prescriptions (record_id, medication_id, dosage, frequency, start_date, end_date, instructions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        record_id,
                        medication_id,
                        random.choice(dosages),
                        random.choice(frequencies),
                        start_date,
                        end_date,
                        random.choice(instructions)
                    ))
    
    # Commit changes and close connection
    connection.commit()
    
    print("Medical database initialized successfully with sample data")
    
    # Display some sample data
    print("\nSample Patients:")
    for row in cursor.execute("SELECT patient_id, first_name, last_name, gender, blood_type FROM patients LIMIT 5"):
        print(row)
    
    print("\nSample Medical Records:")
    for row in cursor.execute("""
        SELECT r.record_id, p.first_name || ' ' || p.last_name as patient, 
               d.first_name || ' ' || d.last_name as doctor, r.diagnosis, r.visit_date 
        FROM medical_records r
        JOIN patients p ON r.patient_id = p.patient_id
        JOIN doctors d ON r.doctor_id = d.doctor_id
        LIMIT 5
    """):
        print(row)
    
    print("\nSample Prescriptions:")
    for row in cursor.execute("""
        SELECT pr.prescription_id, p.first_name || ' ' || p.last_name as patient, 
               m.name as medication, pr.dosage, pr.frequency
        FROM prescriptions pr
        JOIN medical_records r ON pr.record_id = r.record_id
        JOIN patients p ON r.patient_id = p.patient_id
        JOIN medications m ON pr.medication_id = m.medication_id
        LIMIT 5
    """):
        print(row)
    
    connection.close()

if __name__ == "__main__":
    initialize_medical_database()
