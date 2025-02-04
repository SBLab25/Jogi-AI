import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import pyttsx3
import threading
import time

# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Specify the full path to the 'mp_hand_gesture' directory
model_path = r"C:\ecs\ML Model\mp_hand_gesture"

# Specify the full path to the 'gesture.names' file
class_names_file = r"C:\ecs\ML Model\gesture.names"

# Load the gesture recognizer model from the specified path
model = load_model(model_path)

# Load class names from the specified file
with open(class_names_file, 'r') as f:
    classNames = f.read().split('\n')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define the cooldown time (in seconds) between gesture recognitions
cooldown_time = 2  # Adjust this value as needed

# Initialize variables to keep track of time
last_recognition_time = 0

def process_frame(frame):
    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    className = ''

    # Post-process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]

    return frame, className

def text_to_speech(class_name):
    engine.say(class_name)
    engine.runAndWait()

while True:
    current_time = time.time()

    if current_time - last_recognition_time >= cooldown_time:
        # Read each frame from the webcam
        _, frame = cap.read()

        frame, className = process_frame(frame)

        if className:
            text_to_speech(className)
            last_recognition_time = current_time

        # Show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Show the final output
        cv2.imshow("Output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
