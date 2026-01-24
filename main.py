import os
import json
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# --- CONFIG ---
API_SECRET_KEY = "MySuperSecretKey1234" # แก้เป็นรหัสของคุณ
REDIS_URL = os.environ.get('REDIS_URL')

# เชื่อมต่อ Redis
r = None
if REDIS_URL:
    try:
        r = redis.from_url(REDIS_URL)
        print("✅ Connected to Redis")
    except Exception as e:
        print(f"⚠️ Redis Connection Error: {e}")

# ตัวแปรสำรอง (กรณีไม่มี Redis)
memory_signal = {
    "symbol": "",
    "type": "WAIT",
    "price": 0.0,
    "timestamp": 0,
    "ticket": 0
}

@app.route('/')
def home():
    return "The Master Trade is Running"

@app.route('/update_signal', methods=['POST'])
def update_signal():
    token = request.args.get('token')
    if token != API_SECRET_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json
    new_signal = {
        "symbol": data.get('symbol'),
        "type": data.get('type'),
        "price": data.get('price'),
        "timestamp": data.get('timestamp'),
        "ticket": data.get('ticket')
    }

    # เก็บลง Redis (หรือตัวแปรสำรอง)
    if r:
        r.set('current_signal', json.dumps(new_signal))
    else:
        global memory_signal
        memory_signal = new_signal
    
    print(f"Updated: {new_signal}")
    return jsonify({"status": "success", "data": new_signal}), 200

@app.route('/get_signal', methods=['GET'])
def get_signal():
    token = request.args.get('token')
    if token != API_SECRET_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # ดึงจาก Redis
    current_data = None
    if r:
        raw_data = r.get('current_signal')
        if raw_data:
            current_data = json.loads(raw_data)
    
    # ถ้า Redis ไม่มีข้อมูล หรือพัง ให้ใช้ตัวแปรสำรอง
    if not current_data:
        global memory_signal
        current_data = memory_signal

    return jsonify(current_data), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

