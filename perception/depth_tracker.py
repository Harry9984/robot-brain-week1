import cv2
import numpy as np
import math

FOCAL_LENGTH = 1110.0
REAL_WIDTH_CM = 7.0

try:
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    last_x, last_y, last_w, last_h = -1, -1, -1, -1

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # THE MUSCLE (Initialize the window)
        motor_frame = np.zeros((200, 200, 3), dtype=np.uint8)
        cv2.putText(motor_frame, "MOTOR SHAFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        
        # THE EYES (Perception)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0,160,50), (10,255,255)) | cv2.inRange(hsv, (170,160,50), (180,255,255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        screen_center_x = frame.shape[1] // 2
        
        # DEFAULT STATE
        steering_command = 0
        state = "SEARCHING"
        
        # THE BRAIN (State Machine)
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 2000:
                x, y, w, h = cv2.boundingRect(c)
                
                if last_x == -1:
                    last_x, last_y, last_w, last_h = x, y, w, h
                else:
                    last_x = int(0.7 * last_x + 0.3 * x)
                    last_y = int(0.7 * last_y + 0.3 * y)
                    last_w = int(0.7 * last_w + 0.3 * w)
                    last_h = int(0.7 * last_h + 0.3 * h)
                    
                object_cx = last_x + last_w // 2
                error_x = int(object_cx - screen_center_x)
                distance_cm = (REAL_WIDTH_CM * FOCAL_LENGTH) / last_w
                
                if distance_cm < 15:
                    state = "ARRIVED"
                    steering_command = 0
                elif abs(error_x) < 20:
                    state = "ALIGNED"
                    steering_command = 0
                else:
                    state = "TRACKING"
                    steering_command = int(error_x * 0.5)
                    
                print(f"[{state}] Dist: {distance_cm:.1f} cm | Error: {error_x} | Cmd: {steering_command}")
                cv2.rectangle(frame, (last_x, last_y), (last_x + last_w, last_y + last_h), (0,255,0), 2)
                cv2.putText(frame, f"{distance_cm:.0f} cm", (last_x, last_y + last_h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                cv2.circle(frame, (object_cx, last_y + last_h // 2), 5, (255, 0, 0), -1)
            else:
                if last_x != -1:
                    cv2.rectangle(frame, (last_x, last_y), (last_x + last_w, last_y + last_h), (0,255,255), 2)
        else:
            if last_x != -1:
                cv2.rectangle(frame, (last_x, last_y), (last_x + last_w, last_y + last_h), (0,255,255), 2)

        # THE MUSCLE (Map command to visual angle)
        angle_deg = steering_command * 0.2 
        rad = math.radians(angle_deg - 90) 
        x2 = int(100 + 80 * math.cos(rad))
        y2 = int(100 + 80 * math.sin(rad))
        
        cv2.line(motor_frame, (100, 100), (x2, y2), (0, 255, 0), 6)
        cv2.circle(motor_frame, (100, 100), 5, (255, 255, 255), -1)
        
        cv2.imshow("MUSCLE", motor_frame)
        cv2.imshow("Z-Axis", frame)
        cv2.imshow("mask", mask)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
