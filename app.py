from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from Blockchain import blockchain
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dummy validator login credentials (username: validator1, password: password123)
validators = {
    "validator1": "password123",
    "validator2": "admin456",
    "validator3": "password003"
}

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get("username")
        password = data.get("password")
        if username in validators and validators[username] == password:
            session['logged_in'] = True
            session['validator'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('validator', None)
    return redirect(url_for('login'))

@app.route('/add_imei', methods=['POST'])
def add_imei():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized. Please log in."}), 403

    data = request.get_json()
    imei = data.get("imei")
    status = data.get("status")
    region = data.get("region")
    operator = data.get("operator")
    validator = session.get("validator")

    if not imei or not status or not region or not operator:
        return jsonify({"error": "IMEI, status, region, and operator are required"}), 400

    if blockchain.add_device(imei, status, region, operator, validator):
        return jsonify({"message": f"IMEI {imei} added successfully!"}), 200
    else:
        return jsonify({"error": "IMEI already exists"}), 400

@app.route('/search_imei', methods=['GET'])
def search_imei():
    imei = request.args.get('imei')
    if not imei:
        return jsonify({"message": "IMEI number is required"}), 400

    for block in blockchain.chain:
        if imei in block["devices"]:
            device_info = block["devices"][imei]
            return jsonify({
                "imei": imei,
                "status": device_info,
                "region": block.get("region", "N/A"),
                "operator": block.get("operator", "N/A"),
                "validator": block.get("validator", "N/A")
            }), 200
    return jsonify({"message": "IMEI not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
