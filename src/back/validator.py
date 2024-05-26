
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