import cv2

# Menggunakan CAP_DSHOW khas untuk Windows
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Kamera Index 0 gagal, cuba Index 1...")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil gambar dari kamera.")
        break
        
    cv2.imshow('Ujian Kamera Laptop', frame)
    
    # Tekan 'q' pada papan kekunci untuk tutup
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()