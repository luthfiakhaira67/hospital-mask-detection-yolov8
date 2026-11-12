import os
import cv2
from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO

app = Flask(__name__)

# Path absolut ke model best.pt v3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best.pt')

# Load model YOLOv8
model = YOLO(MODEL_PATH)

# Inisialisasi kamera secara global
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not camera.isOpened():
    camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Menyimpan status deteksi terbaru untuk dikirim ke UI Web
latest_status = {
    "state": "idle",
    "confidence": 0.0
}

def gen_frames():
    global latest_status
    while True:
        success, frame = camera.read()
        if not success:
            continue
        
        # Predict dengan model YOLOv8 (Confidence threshold 0.50)
        results = model(frame, conf=0.50, verbose=False)
        annotated_frame = frame.copy()
        
        detected_state = "idle"
        highest_conf = 0.0

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                # Ambil deteksi dengan confidence tertinggi untuk alert utama UI
                if conf > highest_conf:
                    highest_conf = conf
                    detected_state = class_name

                # Tentukan Pesan Alert & Warna di frame kamera
                if class_name == 'with_mask':
                    status_text = f"AKSES DIIZINKAN ({conf:.2f})"
                    color = (0, 200, 83)      # Hijau (BGR)
                elif class_name == 'without_mask':
                    status_text = f"AKSES DITOLAK: PAKAI MASKER! ({conf:.2f})"
                    color = (50, 50, 255)     # Merah (BGR)
                else:  # mask_worn_incorrectly
                    status_text = f"PERBAIKI POSISI MASKER! ({conf:.2f})"
                    color = (0, 165, 255)     # Oranye/Kuning (BGR)

                # Gambar Bounding Box Custom
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Gambar Badge Status di atas Wajah
                label_size, _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(annotated_frame, (x1, y1 - 25), (x1 + label_size[0] + 10, y1), color, -1)
                cv2.putText(annotated_frame, status_text, (x1 + 5, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)

        # Update status global
        latest_status["state"] = detected_state
        latest_status["confidence"] = round(highest_conf * 100, 1)

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint API baru untuk mengirim status deteksi ke JavaScript di frontend
@app.route('/status')
def status():
    return jsonify(latest_status)

if __name__ == '__main__':
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
    finally:
        if camera.isOpened():
            camera.release()