from flask import request, jsonify
from flask_login import login_required, current_user
from ..models import db
from ..validator import is_password_complex, is_dictionary_word

@login_required
def update_password():
    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    user = current_user
    if not user.check_password(old_password):
        user.login_attempts += 1
        db.session.commit()
        if user.login_attempts >= 3:  # limit
            return jsonify({'message': 'Too many login attempts. Account locked.', 'status': 403}), 403
        return jsonify({'message': 'Old password is incorrect', 'status': 400}), 400

    if not is_password_complex(new_password):
        return jsonify({'message': 'Password must be at least 10 characters long and include uppercase, lowercase, digits, and special characters', 'status': 400}), 400

    if is_dictionary_word(new_password):
        return jsonify({'message': 'Password cannot be a dictionary word', 'status': 400}), 400

    if any(user.check_password(pwd) for pwd in user.old_passwords):
        return jsonify({'message': 'Password has been used recently. Please choose a different password.', 'status': 400}), 400

    user.set_password(new_password)
    user.login_attempts = 0
    db.session.commit()

    return jsonify({'message': 'Password updated successfully', 'status': 200})
