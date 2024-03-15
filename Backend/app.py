from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="invoice_db",
)

# Sample data for invoice and clients
# For simplicity, we will directly query the database

# Routes for managing invoice
@app.route('/invoice', methods=['GET'])
def get_invoices():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM invoice")
    invoice = cursor.fetchall()
    return jsonify(invoice)

@app.route('/invoice', methods=['POST'])
def create_invoice():
    data = request.json
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO invoice (client_id, date, total_amount, status) VALUES (%s, %s, %s, %s)", (data['client_id'], data['date'], data['total_amount'], data['status']))
    mydb.commit()
    return jsonify(data), 201

@app.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM invoice WHERE id = %s", (invoice_id,))
    invoice = cursor.fetchone()
    if invoice:
        return jsonify(invoice)
    else:
        return jsonify({'message': 'Invoice not found'}), 404

@app.route('/invoice/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    data = request.json
    cursor = mydb.cursor()
    cursor.execute("UPDATE invoice SET client_id = %s, date = %s, total_amount = %s, status = %s WHERE id = %s", (data['client_id'], data['date'], data['total_amount'], data['status'], invoice_id))
    mydb.commit()
    return jsonify(data)

@app.route('/invoice/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM invoice WHERE id = %s", (invoice_id,))
    mydb.commit()
    return jsonify({'message': 'Invoice deleted'})

# Routes for managing clients
@app.route('/clients', methods=['GET'])
def get_clients():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO clients (name, contact, billing_address) VALUES (%s, %s, %s)", (data['name'], data['contact'], data['billing_address']))
    mydb.commit()
    return jsonify(data), 201

@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
    client = cursor.fetchone()
    if client:
        return jsonify(client)
    else:
        return jsonify({'message': 'Client not found'}), 404

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.json
    cursor = mydb.cursor()
    cursor.execute("UPDATE clients SET name = %s, contact = %s, billing_address = %s WHERE id = %s", (data['name'], data['contact'], data['billing_address'], client_id))
    mydb.commit()
    return jsonify(data)

@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
    mydb.commit()
    return jsonify({'message': 'Client deleted'})

if __name__ == '__main__':
    app.run(debug=True)
