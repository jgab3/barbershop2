from flask import Blueprint, request, jsonify
from extensions import db
from models import Customer

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'Customer_ID': c.Customer_ID,
        'Firstname': c.Firstname,
        'Lastname': c.Lastname,
        'Contact_Number': c.Contact_Number
    } for c in customers])

@customer_bp.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
        Firstname=data['Firstname'],
        Lastname=data['Lastname'],
        Contact_Number=data['Contact_Number']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added!'}), 201

@customer_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    customer.Firstname = data['Firstname']
    customer.Lastname = data['Lastname']
    customer.Contact_Number = data['Contact_Number']
    db.session.commit()
    return jsonify({'message': 'Customer updated!'})

@customer_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted!'})