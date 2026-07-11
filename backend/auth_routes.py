from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    firstname = (data.get('Firstname') or '').strip()
    lastname = (data.get('Lastname') or '').strip()
    email = (data.get('Email') or '').strip().lower()
    password = data.get('Password') or ''

    # Required field validation
    if not firstname or not lastname or not email or not password:
        return jsonify({'message': 'All fields are required.'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'message': 'Please enter a valid email address.'}), 400

    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters.'}), 400

    # DB check: email must not already be registered
    existing_user = User.query.filter_by(Email=email).first()
    if existing_user:
        return jsonify({'message': 'An account with that email already exists.'}), 409

    new_user = User(
        Firstname=firstname,
        Lastname=lastname,
        Email=email,
        Password_Hash=generate_password_hash(password),
        Role='customer'
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully! You can now log in.'}), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get('Email') or '').strip().lower()
    password = data.get('Password') or ''

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    # DB check: look up the user record by email
    user = User.query.filter_by(Email=email).first()

    if not user or not check_password_hash(user.Password_Hash, password):
        return jsonify({'message': 'Invalid email or password.'}), 401

    return jsonify({
        'message': 'Login successful!',
        'user': {
            'User_ID': user.User_ID,
            'Firstname': user.Firstname,
            'Lastname': user.Lastname,
            'Email': user.Email,
            'Role': user.Role
        }
    }), 200
