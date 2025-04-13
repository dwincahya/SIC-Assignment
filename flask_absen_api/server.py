from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # kalau kamu akses dari luar (misal web atau ESP32)

# Ganti connection string ini sesuai MongoDB Atlas kamu
client = MongoClient("mongodb+srv://juanditoyeftapriatama:jyp120707@cluster0.rmdy1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['sekolah']
collection = db['kehadiran']

@app.route('/api/absen', methods=['POST'])
def absen():
    data = request.get_json()
    
    try:
        # Konversi waktu string ke datetime
        waktu = datetime.strptime(data["waktu"], "%Y-%m-%dT%H:%M:%SZ")
        data["waktu"] = waktu
        
        collection.insert_one(data)
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
