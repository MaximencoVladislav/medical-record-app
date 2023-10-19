from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(100))

class Medical_Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    prescription = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
