import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# Ultrasonic sensor pins
TRIG_PIN = 22
ECHO_PIN = 27

# Motor driver pins
IN1_PIN = 12
IN2_PIN = 13
IN3_PIN = 16
IN4_PIN = 19

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up ultrasonic sensor pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Set up motor driver pins
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(IN3_PIN, GPIO.OUT)
GPIO.setup(IN4_PIN, GPIO.OUT)

# Function to move forward
def move_forward():
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)
    GPIO.output(IN3_PIN, GPIO.HIGH)
    GPIO.output(IN4_PIN, GPIO.LOW)

# Function to move left
def move_left():
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)
    GPIO.output(IN3_PIN, GPIO.LOW)
    GPIO.output(IN4_PIN, GPIO.HIGH)

# Function to move right
def move_forward():
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.HIGH)
    GPIO.output(IN3_PIN, GPIO.HIGH)
    GPIO.output(IN4_PIN, GPIO.LOW)

# Function to stop
def stop():
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.LOW)
    GPIO.output(IN3_PIN, GPIO.LOW)
    GPIO.output(IN4_PIN, GPIO.LOW)

# Function to measure distance using ultrasonic sensor
def get_distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    return distance

# Function to move my robot with sensor value and face position
# Navigation Algorithm
def move_robot(distance, face_x, frame_width):
    mid_x = frame_width // 2
    if (face_x < mid_x - 50):
        print("Turn Left")
        move_left()
    elif face_x > mid_x + 50:
        print("Turn Right")
        move_right()
    else:
        print("Move Forward")
        move_forward()
        if distance < 20:
            print("Stop")
            stop()

try:
    while True:
        ret, frame = cap.read()
        distance = get_distance()
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
            move_robot(distance, face_center_x, frame_width)

        cv2.imshow('BRACU Facebot v1.0', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    GPIO.cleanup()

cap.release()
cv2.destroyAllWindows()
