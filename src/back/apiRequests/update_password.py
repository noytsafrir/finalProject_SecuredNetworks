from flask import Blueprint, request, jsonify
from models import db, User, PasswordHistory
from myfunc import *

update_password_bp = Blueprint('update_password_bp', __name__)

@update_password_bp.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    email = data.get('email')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

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