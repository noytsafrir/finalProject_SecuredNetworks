import enc
from flask import Blueprint, request, jsonify
from models import OTP

verify_reset_code_bp = Blueprint('verify_reset_code_bp', __name__)

@verify_reset_code_bp.route('/verify_reset_code', methods=['POST'])
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