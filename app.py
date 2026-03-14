from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'voting_eligibility_secret_key_2024'

# Database configuration
DB_PATH = 'voting_eligibility.db'

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with schema"""
    if not os.path.exists(DB_PATH):
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
        
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(schema_sql)
        conn.close()
        print("Database initialized successfully!")

def calculate_age(date_of_birth):
    """Calculate age from date of birth"""
    try:
        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except (ValueError, TypeError, AttributeError):
        return 0

def check_eligibility(national_id, city=None, state=None, phone_number=None, email=None, verification_level='standard', result_format='detailed'):
    """Check voting eligibility with conditional SQL queries"""
    conn = get_db_connection()
    
    # Get citizen details with age calculation
    query = """
    SELECT 
        c.*,
        CAST((julianday('now') - julianday(c.date_of_birth)) / 365.25 AS INTEGER) as age
    FROM citizens c 
    WHERE c.national_id = ? AND c.is_active = 1
    """
    
    citizen = conn.execute(query, (national_id,)).fetchone()
    
    if not citizen:
        conn.close()
        return {
            'found': False,
            'message': 'Citizen not found in database'
        }
    
    # Get voting rules
    rules_query = "SELECT rule_type, rule_value FROM voting_rules WHERE is_active = 1"
    rules = {row['rule_type']: row['rule_value'] for row in conn.execute(rules_query).fetchall()}
    
    # Check eligibility conditions
    eligibility_checks = []
    is_eligible = True
    
    # Age check
    min_age = int(rules.get('age', 18))
    if citizen['age'] < min_age:
        is_eligible = False
        eligibility_checks.append(f"Age {citizen['age']} is below minimum required age of {min_age}")
    else:
        eligibility_checks.append(f"Age {citizen['age']} meets minimum requirement of {min_age}")
    
    # Country check
    required_country = rules.get('country', 'India')
    if citizen['country'].lower() != required_country.lower():
        is_eligible = False
        eligibility_checks.append(f"Country '{citizen['country']}' does not match required '{required_country}'")
    else:
        eligibility_checks.append(f"Country '{citizen['country']}' is valid")
    
    # Address verification based on verification level
    address_match = True
    if verification_level in ['standard', 'strict']:
        if city and city.strip():
            if citizen['city'].lower() != city.lower():
                address_match = False
                eligibility_checks.append(f"City '{citizen['city']}' does not match provided '{city}'")
            else:
                eligibility_checks.append(f"City '{citizen['city']}' matches provided address")
        
        if state and state.strip():
            if citizen['state'].lower() != state.lower():
                address_match = False
                eligibility_checks.append(f"State '{citizen['state']}' does not match provided '{state}'")
            else:
                eligibility_checks.append(f"State '{citizen['state']}' matches provided address")
    
    # Strict verification - phone and email check
    if verification_level == 'strict':
        if phone_number and phone_number.strip():
            if citizen['phone_number'] and citizen['phone_number'].strip():
                if citizen['phone_number'].strip() != phone_number.strip():
                    address_match = False
                    eligibility_checks.append(f"Phone number does not match records")
                else:
                    eligibility_checks.append(f"Phone number verified")
            else:
                eligibility_checks.append(f"Phone number not found in records")
        
        if email and email.strip():
            if citizen['email'] and citizen['email'].strip():
                if citizen['email'].strip().lower() != email.strip().lower():
                    address_match = False
                    eligibility_checks.append(f"Email does not match records")
                else:
                    eligibility_checks.append(f"Email verified")
            else:
                eligibility_checks.append(f"Email not found in records")
    
    if not address_match:
        is_eligible = False
    
    conn.close()
    
    return {
        'found': True,
        'citizen': dict(citizen),
        'is_eligible': is_eligible,
        'eligibility_checks': eligibility_checks,
        'age': citizen['age'],
        'verification_level': verification_level,
        'result_format': result_format
    }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_eligibility_api():
    """API endpoint to check eligibility"""
    data = request.get_json()
    national_id = data.get('national_id', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    phone_number = data.get('phone_number', '').strip()
    email = data.get('email', '').strip()
    verification_level = data.get('verification_level', 'standard')
    result_format = data.get('result_format', 'detailed')
    
    if not national_id:
        return jsonify({'error': 'National ID is required'}), 400
    
    result = check_eligibility(
        national_id, 
        city, 
        state, 
        phone_number, 
        email, 
        verification_level, 
        result_format
    )
    return jsonify(result)

@app.route('/admin')
def admin():
    """Admin page for managing citizens"""
    conn = get_db_connection()
    citizens = conn.execute("""
        SELECT 
            c.*,
            CAST((julianday('now') - julianday(c.date_of_birth)) / 365.25 AS INTEGER) as age
        FROM citizens c 
        WHERE c.is_active = 1 
        ORDER BY c.id DESC
    """).fetchall()
    conn.close()
    return render_template('admin.html', citizens=citizens)

@app.route('/admin/add', methods=['POST'])
def add_citizen():
    """Add new citizen"""
    data = request.get_json()
    
    required_fields = ['national_id', 'full_name', 'date_of_birth', 'address', 'city', 'state']
    missing_fields = [field for field in required_fields if not data.get(field, '').strip()]
    
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO citizens (national_id, full_name, date_of_birth, address, city, state, country, phone_number, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['national_id'],
            data['full_name'],
            data['date_of_birth'],
            data['address'],
            data['city'],
            data['state'],
            data.get('country', 'India'),
            data.get('phone_number', ''),
            data.get('email', '')
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': 'Citizen added successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'National ID already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/delete/<int:citizen_id>', methods=['DELETE'])
def delete_citizen(citizen_id):
    """Delete citizen (soft delete)"""
    try:
        conn = get_db_connection()
        conn.execute("UPDATE citizens SET is_active = 0 WHERE id = ?", (citizen_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': 'Citizen deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/rules')
def get_rules():
    """Get voting rules"""
    conn = get_db_connection()
    rules = conn.execute("SELECT * FROM voting_rules WHERE is_active = 1").fetchall()
    conn.close()
    return jsonify([dict(rule) for rule in rules])

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='127.0.0.1', port=5000)



