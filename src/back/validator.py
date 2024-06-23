import re
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256
from models import PasswordHistory
# pip install Werkzeug


def is_password_complex(password):
    if len(password) < Config.PASSWORD_LENGTH:
        return False
    if Config.CONTAIN_UPPERCASE and not re.search(r'[A-Z]', password):
        return False
    if Config.CONTAIN_LOWERCASE and not re.search(r'[a-z]', password):
        return False
    if Config.CONTAIN_NUMERIC and not re.search(r'[0-9]', password):
        return False
    if Config.CONTAIN_SPECIAL and not re.search(r'[@$!%*?&#]', password):
        return False
    return True


def is_dictionary_word(password):
    for word in Config.DICTIONARY_WORDS:
        if word.lower() in password.lower():
            return True
    return False


def is_password_new(email, password):
    num_passwords = Config.LAST_PASSWORDS_COUNT
    if not email or not num_passwords:
        return False

    password_history = PasswordHistory.query.filter_by(email=email).order_by(PasswordHistory.timestamp.desc()).limit(num_passwords).all()
    history_list = [
        record.password_hash
        for record in password_history
    ]
    for password_record in history_list:
        if(pbkdf2_sha256.verify(password, password_record)):
            return False
    return True
