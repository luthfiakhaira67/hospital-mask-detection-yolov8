# FaceGuard AI — Hospital Gate Mask Detection (YOLOv8)

Sistem deteksi penggunaan masker secara *real-time* berbasis web untuk kontrol akses pintu masuk area Rumah Sakit menggunakan **YOLOv8 Nano**, **OpenCV**, **Flask**, dan **Tailwind CSS**.

## Fitur Utama
- **Klasifikasi 3 Kelas Deteksi:**
  - `with_mask` — **Akses Diizinkan** (Pintu portal terbuka otomatis)
  - `without_mask` — **Akses Ditolak** (Peringatan wajib memakai masker)
  - `mask_worn_incorrectly` — **Perbaiki Masker** (Peringatan posisi masker belum menutupi hidung dan mulut)
- **Dynamic Live Notification Banner:** Status akses, skor kepercayaan (*confidence*), dan indikator pintu pada antarmuka web berubah secara *real-time* mengikuti hasil deteksi kamera.
- **Panduan Edukasi Pengunjung:** Halaman beranda dilengkapi standar visual cara penggunaan masker medis yang baik dan benar.
- **Optimasi Dataset & Mitigasi Occlusion Bias:** Dilatih menggunakan dataset teraugmentasi di Roboflow (3.751 gambar dari 1.349 gambar asli) untuk menekan kesalahan deteksi akibat benda penghalang.

## Struktur Proyek
```text
hospital-mask-detection-yolov8/
├── models/
│   └── best.pt                 # Bobot model YOLOv8 Nano (v3)
├── static/
│   └── css/
│       └── style.css           # Custom stylesheet tambahan
├── templates/
│   ├── index.html              # Halaman Dashboard & Panduan Penggunaan Masker
│   └── detection.html          # Halaman Live Monitoring & Gate Control
├── detect_realtime.py          # Script pengujian deteksi real-time via OpenCV
├── main.py                     # Server utama Flask & API status deteksi
├── README.md                   # Dokumentasi proyek
└── requirements.txt            # Daftar dependensi Python