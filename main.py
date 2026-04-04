from flask import Flask, request, jsonify
import redis
import os
import json

app = Flask(__name__)

# เชื่อมต่อ Redis (ตัวแปรนี้แหละที่ Server ถามหา)
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url)

# รหัสลับสำหรับตรวจสอบความปลอดภัย (ต้องตรงกับใน EA)
SECRET_KEY = "MySuperSecretKey1234"

@app.route('/')
def home():
    return "MT5 Copy Trade Server is Running!"

@app.route('/update_signal', methods=['POST'])
def update_signal():
    token = request.args.get('token')
    if token != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    if data:
        # บันทึกข้อมูลที่ Master ส่งมาลงใน Redis
        redis_client.set('latest_signal', json.dumps(data))
        return jsonify({"status": "success"}), 200
        
    return jsonify({"error": "No data"}), 400

@app.route('/get_signal', methods=['GET'])
def get_signal():
    token = request.args.get('token')
    if token != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Slave ดึงข้อมูลล่าสุดจาก Redis
        stored_data = redis_client.get('latest_signal')
        if stored_data:
            return jsonify(json.loads(stored_data)), 200
        else:
            return jsonify({"symbol": "", "type": "WAIT", "ticket": 0}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์
    app.run(host='0.0.0.0', port=10000)
