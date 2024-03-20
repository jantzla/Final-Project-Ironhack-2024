import os
import time
import pyaudio
import wave
import speech_recognition as sr

audio_file = r'C:\Users\ljant\Desktop\Ironhack\Projects\Final-Project-Ironhack-2024\Google\SpeechToText\audio_file.wav'

def control_audio(command):
    if command == 'play':
        os.startfile(audio_file)
    elif command == 'pause':
        os.system("TASKKILL /F /IM wmplayer.exe")  # Terminate the Windows Media Player process
    elif command == 'stop':
        os.system("TASKKILL /F /IM wmplayer.exe")  # Terminate the Windows Media Player process
    else:
        print('Unrecognized command:', command)

def process_transcription(transcription):
    print('Transcription:', transcription)
    control_audio(transcription.lower())

def capture_user_commands():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "temp.wav"

    audio = pyaudio.PyAudio()

    # Start recording
    print("Recording...")
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Transcribe recorded audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            command = recognizer.recognize_google(audio_data).lower()
            print("Transcription:", command)
            process_transcription(command)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    while True:
        capture_user_commands()
        time.sleep(1)  # Add a short delay to avoid constantly listening
