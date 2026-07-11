from flask import Blueprint, request, jsonify
from extensions import db
from models import BarberSchedule

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/barbers/<int:barber_id>/schedules', methods=['GET'])
def get_schedules(barber_id):
    schedules = BarberSchedule.query.filter_by(Barber_ID=barber_id).all()
    return jsonify([{
        'Schedule_ID': s.Schedule_ID,
        'Barber_ID': s.Barber_ID,
        'Day': s.Day,
        'Start_Time': str(s.Start_Time),
        'End_Time': str(s.End_Time)
    } for s in schedules])

@schedule_bp.route('/barbers/<int:barber_id>/schedules', methods=['POST'])
def add_schedule(barber_id):
    data = request.json
    new_schedule = BarberSchedule(
        Barber_ID=barber_id,
        Day=data['Day'],
        Start_Time=data['Start_Time'],
        End_Time=data['End_Time']
    )
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule added!'}), 201

@schedule_bp.route('/schedules/<int:id>', methods=['PUT'])
def update_schedule(id):
    schedule = BarberSchedule.query.get_or_404(id)
    data = request.json
    schedule.Day = data['Day']
    schedule.Start_Time = data['Start_Time']
    schedule.End_Time = data['End_Time']
    db.session.commit()
    return jsonify({'message': 'Schedule updated!'})

@schedule_bp.route('/schedules/<int:id>', methods=['DELETE'])
def delete_schedule(id):
    schedule = BarberSchedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule deleted!'})