from flask import Blueprint, request, jsonify
from extensions import db
from models import Services

services_bp = Blueprint('services', __name__)

@services_bp.route('/services', methods=['GET'])
def get_services():
    services = Services.query.all()
    return jsonify([{
        'Services_Code': s.Services_Code,
        'Service_Name': s.Service_Name,
        'Price': float(s.Price)
    } for s in services])

@services_bp.route('/services', methods=['POST'])
def add_service():
    data = request.json
    new_service = Services(
        Service_Name=data['Service_Name'],
        Price=data['Price']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service added!'}), 201

@services_bp.route('/services/<int:id>', methods=['PUT'])
def update_service(id):
    service = Services.query.get_or_404(id)
    data = request.json
    service.Service_Name = data['Service_Name']
    service.Price = data['Price']
    db.session.commit()
    return jsonify({'message': 'Service updated!'})

@services_bp.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Services.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted!'})