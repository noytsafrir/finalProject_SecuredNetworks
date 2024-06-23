from flask import Flask, request, jsonify
<<<<<<< HEAD
from models import db, Customer, User
from flask_cors import CORS
from config import Config
=======
from models import db, Customer, User, PasswordHistory
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask_cors import CORS
from config import Config
from validator import *
>>>>>>> main
import re
import random
import string
import requests


def check_user(email):
    user = User.query.filter_by(email=email).first()
    return user is not None

def check_password(user, password):
    return user.check_password(password)

def password_configuration(password): #פונקציה שנוי ושיר צריכות לעדכן 
    # Example password configuration check
    return len(password) >= 8  # Add more checks as needed
 
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
<<<<<<< HEAD


=======
login_manager = LoginManager(app)
login_manager.login_view = 'login'

reset_codes = {}
>>>>>>> main

mock_users_db = {
    'user@example.com': 'password123',
    'admin@example.com': 'adminpass'
}

def check_user(email):
    user = User.query.filter_by(email=email).first()
    return user is not None

def check_password(user, password):
    return user.check_password(password)

def password_configuration(email,password):

    if(is_password_complex(password) == False or
        is_dictionary_word(password) == True or
        is_password_new(email, password) == False):
        return False
    return True

@app.route('/new_password', methods=['POST'])
def new_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found', 'status': 404})

    if not password_configuration(email,new_password):
        return jsonify({'message': 'Password does not meet configuration requirements', 'status': 400})

    user.set_password(new_password)
    user.reset_login_attempts()
    new_password_history = PasswordHistory(email=email)
    new_password_history.set_password(user.password_hash)
    db.session.add(new_password_history)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully', 'status': 200})

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer_name = data.get('customer_name')
    company_name = data.get('company_name')
    address = data.get('address')

    existing_customer = Customer.query.filter_by(customer_name=customer_name, company_name=company_name).first()
    if existing_customer:
        return jsonify({'message': 'Customer already exists', 'status': 400})

    new_customer = Customer(customer_name=customer_name, company_name=company_name, address=address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'New Customer was added successfully: ' + customer_name, 'status': 200})

@app.route('/verify_reset_code', methods=['POST'])
def verify_reset_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if reset_codes.get(email) == code:
        return jsonify({'message': 'Code verified', 'status': 200})
    else:
        return jsonify({'message': 'Invalid code or expired', 'status': 400})
#-------------------------------------------------Login-------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

<<<<<<< HEAD
    # if not email or not password:
    #     return jsonify({'message': 'Both email and password are required.', 'status': 'fail'}), 400

    # Check if the user exists in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})

    # Check if the password matches
    if user.check_password(password):
        return jsonify({'message': 'Login successful!', 'status': 200})
    else:
        return jsonify({'message': 'Invalid password.', 'status': 401})
    
#להתאים את הפרונט 
@app.route('/new_password', methods=['POST'])
def new_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found' , 'status': 404})

    if not password_configuration(new_password):
        return jsonify({'message': 'Password does not meet configuration requirements', 'status' : 400})

    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully', 'status' : 200})

#להתאים את הפרונט 
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer_name = data.get('customer_name')
    company_name = data.get('company_name')
    address = data.get('address')

    existing_customer = Customer.query.filter_by(customer_name=customer_name, company_name=company_name).first()
    if existing_customer:
        return jsonify({'message': 'Customer already exists', 'status': 400})

    new_customer = Customer(customer_name=customer_name, company_name=company_name, address=address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully' , 'status': 200})


=======
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})
    if user.login_attempts < Config.LOGIN_ATTEMPTS_LIMIT: 
        if user.check_password(password):
            user.reset_login_attempts()
            return jsonify({'message': 'Login successful!', 'status': 200})
        else:
            user.increment_login_attempts()
            return jsonify({'message': 'Invalid password.', 'status': 401})
    else:
        return jsonify({'message': 'Account locked.', 'status': 401})
#-------------------------------------------------End Login-------------------------------------------------
#-------------------------------------------------Register-------------------------------------------------
>>>>>>> main
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if check_user(email):
<<<<<<< HEAD
        return jsonify({'message': 'User already exists'}), 400
    
    if not password_configuration(password):
        return jsonify({'message': 'Password is WEAK AF! --> get better :L', 'status': 400})      # TODO change message

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'status': 200})

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
#     repeat_password = data.get('repeat_password')

#     print(f"Register attempt with email: {email}, password: {password}, repeat_password: {repeat_password}")

#     if not email or not password or not repeat_password:
#         print("All fields are required.")
#         return jsonify({'message': 'All fields are required.', 'status': 'fail'}), 400

#     email_pattern = r'^[^\s@]+@[^\s@]+\.(com|org)$'
#     if not re.match(email_pattern, email):
#         print("Invalid email format.")
#         return jsonify({'message': 'Invalid email format. Please use a valid email ending with .com or .org.', 'status': 'fail'}), 400

#     if password != repeat_password:
#         print("Passwords do not match.")
#         return jsonify({'message': 'Passwords do not match.', 'status': 'fail'}), 400
# #to do
#     if email in mock_users_db:
#         print("Email already registered.")
#         return jsonify({'message': 'Email already registered.', 'status': 'fail'}), 400
# #to do

#     # Add the new user to the mock database
#     mock_users_db[email] = password
#     print("Registration successful!")
#     return jsonify({'message': 'Registration successful!', 'status': 'success'}), 200

if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
     
=======
        return jsonify({'message': 'User already exists', 'status' : 400})

    if not password_configuration(email,password):
        return jsonify({'message': 'Password must be at least 10 characters long and include uppercase, lowercase, digits, and special characters, cant be a dictionary word', 'status': 400})

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    new_password_history = PasswordHistory(email=email)
    new_password_history.set_password(new_user.password_hash)
    db.session.add(new_password_history)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'status': 200})
#-------------------------------------------------End Register-------------------------------------------------
#-------------------------------------------------Forgot Password-------------------------------------------------
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found', 'status': 404})

    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    reset_codes[email] = reset_code
    print(f"Reset code: {reset_code}")  # Debugging statement

    try:
        response = requests.post('http://localhost:3000/api/send-code', json={'email': email, 'code': reset_code})
        print(f"Response from email service: {response.status_code}, {response.json()}")  # Debugging statement
        if response.status_code == 200 and response.json().get('success'):
            return jsonify({'message': 'Password reset code sent', 'status': 200})
        else:
            return jsonify({'message': 'Failed to send reset code', 'status': 500})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'status': 500})
#-------------------------------------------------Update Password-------------------------------------------------
@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    email = data.get('email')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    print(f"Email: {email}, Old Password: {old_password}, New Password: {new_password}")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found', 'status': 404})

    if not user.check_password(old_password):
        return jsonify({'message': 'Old password is incorrect', 'status': 400})
    if not password_configuration(email,new_password):
        return jsonify({'message': 'Password does not meet configuration requirements', 'status': 400})

    try:
        user.set_password(new_password)
        new_password_history = PasswordHistory(email=email)
        new_password_history.set_password(user.password_hash)
        db.session.add(new_password_history)
        db.session.commit()
        return jsonify({'message': 'Password updated successfully', 'status': 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}', 'status': 500})
#-------------------------------------------------End Update Password-------------------------------------------------

#---------------------------------------------------Get Customers-----------------------------------------------------
@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_list = [
        {
            'customer_name': customer.customer_name,
            'company_name': customer.company_name,
            'address': customer.address
        }
        for customer in customers
    ]
    return jsonify(customers_list)

#-------------------------------------------------End Get Customers-------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask_cors import CORS
# from .config import Config
# from .models import db, User

# app = Flask(__name__)
# app.config.from_object(Config)
# CORS(app)

# db.init_app(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # Importing routes
# from .apiRequests.forgot_password import forgot_password
# from .apiRequests.login import login
# from .apiRequests.register import register
# from .apiRequests.update_password import update_password
# from .apiRequests.verify_reset_code import verify_reset_code

# # Registering routes
# app.add_url_rule('/forgot_password', 'forgot_password', forgot_password, methods=['POST'])
# app.add_url_rule('/login', 'login', login, methods=['POST'])
# app.add_url_rule('/register', 'register', register, methods=['POST'])
# app.add_url_rule('/update_password', 'update_password', update_password, methods=['POST'])
# app.add_url_rule('/verify_reset_code', 'verify_reset_code', verify_reset_code, methods=['POST'])

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, host='127.0.0.1', port=5000)

>>>>>>> main
