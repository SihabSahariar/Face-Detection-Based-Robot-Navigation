import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def move_robot(face_x, frame_width):
    mid_x = frame_width // 2
    if face_x < mid_x - 50:
        print("Turn Left")
        # Send control signals to turn the robot left
    elif face_x > mid_x + 50:
        print("Turn Right")
        # Send control signals to turn the robot right
    else:
        print("Move Forward")
        # Send control signals to move the robot forward

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_height, frame_width, _ = frame.shape
    mid_x = frame_width // 2
    mid_y = frame_height // 2

    # Draw center rectangle box
    rect_start = (mid_x - 100, mid_y - 100)
    rect_end = (mid_x + 100, mid_y + 100)
    cv2.rectangle(frame, rect_start, rect_end, (0, 0, 255), 2)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_center_x = x + w // 2
        move_robot(face_center_x, frame_width)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
