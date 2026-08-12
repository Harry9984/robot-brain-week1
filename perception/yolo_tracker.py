import cv2
import math
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 Nano (downloads automatically the first time)
model = YOLO('yolov8n.pt')

# In the COCO dataset, class 39 is 'bottle'. 
TARGET_CLASS_ID = 39 
TARGET_REAL_WIDTH_CM = 10 # CHANGE THIS to your ruler measurement!
FOCAL_LENGTH = 1110.0      # The constant you calibrated in Layer 0

try:
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    last_x, last_y, last_w, last_h = -1, -1, -1, -1

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # THE MUSCLE (Initialize)
        motor_frame = np.zeros((200, 200, 3), dtype=np.uint8)
        cv2.putText(motor_frame, "YOLO MOTOR", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        
        # THE EYES (Neural Network Inference)
        results = model(frame, verbose=False)
        
        screen_center_x = frame.shape[1] // 2
        steering_command = 0
        state = "SEARCHING"
        
        # Find the bottle
        target_box = None
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                if cls_id == TARGET_CLASS_ID:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    target_box = (x1, y1, x2 - x1, y2 - y1)
                    break
            if target_box: break
            
        # THE BRAIN (If eyes see the target)
        if target_box:
            x, y, w, h = target_box
            
            # Sensor Fusion (Memory)
            if last_x == -1:
                last_x, last_y, last_w, last_h = x, y, w, h
            else:
                last_x = int(0.7 * last_x + 0.3 * x)
                last_y = int(0.7 * last_y + 0.3 * y)
                last_w = int(0.7 * last_w + 0.3 * w)
                last_h = int(0.7 * last_h + 0.3 * h)
                
            object_cx = last_x + last_w // 2
            error_x = int(object_cx - screen_center_x)
            distance_cm = (TARGET_REAL_WIDTH_CM * FOCAL_LENGTH) / last_w
            
            # State Machine
            if distance_cm < 20:
                state = "ARRIVED"
                steering_command = 0
            elif abs(error_x) < 30: # Slightly larger deadzone for YOLO
                state = "ALIGNED"
                steering_command = 0
            else:
                state = "TRACKING"
                steering_command = int(error_x * 0.5)
                
            print(f"[{state}] Dist: {distance_cm:.1f} cm | Error: {error_x} | Cmd: {steering_command}")
            cv2.rectangle(frame, (last_x, last_y), (last_x + last_w, last_y + last_h), (0,255,0), 2)
            cv2.putText(frame, f"Bottle {distance_cm:.0f}cm", (last_x, last_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            
        # THE MUSCLE (Map command to visual angle)
        angle_deg = steering_command * 0.2 
        rad = math.radians(angle_deg - 90) 
        x2 = int(100 + 80 * math.cos(rad))
        y2 = int(100 + 80 * math.sin(rad))
        
        cv2.line(motor_frame, (100, 100), (x2, y2), (0, 255, 0), 6)
        cv2.circle(motor_frame, (100, 100), 5, (255, 255, 255), -1)
        
        cv2.imshow("YOLO MUSCLE", motor_frame)
        cv2.imshow("YOLO EYES", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
