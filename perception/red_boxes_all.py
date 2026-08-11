import numpy as np
import cv2
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
try:
    while True:
        ret, frame = cap.read()
        if not ret: break
        hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (5,5), 0), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0,160,50), (10,255,255))
        mask |= cv2.inRange(hsv, (170,160,50), (180,255,255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) > 2000:
                x, y, w, h = cv2.boundingRect(c)
                cx = x + w // 2
                cy = y + h // 2
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.circle(frame, (cx, cy), 4, (0,0,255), -1)
                cv2.putText(frame, f"({cx},{cy})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        cv2.imshow("red", frame)
        cv2.imshow("mask", mask)
        if cv2.waitKey(1) == 27: break
finally:
    cap.release(); cv2.destroyAllWindows()
