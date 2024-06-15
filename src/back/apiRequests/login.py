from flask import request, jsonify
from flask_login import login_user
from ..models import User

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})

    if user.check_password(password):
        # login_user(user)
        return jsonify({'message': 'Login successful!', 'status': 200})
    else:
        return jsonify({'message': 'Invalid password.', 'status': 401})
    

#from the main
# @app.route('/update_password', methods=['POST'])
# def update_password():
#     data = request.get_json()
#     email = data.get('email')
#     old_password = data.get('oldPassword')
#     new_password = data.get('newPassword')

#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({'message': 'User not found', 'status': 404}), 404

#     if not user.check_password(old_password):
#         user.login_attempts += 1
#         db.session.commit()
#         if user.login_attempts >= Config.LOGIN_ATTEMPTS_LIMIT:
#             return jsonify({'message': 'Too many login attempts. Account locked.', 'status': 403}), 403
#         return jsonify({'message': 'Old password is incorrect', 'status': 400}), 400

#     if not is_password_complex(new_password):
#         return jsonify({'message': 'Password must be at least 10 characters long and include uppercase, lowercase, digits, and special characters', 'status': 400}), 400

#     if is_dictionary_word(new_password):
#         return jsonify({'message': 'Password cannot be a dictionary word', 'status': 400}), 400

#     if any(check_password_hash(pwd, new_password) for pwd in user.old_passwords):
#         return jsonify({'message': 'Password has been used recently. Please choose a different password.', 'status': 400}), 400

#     user.set_password(new_password)
#     user.login_attempts = 0
#     db.session.commit()

#     return jsonify({'message': 'Password updated successfully', 'status': 200}), 200
