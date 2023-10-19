from flask import Blueprint, request, jsonify
from models import db, Medical_Record

medical_record_api = Blueprint('medical_record_api', __name__)

@medical_record_api.route('/create', methods=['POST'])
def create_medical_record():
    data = request.get_json()
    patient_id = data.get('patient_id')
    visit_date = data.get('visit_date')
    diagnosis = data.get('diagnosis')
    prescription = data.get('prescription')
    created_at = data.get('created_at')
    created_by = data.get('created_by')

    if not all([patient_id, visit_date, diagnosis, created_at, created_by]):
        return jsonify({'error': 'Required fields missing'})

    if len(diagnosis) < 5 or len(diagnosis) > 100:
        return jsonify({'error': 'Diagnosis length must be between 5 and 100 characters'})

    new_medical_record = MedicalRecord(
        patient_id=patient_id,
        visit_date=visit_date,
        diagnosis=diagnosis,
        prescription=prescription,
        created_at=created_at,
        created_by=created_by
    )

    db.session.add(new_medical_record)
    db.session.commit()
    return jsonify({'message': 'Medical record created successfully'})

@medical_record_api.route('/list', methods=['GET'])
def list_medical_records():
    medical_records = MedicalRecord.query.all()
    medical_record_list = [{'id': mr.id, 'patient_id': mr.patient_id, 'visit_date': mr.visit_date,
                           'diagnosis': mr.diagnosis, 'prescription': mr.prescription,
                           'created_at': mr.created_at, 'created_by': mr.created_by} for mr in medical_records]
    return jsonify(medical_record_list)

@medical_record_api.route('/update/<int:id>', methods=['PUT'])
def update_medical_record(id):
    data = request.get_json()
    medical_record = MedicalRecord.query.get(id)
    if not medical_record:
        return jsonify({'error': 'Medical record not found'})

    medical_record.patient_id = data.get('patient_id', medical_record.patient_id)
    medical_record.visit_date = data.get('visit_date', medical_record.visit_date)
    medical_record.diagnosis = data.get('diagnosis', medical_record.diagnosis)
    medical_record.prescription = data.get('prescription', medical_record.prescription)
    medical_record.created_at = data.get('created_at', medical_record.created_at)
    medical_record.created_by = data.get('created_by', medical_record.created_by)

    db.session.commit()
    return jsonify({'message': 'Medical record updated successfully'})

@medical_record_api.route('/delete/<int:id>', methods=['DELETE'])
def delete_medical_record(id):
    medical_record = MedicalRecord.query.get(id)
    if not medical_record:
        return jsonify({'error': 'Medical record not found'})

    db.session.delete(medical_record)
    db.session.commit()
    return jsonify({'message': 'Medical record deleted successfully'})
