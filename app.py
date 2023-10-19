from flask import Flask, render_template, request, jsonify
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'medical_record_db'

db = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return "This is a POST request response"

@app.route('/patient', methods=['GET', 'POST'])
@app.route('/patient/<int:patient_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def patient(patient_id=None):
    cursor = db.cursor()
    
    if request.method == 'GET':
        if patient_id is not None:
            cursor.execute("SELECT * FROM `patient` WHERE ID = %s", (patient_id,))
            result = cursor.fetchone()
            return jsonify(result) if result else ('Patient not found', 404)
        else:
            cursor.execute("SELECT * FROM `patient`")
            result = cursor.fetchall()
            return jsonify(result)

    if request.method == 'POST':
        data = request.json 
        cursor.execute("INSERT INTO `patient` (First_name, Last_name, Birth_date, Gender, Phone, Address) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (data['First_name'], data['Last_name'], data['Birth_date'], data['Gender'], data['Phone'], data['Address']))
        db.commit()
        return "Data inserted into patient successfully", 201

    if request.method == 'PUT':
        if patient_id is not None:
            data = request.json
            cursor.execute("UPDATE `patient` SET First_name = %s, Last_name = %s, Birth_date = %s, Gender = %s, Phone = %s, Address = %s WHERE ID = %s",
                           (data['First_name'], data['Last_name'], data['Birth_date'], data['Gender'], data['Phone'], data['Address'], patient_id))
            db.commit()
            return "Patient information updated successfully"
        else:
            return "Patient ID is required for updating", 400

    if request.method == 'PATCH':
        if patient_id is not None:
            data = request.json 
            update_query = "UPDATE `patient` SET "
            update_params = []
            
            for key, value in data.items():
                update_query += f"{key} = %s, "
                update_params.append(value)

            update_query = update_query[:-2]
            
            update_query += f" WHERE ID = %s"
            update_params.append(patient_id)
            
            cursor.execute(update_query, update_params)
            db.commit()
            return "Patient information updated successfully"
        else:
            return "Patient ID is required for updating", 400

    if request.method == 'DELETE':
        if patient_id is not None:
            cursor.execute("DELETE FROM `patient` WHERE ID = %s", (patient_id,))
            db.commit()
            return "Patient deleted successfully"
        else:
            return "Patient ID is required for deletion", 400
        
@app.route('/medicalrecord', methods=['GET', 'POST'])
@app.route('/medicalrecord/<int:record_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def medical_record(record_id=None):
    cursor = db.cursor()

    if request.method == 'GET':
        if record_id is not None:
            cursor.execute("SELECT * FROM `medicalrecord` WHERE ID = %s", (record_id,))
            result = cursor.fetchone()
            return jsonify(result) if result else ('Medical record not found', 404)
        else:
            cursor.execute("SELECT * FROM `medicalrecord`")
            result = cursor.fetchall()
            return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO `medicalrecord` (Patient_id, Visit_date, Diagnosis, Prescription, Created_by) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       (data['Patient_id'], data['Visit_date'], data['Diagnosis'], data['Prescription'], data['Created_by']))
        db.commit()
        return "Data inserted into medical record successfully", 201

    if request.method == 'PUT':
        if record_id is not None:
            data = request.json
            cursor.execute("UPDATE `medicalrecord` SET Patient_id = %s, Visit_date = %s, Diagnosis = %s, Prescription = %s, Created_by = %s WHERE ID = %s",
                           (data['Patient_id'], data['Visit_date'], data['Diagnosis'], data['Prescription'], data['Created_by'], record_id))
            db.commit()
            return "Medical record information updated successfully"
        else:
            return "Medical record ID is required for updating", 400

    if request.method == 'PATCH':
        if record_id is not None:
            data = request.json 
            update_query = "UPDATE `medicalrecord` SET "
            update_params = []

            for key, value in data.items():
                update_query += f"{key} = %s, "
                update_params.append(value)
            update_query = update_query[:-2]

            update_query += f" WHERE ID = %s"
            update_params.append(record_id)

            cursor.execute(update_query, update_params)
            db.commit()
            return "Medical record information updated successfully"
        else:
            return "Medical record ID is required for updating", 400

    if request.method == 'DELETE':
        if record_id is not None:
            cursor.execute("DELETE FROM `medicalrecord` WHERE ID = %s", (record_id,))
            db.commit()
            return "Medical record deleted successfully"
        else:
            return "Medical record ID is required for deletion", 400

if __name__ == '__main__':
    app.run()
