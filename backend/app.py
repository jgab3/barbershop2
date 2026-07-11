from flask import Flask
from flask_cors import CORS
from extensions import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/barbershop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from services_routes import services_bp
from barber_routes import barber_bp
from customer_routes import customer_bp
from reservation_routes import reservation_bp
from schedule_routes import schedule_bp
from auth_routes import auth_bp

app.register_blueprint(services_bp)
app.register_blueprint(barber_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return 'Barbershop API is running!'

if __name__ == '__main__':
    app.run(debug=True)