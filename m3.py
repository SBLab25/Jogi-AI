import speech_recognition as sr
import os
import webbrowser

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 4000

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"User said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        listen()
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        listen()

# Function to run the AI voice assistant [ I DONT HAVE VOICE ASSISTANT SO A SIMPLE PROGRAM TO PRINT A PATTERN]
def open_jarvis():
    # os.system("python code1.py")
    path_to_code1 = "C:/Users/Ankit/Desktop/bhupendar/m4.py"
    os.system(f"python {path_to_code1}")
    

# Function to run object detection   , presss q to stop
def open_object_detection():
    path_to_code2 = "C:/Users/Ankit/Desktop/bhupendar/draft3.py"
    os.system(f"python {path_to_code2}")

# Function to search something in firefox
def open_browser_and_search(query):
    url = f'https://www.google.com/search?q={query}'
    webbrowser.open_new_tab(url)


def open_browser_and_open(query):
    url = f'https://www.{query}.com/'
    webbrowser.open_new_tab(url)

def play_youtube_or_spotify():
    path_to_code1 = "C:/Users/Ankit/Desktop/bhupendar/m5.py"
    os.system(f"python {path_to_code1}")

# Main function to listen to user commands
if __name__ == "__main__":
    while True:
        user_input = listen()
        # user_input = user_input.lower()
        words = user_input.split()
        
        
        if 'friday' in user_input:
            open_jarvis()
        if 'vision' in user_input:
            open_object_detection()
        if len(words) > 0 and words[0].lower() == "search":
            words = ' '.join(words[1:])
            open_browser_and_search(words)
            if input("Press Enter to continue after closing the browser..."):
                continue

        if len(words) > 0 and words[0].lower() == "open":
            words = ' '.join(words[1:])
            open_browser_and_open(words)
            if input("Press Enter to continue after closing the browser..."):
                continue
        if 'youtube' in user_input or 'spotify' in user_input:
            play_youtube_or_spotify()

        if 'stop' in user_input:
            os.system("taskkill /im python.exe /f")
        if 'quit' in user_input:
            break



