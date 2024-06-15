from flask import Flask, request, jsonify
from models import db, Customer, User
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask_cors import CORS
from config import Config
from validator import *
import re
import random
import string
import requests

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

reset_codes = {}

mock_users_db = {
    'user@example.com': 'password123',
    'admin@example.com': 'adminpass'
}



def check_user(email):
    user = User.query.filter_by(email=email).first()
    return user is not None

def check_password(user, password):
    return user.check_password(password)

#updated in the validator.py
def password_configuration(password):
    return len(password) >= 10



@app.route('/new_password', methods=['POST'])
def new_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found', 'status': 404})

    if not password_configuration(new_password):
        return jsonify({'message': 'Password does not meet configuration requirements', 'status': 400})

    user.set_password(new_password)
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
    return jsonify({'message': 'Customer added successfully', 'status': 200})

@app.route('/verify_reset_code', methods=['POST'])
def verify_reset_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if reset_codes.get(email) == code:
        return jsonify({'message': 'Code verified', 'status': 200}), 200
    else:
        return jsonify({'message': 'Invalid code or expired', 'status': 400}), 400
#-------------------------------------------------Login-------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})

    if user.check_password(password):
        return jsonify({'message': 'Login successful!', 'status': 200})
    else:
        return jsonify({'message': 'Invalid password.', 'status': 401})
#-------------------------------------------------End Login-------------------------------------------------
#-------------------------------------------------Register-------------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if check_user(email):
        return jsonify({'message': 'User already exists'}), 400

    if not password_configuration(password):
        return jsonify({'message': 'Password is WEAK AF! --> get better :L', 'status': 400})  # TODO change message

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
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
        return jsonify({'message': 'User not found', 'status': 404}), 404

    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    reset_codes[email] = reset_code

    try:
        response = requests.post('http://localhost:3000/api/send-code', json={'email': email, 'code': reset_code})
        if response.status_code == 200 and response.json().get('success'):
            return jsonify({'message': 'Password reset code sent', 'status': 200}), 200
        else:
            return jsonify({'message': 'Failed to send reset code', 'status': 500}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'status': 500}), 500

#-------------------------------------------------End Forgot Password-------------------------------------------------
#-------------------------------------------------Update Password-------------------------------------------------
@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    email = data.get('email')
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found', 'status': 404}), 404

    if not user.check_password(old_password):
        user.login_attempts += 1
        db.session.commit()
        if user.login_attempts >= Config.LOGIN_ATTEMPTS_LIMIT:
            return jsonify({'message': 'Too many login attempts. Account locked.', 'status': 403}), 403
        return jsonify({'message': 'Old password is incorrect', 'status': 400}), 400

    if not is_password_complex(new_password):
        return jsonify({'message': 'Password must be at least 10 characters long and include uppercase, lowercase, digits, and special characters', 'status': 400}), 400

    if is_dictionary_word(new_password):
        return jsonify({'message': 'Password cannot be a dictionary word', 'status': 400}), 400

    if any(check_password_hash(pwd, new_password) for pwd in user.old_passwords):
        return jsonify({'message': 'Password has been used recently. Please choose a different password.', 'status': 400}), 400

    user.set_password(new_password)
    user.login_attempts = 0
    db.session.commit()

    return jsonify({'message': 'Password updated successfully', 'status': 200}), 200
#-------------------------------------------------End Update Password-------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)

