class user:
    
    email = ""
    password = ""

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __str__(self):
        return f"Email: {self.email}, Password: {self.password}"