import os
import base64
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Bật CORS để giao diện HTML gọi API mượt mà không bị chặn

# Thư mục gốc lưu ảnh trên máy tính
ROOT_DIR = r"C:\BloomShoot_Photos"

@app.route('/create_pin_folder', methods=['POST'])
def create_pin_folder():
    try:
        data = request.json
        pin = data.get('pin')
        if not pin:
            return jsonify({"status": "error", "message": "Missing PIN"}), 400
        
        # Tạo thư mục mã PIN cục bộ
        pin_folder = os.path.join(ROOT_DIR, str(pin))
        os.makedirs(pin_folder, exist_ok=True)
        
        print(f"✅ Đã tạo thư mục ca chụp cho PIN: {pin} tại {pin_folder}")
        return jsonify({"status": "success", "message": f"Created folder for PIN {pin}"})
    except Exception as e:
        print(f"❌ Lỗi tạo thư mục: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/save_photo', methods=['POST'])
def save_photo():
    try:
        data = request.json
        pin = data.get('pin')
        image_data = data.get('image')
        is_merged = data.get('is_merged', False)
        
        if not pin or not image_data:
            return jsonify({"status": "error", "message": "Missing data"}), 400
            
        pin_folder = os.path.join(ROOT_DIR, str(pin))
        os.makedirs(pin_folder, exist_ok=True)
        
        # Xử lý giải mã chuỗi Base64 thành file ảnh PNG
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        
        prefix = "Merged_" if is_merged else "Photo_"
        filename = f"{prefix}{int(time.time())}.png"
        filepath = os.path.join(pin_folder, filename)
        
        with open(filepath, "wb") as fh:
            fh.write(image_bytes)
            
        print(f"📸 Đã lưu ảnh vào thư mục {pin}: {filename}")
        return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        print(f"❌ Lỗi lưu ảnh: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    os.makedirs(ROOT_DIR, exist_ok=True)
    print(f"🚀 Server Python BLOOM SHOOT đang chạy tại: http://127.0.0.1:5000")
    print(f"📁 Thư mục lưu ảnh cục bộ: {ROOT_DIR}")
    app.run(host='127.0.0.1', port=5000, debug=True)