import cv2 # type: ignore
from deepface import DeepFace # type: ignore 


# Referens bild
reference_image_path = "Images\WIN_20250430_20_44_12_Pro.jpg"

# Boolean message
face_detected = False

# Starta webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Press 'q' to quit")

while True:
    # Kolla varje frame
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Visa webcam live
    cv2.imshow('Webcam Feed', frame)

    # Kolla ifall det är refrence bilden
    try:
        result = DeepFace.verify(frame, reference_image_path)
        if result["verified"]:
            face_detected = True
        else:
            face_detected = False
    except Exception as e:
        face_detected = False
    
    # Quita
    if cv2.waitKey(1) == ord('q'):
        break

# Stäng av
cap.release()
cv2.destroyAllWindows()
