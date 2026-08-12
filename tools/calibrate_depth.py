import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

print("Hold the object exactly 50 cm from the camera lens.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, (0, 160, 50), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 160, 50), (180, 255, 255))
    mask = mask1 | mask2
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, f"Width: {w} px", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            
    cv2.imshow("Z-Axis Calibration", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
