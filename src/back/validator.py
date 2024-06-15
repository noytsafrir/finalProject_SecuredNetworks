
# #TODO: implement the validator functions

# def userExists(username):
#     """
#     Check if a user exists in the database
#     """
#     # user = User.query.filter_by(username=username).first()
#     # if user is None:
#     #     return False
#     return True

# def validateEmail(email):
#     """
#     Validate the email
#     """
#     # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#     #     return False
#     return True

# def validatePassword(password):
#     """
#     Validate the password by the configuration of the password
#     """
#     # if len(password) < 10:
#     #     return False
#     return True

import re
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
# pip install Werkzeug

#TODO: implement the validator functions

def userExists(username):
    """
    Check if a user exists in the database
    """
    # user = User.query.filter_by(username=username).first()
    # if user is None:
    #     return False
    return True

def validateEmail(email):
    """
    Validate the email
    """
    # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #     return False
    return True

def validatePassword(password):
    """
    Validate the password by the configuration of the password
    """
    # if len(password) < 10:
    #     return False
    return True


def is_password_complex(password):
    if len(password) < Config.PASSWORD_LENGTH:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[@$!%*?&#]', password):
        return False
    return True


def is_dictionary_word(password):
    return password.lower() in Config.DICTIONARY_WORDS