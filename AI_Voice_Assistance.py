import os
import sys
from os import system
import speech_recognition as sr
import whisper
from gpt4all import GPT4All
import sounddevice as sd
import numpy as np
import boto3
from pydub import playback
import pydub
import cv2

wake_word = "Jogi"
model = GPT4All(r"C:\ecs\ML Model\gpt4all-falcon-q4_0.gguf", allow_download=False)

tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.pt')
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
tiny_model = whisper.load_model(tiny_model_path)
base_model = whisper.load_model(base_model_path)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

def synthesize_speech(text,output_filename):
    polly = boto3.client('polly', region_name='us-east-1')
    response = polly.synthesize_speech(
        VoiceId='Ruth',
        OutputFormat='mp3', 
        Text=text, 
        Engine='neural'
    )

    with open(output_filename, 'wb') as f:
        f.write(response['AudioStream'].read())

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, foormat="mp3")
    playback.play(sound)

def detect_wake_word(audio):
    """Detects if the wake word is present in the given audio."""
    with open("wake_detect.wav", "wb") as f:
        f.write(audio.get_wav_data())
    result = tiny_model.transcribe('wake_detect.wav')
    text_input = result['text']
    return wake_word in text_input.lower()

def detect_claps(audio_data, threshold=0.7):
    rms = np.sqrt(np.mean(np.square(audio_data)))
    return rms > threshold

def prompt_gpt(audio):      # audio is the user's prompt
    try:
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        prompt_text = result['text']
        if len(prompt_text.strip()) == 0:
            print("Empty prompt. Please speak again.")

            # speak("Empty prompt. Please speak again.")
        else:
            print('User: ' + prompt_text)
            output = model.generate(prompt_text, max_tokens=100)
            print('Prompt: ', output)
            # speak(output)
            synthesize_speech(output, 'response.mp3')
            play_audio('response.mp3')
            print('\n' 'Do you need my help in some other matter. \n')
            synthesize_speech('Do you need my help in some other matter. \n',"regenerate.mp3")
            play_audio("regenerate.mp3")
    except Exception as e:
        print("Prompt error: ", e)

def continuous_listen():    # This function listens for claps and prompts the user to speak
    r = sr.Recognizer()  # Initialize the recognizer here
    
    with sr.Microphone() as source:     # Use the default microphone as the audio source
        r.adjust_for_ambient_noise(source, duration=0.5)
        print('\nHi, my name is Tanya. \n')
        synthesize_speech('Hi, my name is Tanya.', 'Intro.mp3')
        play_audio('Intro.mp3')

        while True:
            try:
                # Record audio for a short duration
                audio_data = sd.rec(int(44100 * 0.5), samplerate=44100, channels=2, dtype=np.int16)
                sd.wait()

                # Check for claps
                if detect_claps(audio_data):
                    #print("Clap detected. Please speak your prompt to GPT4All.")
                    synthesize_speech("How may I help you?", 'response.mp3')
                    # speak('Hey everyone, How may I help you?')
                    play_audio('response.mp3')

                    # Listen for a longer duration to capture the user's command or question
                    with sr.Microphone() as new_source:
                        print("Listening for user's prompt...")
                        audio_prompt = r.listen(new_source, timeout=5)
                    prompt_text = r.recognize_google(audio_prompt).lower()
                    print("User: ", prompt_text)

                    #Check for stop word
                    if "stop" in prompt_text:
                        print("Stopping...")
                        sys.exit(0)
                    
                    #Check for wake word
                    prompt_gpt(audio_prompt)

            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    continuous_listen()