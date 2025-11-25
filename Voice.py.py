import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Ava:", text)
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=4, fs=16000):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio, fs

def recognize_audio():
    audio, fs = record_audio()
    wav.write("input.wav", fs, audio)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile("input.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("You (voice):", text)
            return text.lower()
        except:
            speak("Sorry, I couldn't understand.")
            return ""

def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + now)
    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak("Today's date is " + today)
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak("Searching for " + query)
        webbrowser.open("https://www.google.com/search?q=" + query)
    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a nice day.")
        exit()
    else:
        speak("I didn't understand. Try saying time, date or search.")

def main():
    speak("Hello! I'm Ava, your voice assistant.")
    speak("You can speak or type commands.")

    while True:
        choice = input("Type 'v' for voice or 't' for typing: ").lower()

        if choice == "t":
            command = input("You (type): ").lower()
        elif choice == "v":
            command = recognize_audio()
        else:
            speak("Invalid choice.")
            continue

        handle_command(command)

main()
