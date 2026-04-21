import socket
import threading

# ตั้งค่า IP และ Port (ต้องเปิด Port บน Firewall ของ Server ด้วย)
HOST = '0.0.0.0'
PORT = 9000

def handle_client(conn, addr):
    print(f"เชื่อมต่อใหม่จาก: {addr}")
    while True:
        try:
            # รอรับข้อมูลจาก Master หรือ Slave
            data = conn.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"ได้รับ: {message}")
            
            # TODO: กระจายข้อมูลให้ Slave ทุกคนที่ต่อท่อค้างไว้
            
        except ConnectionResetError:
            break
    
    conn.close()
    print(f"ยกเลิกการเชื่อมต่อ: {addr}")

# เปิด Server รอรับสาย
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(100) # รองรับคิว 100 คนพร้อมกัน
print(f"เปิดเซิร์ฟเวอร์รอที่พอร์ต {PORT}...")

while True:
    conn, addr = server.accept()
    # โยนงานให้ Thread ใหม่ดูแลลูกค้าแต่ละคน
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
