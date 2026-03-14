# 🗳️ Voting Eligibility Checker

A modern, responsive web application to check if a citizen is eligible to vote based on age and address verification using SQL-driven conditional queries.

## ✨ Features

- **Modern UI**: Beautiful, responsive design with HTML/CSS/JavaScript
- **SQL Database**: Separate `schema.sql` file with comprehensive database structure
- **Conditional Queries**: Advanced SQL queries for age calculation and eligibility checks
- **Address Verification**: Optional city/state verification for enhanced security
- **Admin Panel**: Complete CRUD operations for citizen management
- **Real-time Validation**: Instant eligibility checking with detailed feedback
- **Configurable Rules**: Database-driven voting rules system

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with separate schema file
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with gradients and animations
- **API**: RESTful JSON API endpoints

## 📋 Requirements

- Python 3.7+
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone/Download the Project
```bash
# Navigate to your project directory
cd "C:\Users\CHETAN\OneDrive\Desktop\chetan dbms"
```

### 2. Install Dependencies
```powershell
# Install required packages
pip install -r requirements.txt
```

### 3. Run the Application
```powershell
# Start the Flask server
python app.py
```

### 4. Access the Application
- **Main App**: http://127.0.0.1:5000
- **Admin Panel**: http://127.0.0.1:5000/admin

## 📊 Database Schema

The application uses a separate `schema.sql` file that includes:

- **citizens** table: Stores citizen information with age calculation
- **voting_rules** table: Configurable eligibility rules
- **Indexes**: Optimized for performance
- **Sample Data**: Pre-populated with test citizens

### Key SQL Features:
- Age calculation using `julianday()` function
- Conditional queries for eligibility checking
- Soft delete functionality
- Comprehensive indexing

## 🎯 Usage

### For Citizens:
1. Enter your National ID (e.g., IND-001)
2. Optionally provide city/state for address verification
3. Click "Check Eligibility" to get instant results
4. View detailed eligibility criteria and reasoning

### For Administrators:
1. Access the admin panel at `/admin`
2. View all citizens with their eligibility status
3. Add new citizens with complete information
4. Delete citizens (soft delete)
5. Manage voting rules

## 🔍 Sample Data

The database comes pre-loaded with sample citizens:
- **IND-001**: Rajesh Kumar (Age: 29) - ✅ Eligible
- **IND-002**: Priya Sharma (Age: 14) - ❌ Not Eligible (Underage)
- **IND-003**: Amit Patel (Age: 36) - ✅ Eligible
- **IND-004**: Sneha Reddy (Age: 19) - ✅ Eligible
- **IND-005**: Vikram Singh (Age: 32) - ✅ Eligible
- **IND-006**: Anita Desai (Age: 39) - ✅ Eligible
- **IND-007**: Rohit Verma (Age: 12) - ❌ Not Eligible (Underage)
- **IND-008**: Kavita Joshi (Age: 34) - ✅ Eligible

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Styling**: Gradient backgrounds, smooth animations
- **Interactive Elements**: Hover effects, loading states
- **Real-time Feedback**: Instant validation and results
- **Accessibility**: Proper labels and keyboard navigation

## 🔧 API Endpoints

- `POST /check` - Check citizen eligibility
- `GET /admin` - Admin panel
- `POST /admin/add` - Add new citizen
- `DELETE /admin/delete/<id>` - Delete citizen
- `GET /admin/rules` - Get voting rules

## 📱 Screenshots

The application features:
- Clean, modern interface with gradient backgrounds
- Form validation and error handling
- Detailed eligibility results with reasoning
- Admin panel with data management
- Responsive design for all devices

## 🔒 Security Notes

- This is a demo application for educational purposes
- Do not use in production without proper security measures
- Database is local SQLite (not suitable for production)
- No authentication/authorization implemented

## 🛠️ Customization

### Adding New Voting Rules:
1. Insert into `voting_rules` table
2. Update eligibility logic in `app.py`
3. Restart the application

### Modifying UI:
- Edit CSS in `templates/index.html` and `templates/admin.html`
- JavaScript functions are inline for easy modification
- Responsive breakpoints can be adjusted

## 📝 License

This project is for educational purposes. Feel free to modify and use for learning.

## 🤝 Contributing

This is a demo project, but suggestions and improvements are welcome!

---

**Happy Voting! 🗳️**


