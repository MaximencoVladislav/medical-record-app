from flask import Blueprint, request, jsonify
from models import db, Patient

patient_api = Blueprint('patient_api', __name__)

@patient_api.route('/create', methods=['POST'])
def create_patient():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    gender = data.get('gender')
    phone = data.get('phone')
    address = data.get('address')

    if not all([first_name, last_name, birth_date, gender]):
        return jsonify({'error': 'Required fields missing'})

    if len(first_name) < 2 or len(first_name) > 20:
        return jsonify({'error': 'First name length must be between 2 and 20 characters'})

    if len(last_name) < 2 or len(last_name) > 20:
        return jsonify({'error': 'Last name length must be between 2 and 20 characters'})


    new_patient = Patient(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        gender=gender,
        phone=phone,
        address=address
    )

    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient created successfully'})

@patient_api.route('/list', methods=['GET'])
def list_patients():
    patients = Patient.query.all()
    patient_list = [{'id': p.id, 'first_name': p.first_name, 'last_name': p.last_name, 'birth_date': p.birth_date,
                    'gender': p.gender, 'phone': p.phone, 'address': p.address} for p in patients]
    return jsonify(patient_list)

@patient_api.route('/update/<int:id>', methods=['PUT'])
def update_patient(id):
    data = request.get_json()
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'})

    patient.first_name = data.get('first_name', patient.first_name)
    patient.last_name = data.get('last_name', patient.last_name)
    patient.birth_date = data.get('birth_date', patient.birth_date)
    patient.gender = data.get('gender', patient.gender)
    patient.phone = data.get('phone', patient.phone)
    patient.address = data.get('address', patient.address)

    db.session.commit()
    return jsonify({'message': 'Patient updated successfully'})

@patient_api.route('/delete/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'})

    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'})
