import os
import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit # เพิ่มตัวนี้
import redis

app = Flask(__name__)
# ตั้งค่า SocketIO (ใช้ eventlet เป็น engine หลัก)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# ... (ส่วนเชื่อมต่อ Redis เก็บไว้เหมือนเดิม) ...

@app.route('/')
def home():
    return "RemiTrade Server (WebSocket Mode) is Running."

# 1. Master ยิงสัญญาณมาที่นี่ (ผ่าน HTTP เหมือนเดิม)
@app.route('/update_signal', methods=['POST'])
def update_signal():
    token = request.args.get('token')
    if token != "MySuperSecretKey1234":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    
    # ... (บันทึกลง Redis เหมือนเดิม) ...

    # 🚨 ไฮไลท์สำคัญ: บรอดแคสต์ (Push) สัญญาณไปให้ Slave ทุกคนที่ต่อ WebSocket อยู่ทันที!
    socketio.emit('new_signal', data)
    
    print(f"Broadcasted: {data}")
    return jsonify({"status": "success"}), 200

# 2. เมื่อมี Slave ทักมาเชื่อมต่อ WebSocket
@socketio.on('connect')
def handle_connect():
    print("🟢 New Slave Connected!")
    # สามารถดึงค่าล่าสุดจาก Redis ส่งไปให้ทันทีที่ต่อติดได้ด้วย

@socketio.on('disconnect')
def handle_disconnect():
    print("🔴 Slave Disconnected")
# --- เพิ่มช่องทางให้ Slave ดึงข้อมูลผ่าน WebRequest ---
@app.route('/get_signal', methods=['GET'])
def get_signal():
    # 🚨 เพิ่มการเช็ค Token เหมือนฝั่ง Update
    token = request.args.get('token')
    secret_key = "MySuperSecretKey1234" # ควรใช้ค่าเดียวกับ Master
    
    if token != secret_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        stored_data = redis_client.get('latest_signal')
        if stored_data:
            return jsonify(json.loads(stored_data)), 200
        else:
            return jsonify({"symbol": "", "type": "WAIT", "ticket": 0}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    # เปลี่ยนจากการใช้ app.run เป็น socketio.run
    socketio.run(app, host='0.0.0.0', port=port)
