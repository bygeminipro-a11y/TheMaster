from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIG ---
# รหัสลับสำหรับ Master และ Slave ต้องตรงกัน
API_SECRET_KEY = "MySuperSecretKey1234"

# ตัวแปรเก็บสถานะล่าสุด (เริ่มมาเป็นสถานะรอ)
current_signal = {
    "type": "WAIT",
    "price": 0.0,
    "timestamp": 0,
    "ticket": 0
}

@app.route('/')
def home():
    return "RemiTrade Server is Running..."

# --- ฝั่ง Master ส่งข้อมูลมา (POST) ---
@app.route('/update_signal', methods=['POST'])
def update_signal():
    # 1. เช็ค Token ว่าตรงไหม
    token = request.args.get('token')
    if token != API_SECRET_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # 2. รับข้อมูล JSON
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    # 3. อัปเดตข้อมูล
    global current_signal
    current_signal = {
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
    # 1. เพิ่มบรรทัดเช็ค Token (เหมือน update_signal)
    token = request.args.get('token')
    
    # ถ้า Token ไม่ตรงกับรหัสลับ ให้ดีดออก
    if token != API_SECRET_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # ถ้าผ่าน ให้ส่งข้อมูลได้
    return jsonify(current_signal), 200
