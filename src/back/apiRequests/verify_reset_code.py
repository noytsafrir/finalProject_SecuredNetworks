from flask import request, jsonify

reset_codes = {}  # This should be a shared state if used in multiple modules

def verify_reset_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if reset_codes.get(email) == code:
        return jsonify({'message': 'Code verified', 'status': 200}), 200
    else:
        return jsonify({'message': 'Invalid code or expired', 'status': 400}), 400
