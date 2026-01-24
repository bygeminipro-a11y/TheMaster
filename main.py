import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIG ---
API_SECRET_KEY = "MySuperSecretKey1234"

# ตัวแปรเก็บสถานะ (Global)
current_signal = {
    "symbol": "",      # <--- เพิ่มตรงนี้
    "type": "WAIT",
    "price": 0.0,
    "timestamp": 0,
    "ticket": 0
}

@app.route('/')
def home():
    return "TheMaster Server is Running (OK)."

# --- ฝั่ง Master ส่งข้อมูล (POST) ---
@app.route('/update_signal', methods=['POST'])
def update_signal():
    # 1. เช็ค Token
    token = request.args.get('token')
    if token != API_SECRET_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # 2. รับ JSON
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    # 3. อัปเดต
    global current_signal
    current_signal = {
        "symbol": data.get('symbol'), # <--- รับค่า symbol มาใส่
        "type": data.get('type'),
        "price": data.get('price'),
        "timestamp": data.get('timestamp'),
        "ticket": data.get('ticket')
    }
    
    print(f"Updated: {current_signal}")
    return jsonify({"status": "success", "data": current_signal}), 200

# --- ฝั่ง Slave ดึงข้อมูล (GET) ---
@app.route('/get_signal', methods=['GET'])
def get_signal():
    # 1. เช็ค Token (ต้องมี key ถึงจะดึงได้)
    token = request.args.get('token')
    if token != API_SECRET_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    return jsonify(current_signal), 200

if __name__ == '__main__':
    # ใช้ port จาก Env ของ Render หรือ default 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)


