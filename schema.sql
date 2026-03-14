
DROP TABLE IF EXISTS citizens;
DROP TABLE IF EXISTS voting_rules;

CREATE TABLE citizens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    national_id TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'India',
    phone_number TEXT,
    email TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Voting rules table - configurable eligibility rules
CREATE TABLE voting_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    rule_type TEXT NOT NULL, -- 'age', 'address', 'country'
    rule_value TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default voting rules
INSERT INTO voting_rules (rule_name, rule_type, rule_value) VALUES
('Minimum Age', 'age', '18'),
('Required Country', 'country', 'India'),
('Address Verification Required', 'address', 'true');

-- Insert sample citizens data
INSERT INTO citizens (national_id, full_name, date_of_birth, address, city, state, country, phone_number, email) VALUES
('IND-001', 'Rajesh Kumar', '1995-03-15', '123 MG Road', 'Mumbai', 'Maharashtra', 'India', '+91-9876543210', 'rajesh.kumar@email.com'),
('IND-002', 'Priya Sharma', '2010-07-22', '456 Park Avenue', 'Delhi', 'Delhi', 'India', '+91-9876543211', 'priya.sharma@email.com'),
('IND-003', 'Amit Patel', '1988-11-08', '789 Gandhi Street', 'Ahmedabad', 'Gujarat', 'India', '+91-9876543212', 'amit.patel@email.com'),
('IND-004', 'Sneha Reddy', '2005-12-03', '321 Tech Park', 'Bangalore', 'Karnataka', 'India', '+91-9876543213', 'sneha.reddy@email.com'),
('IND-005', 'Vikram Singh', '1992-05-18', '654 Lake View', 'Pune', 'Maharashtra', 'India', '+91-9876543214', 'vikram.singh@email.com'),
('IND-006', 'Anita Desai', '1985-09-12', '987 Hill Station', 'Shimla', 'Himachal Pradesh', 'India', '+91-9876543215', 'anita.desai@email.com'),
('IND-007', 'Rohit Verma', '2012-01-25', '147 Valley Road', 'Dehradun', 'Uttarakhand', 'India', '+91-9876543216', 'rohit.verma@email.com'),
('IND-008', 'Kavita Joshi', '1990-04-30', '258 Garden City', 'Jaipur', 'Rajasthan', 'India', '+91-9876543217', 'kavita.joshi@email.com');

-- Create indexes for better performance
CREATE INDEX idx_citizens_national_id ON citizens(national_id);
CREATE INDEX idx_citizens_city_state ON citizens(city, state);
CREATE INDEX idx_citizens_dob ON citizens(date_of_birth);
CREATE INDEX idx_voting_rules_type ON voting_rules(rule_type);


