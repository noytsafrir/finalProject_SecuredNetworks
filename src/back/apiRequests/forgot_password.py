from flask import request, jsonify
from ..models import db, User
import random
import string
import requests

reset_codes = {}

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
