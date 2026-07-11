from flask import Blueprint, request, jsonify
from extensions import db
from models import Barber, Reservation, BarberSchedule

barber_bp = Blueprint('barber', __name__)

@barber_bp.route('/barbers', methods=['GET'])
def get_barbers():
    barbers = Barber.query.all()
    return jsonify([{
        'Barber_ID': b.Barber_ID,
        'Barber_Name': b.Barber_Name,
        'Contact_Number': b.Contact_Number
    } for b in barbers])

@barber_bp.route('/barbers', methods=['POST'])
def add_barber():
    data = request.json
    new_barber = Barber(
        Barber_Name=data['Barber_Name'],
        Contact_Number=data['Contact_Number']
    )
    db.session.add(new_barber)
    db.session.commit()
    return jsonify({'message': 'Barber added!'}), 201

@barber_bp.route('/barbers/<int:id>', methods=['PUT'])
def update_barber(id):
    barber = Barber.query.get_or_404(id)
    data = request.json
    barber.Barber_Name = data['Barber_Name']
    barber.Contact_Number = data['Contact_Number']
    db.session.commit()
    return jsonify({'message': 'Barber updated!'})

@barber_bp.route('/barbers/<int:id>', methods=['DELETE'])
def delete_barber(id):
    barber = Barber.query.get_or_404(id)
    reservations = Reservation.query.filter_by(Barber_ID=id).first()
    if reservations:
        return jsonify({'message': 'Cannot delete barber with existing reservations!'}), 400
    BarberSchedule.query.filter_by(Barber_ID=id).delete()
    db.session.delete(barber)
    db.session.commit()
    return jsonify({'message': 'Barber deleted!'})