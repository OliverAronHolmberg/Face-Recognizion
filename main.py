import threading
import cv2  # type: ignore
from deepface import DeepFace  # type: ignore 

# Referens bild
reference_image_path = "Images\\WIN_20250430_20_44_12_Pro.jpg"

# Finns för att programet inte ska lagga
frame_count = 0

# Starta Webcam
cap = cv2.VideoCapture(0)

# Status för om en frame kan varifieras samtidigt
verifying = False

# Ifall webcamen inte öppnar så stängs programet
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Funktion som kör verifiering i bakgrunden
def run_verification(frame):
    global verifying
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (320, 240))
        result = DeepFace.verify(small_frame, reference_image_path)

        # Kollar så framen är varifierad och isåfall sätter message på true
        if result["verified"]:
            print("true")
            message = "True"
        else:
            print("false")
            message = "False"
    except Exception as e:
        print("False")
        message = "False"


    verifying = False

while True:
    ret, frame = cap.read()

    # Om programet inte kan ta emot webcamen så stängs loopen
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Visa webbkamera-bilden på monitorn
    cv2.imshow('Webcam', frame)

    # Lägg till 1 på frame count varje frame
    frame_count += 1

    # Kolla så bilden matchar, starta verifiering varje 30:e frame om inget verifieras
    if frame_count % 30 == 0 and not verifying:
        verifying = True
        # Skapa en tråd för att köra verifiering i bakgrunden
        threading.Thread(target=run_verification, args=(frame.copy(),)).start()

    # Tryck 'q' för att avsluta
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#Stänger av kameran
cap.release()

#Stänger alla fönster som skapades med programet
cv2.destroyAllWindows()
