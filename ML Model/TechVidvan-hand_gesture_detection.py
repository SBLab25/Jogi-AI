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

# Specify paths
model_path = r"C:\Users\chand\OneDrive\Desktop\hand-gesture-recognition-code (1)\mp_hand_gesture"
class_names_file = r"C:\Users\chand\OneDrive\Desktop\hand-gesture-recognition-code (1)\gesture.names"

# Load the gesture recognizer model
model = load_model(model_path)

# Load class names
with open(class_names_file, 'r') as f:
    classNames = f.read().split('\n')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define the cooldown time (in seconds) between gesture recognitions
cooldown_time = 2  # Adjust this value as needed

# Initialize variables to keep track of time
last_recognition_time = 0

# Initialize TTS engine in a separate thread
tts_engine = pyttsx3.init()
tts_lock = threading.Lock()

def text_to_speech_async(class_name):
    def async_tts():
        with tts_lock:
            tts_engine.say(class_name)
            tts_engine.runAndWait()

    threading.Thread(target=async_tts).start()

while True:
    current_time = time.time()

    if current_time - last_recognition_time >= cooldown_time:
        # Read each frame from the webcam
        _, frame = cap.read()

        # Resize the frame for hand detection (improve speed)
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Get hand landmark prediction
        x, y, _ = small_frame.shape
        framergb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        result = hands.process(framergb)

        landmarks = []
        className = ''

        # Post-process the result
        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(small_frame, handslms, mpHands.HAND_CONNECTIONS)

        if landmarks:
            # Predict gesture
            className = classNames[np.argmax(model.predict([landmarks]))]

        if className:
            text_to_speech_async(className)
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
