import tkinter as tk
import speech_recognition as sr

# Global flag to control recording
is_recording = False

def start_recording():
    global is_recording
    is_recording = True
    while is_recording:
        print("Listening...")
        # Initialize recognizer class (for recognizing the speech)
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            try:
                # Listen for audio and recognize speech
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)  # Using Google's speech recognition API
                print(f"Recognized speech: {text}")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service")
            if not is_recording:
                break

def stop_recording():
    global is_recording
    is_recording = False
    print("Recording stopped.")

# Create a simple Tkinter window
window = tk.Tk()
window.title("Speech Recognition")

# Start recording button
start_button = tk.Button(window, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

# Stop recording button
stop_button = tk.Button(window, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

# Start the GUI
window.mainloop()