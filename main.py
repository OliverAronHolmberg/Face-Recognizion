import threading
import cv2
from deepface import DeepFace
from mqtt_publisher import send_message
import subprocess
import os
import time
import webbrowser
import socket

base_dir = os.path.dirname(os.path.abspath(__file__))

# Start Node.js server
node_process = subprocess.Popen(
    ["node", "webcam-site/server.js"],
    cwd=base_dir,
    shell=True
)

def wait_for_server(host, port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

if wait_for_server("localhost", 3000):
    webbrowser.open_new_tab("http://localhost:3000")
else:
    print("⚠️ Node server did not start within 10 seconds.")

reference_image_path = "Images\\WIN_20250430_20_44_12_Pro.jpg"
frame_count = 0
cap = cv2.VideoCapture(0)
last_message = ""
verifying = False

# Path to save JPEG frames for the webpage
jpeg_output_path = os.path.join(base_dir, "webcam-site", "public", "latest.jpg")
temp_jpeg_path = os.path.join(base_dir, "webcam-site", "public", "latest_temp.jpg")  # proper .jpg extension

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def send_verification_status(message):
    global last_message
    send_message(message)
    last_message = message
    status_file = os.path.join(base_dir, "webcam-site", "public", "status.txt")
    try:
        with open(status_file, "w") as f:
            f.write(message)
    except Exception as e:
        print(f"Failed to write status.txt: {e}")



def run_verification(frame):
    global verifying, last_message
    message = "False"  # <-- Add this line to initialize message
    
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (320, 240))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_frame = frame[y:y+h, x:x+w]
                print(f"Detected face at [{x}, {y}, {w}, {h}]")
                result = DeepFace.verify(face_frame, reference_image_path)
                print(f"DeepFace result: {result}")
                if result.get("verified", False):
                    print("Face verified: True")
                    message = "True"
                else:
                    print("Face not verified: False")
                    message = "False"
                if message != last_message:
                    send_verification_status(message)
                    last_message = message
        else:
            print("No faces detected.")
            if last_message != "False":
                send_verification_status("False")
                last_message = "False"
    except Exception as e:
        print(f"Error: {e}")
        if last_message != "False":
            send_verification_status("False")
            last_message = "False"
    verifying = False


# Throttle saving to ~10 FPS to reduce flickering
save_fps = 10
last_save_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Resize for consistent output size
    small_frame = cv2.resize(frame, (640, 480))

    now = time.time()
    if now - last_save_time > 1 / save_fps:
        cv2.imwrite(temp_jpeg_path, small_frame)
        try:
            if os.path.exists(jpeg_output_path):
                os.remove(jpeg_output_path)
            os.rename(temp_jpeg_path, jpeg_output_path)
        except PermissionError:
            print("PermissionError on rename, retrying after 0.1 seconds...")
            time.sleep(0.1)
            if os.path.exists(jpeg_output_path):
                os.remove(jpeg_output_path)
            os.rename(temp_jpeg_path, jpeg_output_path)
        last_save_time = now

    frame_count += 1

    # Run verification every 30 frames if not currently verifying
    if frame_count % 30 == 0 and not verifying:
        verifying = True
        threading.Thread(target=run_verification, args=(frame.copy(),)).start()

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
