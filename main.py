from flask import Flask, request, jsonify

app = Flask(__name__)

# เก็บรายชื่อออเดอร์ทั้งหมดไว้ในหน่วยความจำ
current_master_list = "EMPTY"
SECRET_KEY = "MySuperSecretKey1234"

@app.route('/')
def home():
    return "."

@app.route('/update_list', methods=['POST'])
def update_list():
    global current_master_list
    token = request.args.get('token')
    if token != SECRET_KEY:
        return jsonify({"status": "unauthorized"}), 401
    
    data = request.json
    current_master_list = data.get('master_list', "EMPTY")
    return jsonify({"status": "updated"}), 200

@app.route('/get_signal', methods=['GET'])
def get_signal():
    token = request.args.get('token')
    if token != SECRET_KEY:
        return jsonify({"status": "unauthorized"}), 401
    return jsonify({"master_list": current_master_list}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
