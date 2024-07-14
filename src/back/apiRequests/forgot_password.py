import requests, enc
from flask import Blueprint, request, jsonify
from models import db, User, OTP

forgot_password_bp = Blueprint('forgot_password_bp', __name__)

@forgot_password_bp.route('/forgot_password', methods=['POST'])
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