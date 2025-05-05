import cv2  # type: ignore
from deepface import DeepFace  # type: ignore
import mqtt_publisher  

# Referens bild 
reference_image_path = "Images\\WIN_20250430_20_44_12_Pro.jpg"


frame_count = 0

# Starta Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Lägg till 1 på frame_count
    frame_count += 1

    # Kolla så bilden matchar var 5:te frame
    if frame_count % 5 == 0:
        try:
            result = DeepFace.verify(frame, reference_image_path)
            if result["verified"]:
                print("true")
                message = "True"
            else:
                print("false")
                message = "False"
        except Exception as e:
            print("false")
            message = "False"

        #Sicka till mqtt script
        mqtt_publisher.send_message(message)  
    
    # Stäng av om man trycker q
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
