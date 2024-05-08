import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
import pyttsx3
import pywhatkit

# Spotify API credentials
# SPOTIPY_CLIENT_ID = '8b94a2ca458e4ac49b754bf3443bd0be'
# SPOTIPY_CLIENT_SECRET = '88a1299a986841439a78491c27f9e921'
# SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# # Spotify authentication
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIPY_REDIRECT_URI,
#                                                scope="user-library-read user-read-playback-state user-modify-playback-state"))

# Speech recognition setup
# recognizer = sr.Recognizer()

# Text-to-speech setup
# engine = pyttsx3.init()

# def play_song(track_name):
#     # Search for the track
#     results = sp.search(q=track_name, type='track', limit=1)
    
#     if results['tracks']['items']:
#         track_uri = results['tracks']['items'][0]['uri']
#         sp.start_playback(uris=[track_uri])
#         engine.say(f"Playing {track_name}")
#         engine.runAndWait()
#     else:
#         engine.say("Sorry, I couldn't find that song.")
#         engine.runAndWait()

# def play_youtube_video(video_query):
#     pywhatkit.playonyt(video_query)
#     engine.say(f"Playing {video_query} on YouTube.")
#     engine.runAndWait()

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

if __name__ == "main":
   while True:
        command = listen()
        command = command.lower()
        # words = user_input.split()
        
        
        # if "play" in command and "song" in command:
        #     song_name = command.replace("play", "").replace("song", "").strip()
        #     play_song(song_name)
        # if "play" in command and "video" in command:
        #     video_query = command.replace("play", "").replace("video", "").strip()
        #     play_youtube_video(video_query)
        # if "exit" in command or "quit" in command:
        #     break