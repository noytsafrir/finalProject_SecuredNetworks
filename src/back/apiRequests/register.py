from flask import request, jsonify
from ..models import db, User
from ..validator import password_configuration

def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    if not password_configuration(password):
        return jsonify({'message': 'Password is WEAK AF! --> get better :L', 'status': 400})  # TODO change message

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'status': 200})

