from flask import Flask, request, jsonify
from models import db, Customer, User
from flask_cors import CORS
from config import Config
import re


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



# A simple dictionary to act as a mock database for users
mock_users_db = {
    'user@example.com': 'password123',
    'admin@example.com': 'adminpass'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

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


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if check_user(email):
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
     
