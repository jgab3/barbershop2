from flask import Blueprint, request, jsonify
from extensions import db
from models import Reservation, Customer, Barber

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    result = []
    for r in reservations:
        customer = Customer.query.get(r.Customer_ID)
        barber = Barber.query.get(r.Barber_ID)
        result.append({
            'Reservation_ID': r.Reservation_ID,
            'Customer_ID': r.Customer_ID,
            'Barber_ID': r.Barber_ID,
            'Customer_Name': f'{customer.Firstname} {customer.Lastname}',
            'Barber_Name': barber.Barber_Name,
            'Date': str(r.Date),
            'Time': str(r.Time),
            'Status': r.Status,
            'DP_Amount': float(r.DP_Amount),
            'DP_Status': r.DP_Status
        })
    return jsonify(result)

@reservation_bp.route('/reservations', methods=['POST'])
def add_reservation():
    data = request.json
    existing = Reservation.query.filter_by(
        Barber_ID=data['Barber_ID'],
        Date=data['Date'],
        Time=data['Time']
    ).first()
    if existing:
        return jsonify({'message': 'Barber is already booked at this date and time!'}), 400
    new_reservation = Reservation(
        Customer_ID=data['Customer_ID'],
        Barber_ID=data['Barber_ID'],
        Date=data['Date'],
        Time=data['Time'],
        Status=data.get('Status', 'Pending'),
        DP_Amount=data['DP_Amount'],
        DP_Status=data.get('DP_Status', None)
    )
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation added!'}), 201

@reservation_bp.route('/reservations/<int:id>', methods=['PUT'])
def update_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    data = request.json
    reservation.Customer_ID = data['Customer_ID']
    reservation.Barber_ID = data['Barber_ID']
    reservation.Date = data['Date']
    reservation.Time = data['Time']
    reservation.Status = data['Status']
    reservation.DP_Amount = data['DP_Amount']
    db.session.commit()
    return jsonify({'message': 'Reservation updated!'})

@reservation_bp.route('/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation deleted!'})