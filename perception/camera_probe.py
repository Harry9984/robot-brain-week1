import cv2

for i in range(4):
    cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print(f"[{i}] NO DEVICE")
        continue
    frame = None
    for _ in range(10):
        ret, f = cap.read()
        if ret:
            frame = f
            break
    if frame is None:
        print(f"[{i}] OPENED BUT NO FRAME")
    else:
        print(f"[{i}] LIVE shape={frame.shape}")
        cv2.imshow(f"camera {i}", frame)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    cap.release()
print("PROBE DONE")
