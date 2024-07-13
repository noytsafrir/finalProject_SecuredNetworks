
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from apiRequests.add_customer import add_customer_bp
from apiRequests.forgot_password import forgot_password_bp
from apiRequests.get_customers import get_customers_bp
from apiRequests.login import login_bp
from apiRequests.new_password import new_password_bp
from apiRequests.register import register_bp
from apiRequests.update_password import update_password_bp
from apiRequests.verify_reset_code import verify_reset_code_bp


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)



# Register blueprints
app.register_blueprint(add_customer_bp)
app.register_blueprint(forgot_password_bp)
app.register_blueprint(get_customers_bp)
app.register_blueprint(login_bp)
app.register_blueprint(new_password_bp)
app.register_blueprint(register_bp)
app.register_blueprint(update_password_bp)
app.register_blueprint(verify_reset_code_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
