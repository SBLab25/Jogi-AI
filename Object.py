import cv2
import numpy as np
import os
from gtts import gTTS
import pygame
import mediapipe as mp
import time

# Initialize Pygame mixer for audio
pygame.mixer.init()

# Object detection settings
yolov4_weights = "C:\ecs\ML Model\yolov4-tiny.weights"
yolov4_cfg = "C:\ecs\ML Model\yolov4-tiny.cfg"
classes_file = "C:\ecs\ML Model\classes.txt"

# Initialize YOLOv4-tiny
net = cv2.dnn.readNet(yolov4_weights, yolov4_cfg)
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1 / 255)

# Load class lists
classes = []
with open(classes_file, "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

# Initialize camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower frame resolution
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Lower frame resolution

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# State variables
object_detection_active = False
last_object = None
thumb_up_count = 0
thumb_down_count = 0
threshold = 5  # Adjust this threshold for accuracy
frame_delay = 0.1  # Add a delay of 100 milliseconds between frames

while True:
    ret, frame = cam.read()

    # Use MediaPipe for hand tracking
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Check if the thumb is raised (you can adjust the landmark indices)
            if landmarks.landmark[4].y < landmarks.landmark[3].y and landmarks.landmark[4].y < landmarks.landmark[2].y:
                thumb_up_count += 1
                thumb_down_count = 0
            else:
                thumb_down_count += 1
                thumb_up_count = 0

            if thumb_up_count >= threshold:
                if not object_detection_active:
                    object_detection_active = True
                    tts = gTTS(text="OBJECT DETECTION FEATURE ACTIVATED", lang='en')
                    tts.save("activated.mp3")
                    pygame.mixer.music.load("activated.mp3")
                    pygame.mixer.music.play()
            elif thumb_down_count >= threshold:
                object_detection_active = False
                thumb_up_count = 0

    if object_detection_active:
        # Object Detection
        (class_ids, scores, bboxes) = model.detect(frame)
        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            (x, y, w, h) = bbox
            class_name = classes[class_id]
            print(class_name)
            print(score)
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)

            if class_name != last_object and not pygame.mixer.music.get_busy() and score > 0.5:
                name = class_name + ".mp3"

                # Only get from Google if we don't have it
                if not os.path.isfile(name):
                    tts = gTTS(text="I see a " + class_name, lang='en', slow=True)
                    tts.save(name)

                last_object = class_name
                pygame.mixer.music.load(name)
                pygame.mixer.music.play()

    # Display the 'Press q to close' message
    cv2.putText(frame, "Press 'q' to close", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Frame", frame)
    
    # Check for 'q' key press and exit the loop if pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(frame_delay)  # Add a frame delay to reduce CPU usage

# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
