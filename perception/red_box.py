import cv2
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
try:
    while True:
        ret, frame = cap.read()
        if not ret: break
        hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (5,5), 0), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0,170,50), (7,255,255))
        mask |= cv2.inRange(hsv, (173,170,50), (180,255,255))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 500:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.imshow("red", frame)
        if cv2.waitKey(1) == 27: break
finally:
    cap.release(); cv2.destroyAllWindows()
