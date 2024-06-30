import hashlib, binascii, os, pyotp

user_otps = {}
OTP_INTERVAL = 300 # otp lifetime is 5 min
__totp = pyotp.TOTP("os.getenv('SECRET_KEY')", interval=OTP_INTERVAL)

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def generate_secret_key():
    return pyotp.random_base32()

def generate_otp(secret_key):
    totp = pyotp.TOTP(secret_key, interval=OTP_INTERVAL);
    return totp.now()

def verify_otp(secret_key ,otp):
    totp = pyotp.TOTP(secret_key, interval=OTP_INTERVAL);
    return totp.verify(otp)