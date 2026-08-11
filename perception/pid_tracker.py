import numpy as np
import cv2
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
last_x, last_y, last_w, last_h = -1, -1, -1, -1
try:
    while True:
        ret, frame = cap.read()
        screen_center_x = frame.shape[1] // 2
        cv2.line(frame, (screen_center_x, 0), (screen_center_x, frame.shape[0]), (255, 0, 0), 2) # Draw a blue center line
        if not ret: break
        hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (5,5), 0), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0,160,50), (10,255,255))
        mask |= cv2.inRange(hsv, (170,160,50), (180,255,255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 2000:
                x, y, w, h = cv2.boundingRect(c)
                
                if last_x == -1: # First time seeing it
                    last_x, last_y, last_w, last_h = x, y, w, h
                else:
                    # THE MEMORY FORMULA: 70% past, 30% present
                    last_x = int(0.7 * last_x + 0.3 * x)
                    last_y = int(0.7 * last_y + 0.3 * y)
                    last_w = int(0.7 * last_w + 0.3 * w)
                    last_h = int(0.7 * last_h + 0.3 * h)
                
                # The object center is the left edge (last_x) + half the width (last_w)
                object_cx = last_x + last_w // 2 
                
                # Calculate Error (Integer division not needed here, but we cast to int for clean printing)
                error_x = int(object_cx - screen_center_x)
                
                # P-Controller: The multiplier (Kp) is 0.5
                steering_command = int(error_x * 0.5)
                
                # Print the command to the terminal
                print(f"Error: {error_x} | Steering Command: {steering_command}")
                
                # Draw the center dot of the object so you can see it cross the blue line
                cv2.circle(frame, (object_cx, last_y + last_h // 2), 5, (255, 0, 0), -1)

                # Draw the smoothed memory (Green)
                cv2.rectangle(frame, (last_x, last_y), (last_x + last_w, last_y + last_h), (0,255,0), 2)
                cv2.putText(frame, "TRACKING", (last_x, last_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        else:
            # THE GHOST: Camera is blind, rely on memory (Yellow)
            if last_x != -1:
                cv2.rectangle(frame, (last_x, last_y), (last_x + last_w, last_y + last_h), (0,255,255), 2)
                cv2.putText(frame, "GHOST", (last_x, last_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
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
