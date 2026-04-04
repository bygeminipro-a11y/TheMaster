from flask import Flask, request, jsonify

app = Flask(__name__)

# ใช้ตัวแปรเก็บข้อมูลไว้ใน RAM ของเซิร์ฟเวอร์แทน Redis
latest_signal_data = {"symbol": "", "type": "WAIT", "ticket": 0}

# รหัสลับสำหรับตรวจสอบความปลอดภัย
SECRET_KEY = "MySuperSecretKey1234"

@app.route('/')
def home():
    return "MT5 Copy Trade Server is Running Perfectly!"

@app.route('/update_signal', methods=['POST'])
def update_signal():
    global latest_signal_data
    token = request.args.get('token')
    
    if token != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    if data:
        # อัปเดตข้อมูลใหม่ลงใน RAM ทันที
        latest_signal_data = data
        return jsonify({"status": "success"}), 200
        
    return jsonify({"error": "No data"}), 400

@app.route('/get_signal', methods=['GET'])
def get_signal():
    token = request.args.get('token')
    
    if token != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # ส่งข้อมูลล่าสุดให้ Slave ทันที
    return jsonify(latest_signal_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
