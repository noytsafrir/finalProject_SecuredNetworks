from flask import Flask, request, jsonify
from models import db, Customer, User, PasswordHistory, OTP
from flask_cors import CORS
from config import Config
from validator import *
import re, random, string, requests, enc
from sqlalchemy import text
import os
from dotenv import load_dotenv
import mysql.connector

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
load_dotenv()
safe_mode = os.getenv('SAFE_MODE') == 'true'

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

def set_unsecured_connection():
    # Database connection setup
    unsecuredConnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='A123456',
        database='store'
    )
    unsecuredCursor = unsecuredConnection.cursor()
    return unsecuredConnection, unsecuredCursor

def close_unsecured_connection(cursor, connection):
    connection.commit()
    cursor.close()
    connection.close()
#-------------------------------------------------New Password-------------------------------------------------
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
    new_password_history = PasswordHistory(email=email, password_hash=user.password_hash)
    db.session.add(new_password_history)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully', 'status': 200})
#-------------------------------------------------End New Password-------------------------------------------------
#-------------------------------------------------Add Customer-------------------------------------------------
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer_name = data.get('customer_name')
    company_name = data.get('company_name')
    address = data.get('address')

    # safe mode
    if safe_mode:
        existing_customer = Customer.query.filter_by(customer_name=customer_name).first()
        if existing_customer is not None:
            return jsonify({'message': 'Customer already exists', 'status': 400})

    # unsafe mode
    else:
        try:
            # Database connection setup
            unsecuredConnection, unsecuredCursor = set_unsecured_connection()
            # Constructing a single query that includes a potential SQL injection
            query = f"SELECT * FROM customers WHERE customer_name = '{customer_name}';"
            print(query)    # Debugging statement
            # Executing the query with multi=True to allow multiple statements
            for result in unsecuredCursor.execute(query, multi=True):
                if result.with_rows:
                    res = result.fetchall()
                    if res:
                        close_unsecured_connection(unsecuredCursor, unsecuredConnection)
                        return jsonify({'message': 'Customer already exists', 'status': 400})
            close_unsecured_connection(unsecuredCursor, unsecuredConnection)
        except mysql.connector.ProgrammingError as e:
            print(f"Error: {e}")
            return jsonify({'message': 'SQL error', 'status': 500})
        
    # safe mode & unsafe mode
    # Add the new customer
    new_customer = Customer(customer_name=customer_name, company_name=company_name, address=address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'New Customer was added successfully:', 'status': 200})
#-------------------------------------------------End Add Customer-------------------------------------------------
#-------------------------------------------------Login-------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = None
    if safe_mode:
        user = User.query.filter_by(email=email).first()
    else:
        try:
            # Database connection setup
            unsecuredConnection, unsecuredCursor = set_unsecured_connection()
            # Constructing a single query that includes a potential SQL injection
            query = f"SELECT * FROM users WHERE email = '{email}'"
            print(query)    # Debugging statement
            # Executing the query with multi=True to allow multiple statements
            for result in unsecuredCursor.execute(query, multi=True):
                if result.with_rows:
                    res = result.fetchone()
                    if res:
                        user = User(email=res[0], password_hash=res[1], login_attempts=res[2])
            close_unsecured_connection(unsecuredCursor, unsecuredConnection)
        except mysql.connector.ProgrammingError as e:
            print(f"Error: {e}")
            return jsonify({'message': 'SQL error', 'status': 500})
    
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})
    if user.login_attempts < Config.LOGIN_ATTEMPTS_LIMIT: 
        if user.check_password(password):
            user.reset_login_attempts()
            return jsonify({'message': 'Login successful!', 'status': 200, 'user_email': user.email})
        else:
            user.increment_login_attempts()
            return jsonify({'message': 'Invalid password.', 'status': 401})
    else:
        return jsonify({'message': 'Account locked.', 'status': 401})
#-------------------------------------------------End Login-------------------------------------------------
#-------------------------------------------------Register-------------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # safe mode
    if safe_mode:
        if check_user(email):
            return jsonify({'message': 'User already exists', 'status' : 400})
    # unsafe mode
    else:  
        try:
            # Database connection setup
            unsecuredConnection, unsecuredCursor = set_unsecured_connection()
            # Constructing a single query that includes a potential SQL injection
            query = f"SELECT * FROM users WHERE email = '{email}';"
            # Executing the query with multi=True to allow multiple statements
            for result in unsecuredCursor.execute(query, multi=True):
                if result.with_rows:
                    res = result.fetchall()
                    if res:
                        close_unsecured_connection(unsecuredCursor, unsecuredConnection)
                        return jsonify({'message': 'User already exists', 'status': 400})
            close_unsecured_connection(unsecuredCursor, unsecuredConnection)
        except mysql.connector.ProgrammingError as e:
            print(f"Error: {e}")
            return jsonify({'message': 'SQL error', 'status': 500})

    # safe mode    
    if not password_configuration(email,password):
        return jsonify({'message': 'Password must be at least 10 characters long and include uppercase, lowercase, digits, and special characters, cant be a dictionary word', 'status': 400})

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    new_password_history = PasswordHistory(email=email, password_hash=new_user.password_hash)
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
    if user == None:
        return jsonify({'message': 'User not found', 'status': 404})
    user_otp = OTP.query.filter_by(email=email).first()
    if user_otp is None:
        user_otp = OTP(email=email, secret_key=enc.generate_secret_key())
        db.session.add(user_otp)
    else:
        user_otp.secret_key = enc.generate_secret_key()
    db.session.commit()
    otp = enc.generate_otp(user_otp.secret_key)
    print(f"### OTP for {email}: {otp}") # TODO Debugging statement

    try:
        response = requests.post('http://localhost:3000/api/send-code', json={'email': email, 'code': otp})
        print(f"Response from email service: {response.status_code}, {response.json()}")  # Debugging statement
        if response.status_code == 200 and response.json().get('success'):
            return jsonify({'message': 'Password reset code sent', 'status': 200})
        else:
            return jsonify({'message': 'Failed to send reset code', 'status': 500})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'status': 500})
#-------------------------------------------------End Forgot Password-------------------------------------------------
#-------------------------------------------------Verify Reset Code-------------------------------------------------
@app.route('/verify_reset_code', methods=['POST'])
def verify_reset_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    user_otp = OTP.query.filter_by(email=email).first()
    if user_otp is None:
        return jsonify({'message': 'User not found', 'status': 404})
    secret_key = user_otp.secret_key
    if enc.verify_otp(secret_key, code):
        return jsonify({'message': 'Code verified', 'status': 200})
    else:
        return jsonify({'message': 'Invalid code or expired', 'status': 400})
#-------------------------------------------------End Verify Reset Code-------------------------------------------------
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
        new_password_history = PasswordHistory(email=email, password_hash=user.password_hash)
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
    search_field = request.args.get('searchField')
    search_type = request.args.get('searchType')
    search_data = request.args.get('searchData')

    if safe_mode:
        query = Customer.query
        if search_field and search_type and search_data:
            if search_type == 'contains':
                query = query.filter(getattr(Customer, search_field).like(f'%{search_data}%'))
            elif search_type == 'equals':
                query = query.filter(getattr(Customer, search_field) == search_data)
        result = query.all()
        customers = [
            {
                'customer_name': customer.customer_name,
                'company_name': customer.company_name,
                'address': customer.address
            }
            for customer in result
        ]
    else:
        if not search_field or not search_type or not search_data:
            query = text("SELECT customer_name, company_name, address FROM customers")
            print(query)    # Debugging statement
            result = db.session.execute(query)
        else:
            if search_type == 'contains':
                query = text(f"SELECT customer_name, company_name, address FROM customers WHERE {search_field} LIKE '%{search_data}%'")
                print(query)    # Debugging statement
                result = db.session.execute(query)
            elif search_type == 'equals':
                query = text(f"SELECT customer_name, company_name, address FROM customers WHERE {search_field} = '{search_data}'")
                print(query)    # Debugging statement
                result = db.session.execute(query)
        customers = [
            {
                'customer_name': row[0],
                'company_name': row[1],
                'address': row[2]
            }
            for row in result
        ]
    print(query) # Debugging statement
  
    return jsonify(customers)

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

