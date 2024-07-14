from flask import Blueprint, request, jsonify
from models import db, User, PasswordHistory
from myfunc import *

new_password_bp = Blueprint('new_password_bp', __name__)

@new_password_bp.route('/new_password', methods=['POST'])
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