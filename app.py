# backend/app.py
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) # Allows the frontend website to access this data

# Simple in-memory list to store alerts
alerts = []

@app.route('/api/alert', methods=['POST'])
def receive_alert():
    """Receives motion alert data from the SIM800L module."""
    try:
        data = request.json
        location = data.get('location', 'Unspecified Zone')
        
        new_alert = {
            'id': len(alerts) + 1,
            'location': location,
            'timestamp': datetime.now().isoformat() 
        }
        alerts.append(new_alert)
        print(f"NEW ALERT RECEIVED: {location}")
        
        return jsonify({"status": "success", "message": "Alert logged"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Provides the list of alerts to the website."""
    # Return the list of alerts, sorted by newest first
    return jsonify(sorted(alerts, key=lambda a: a['timestamp'], reverse=True)), 200

if __name__ == '__main__':
    # You must install Flask and flask-cors first (pip install Flask flask-cors)
    # The SIM800L will eventually POST data to the public IP/Domain of this server
    app.run(host='0.0.0.0', port=5000, debug=True)