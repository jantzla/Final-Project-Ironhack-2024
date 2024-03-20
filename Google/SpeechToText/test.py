from google.cloud import speech_v1 as sr
import os
import time
import pyaudio
import wave

audio_file = r'C:\Users\ljant\Desktop\Ironhack\Projects\Final-Project-Ironhack-2024\Google\SpeechToText\audio_file.wav'

def control_audio(command):
    if command == 'play':
        os.startfile(audio_file)
    elif command == 'pause':
        os.system("powershell -c (New-Object -ComObject WMPlayer.OCX).controls.pause()")
    elif command == 'stop':
        os.system("powershell -c (New-Object -ComObject WMPlayer.OCX).controls.stop()")
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
    with open(WAVE_OUTPUT_FILENAME, 'rb') as audio_file:
        content = audio_file.read()

    audio = sr.RecognitionAudio(content=content)
    config = sr.RecognitionConfig(
        encoding=sr.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        command = result.alternatives[0].transcript
        process_transcription(command)

if __name__ == "__main__":
    while True:
        capture_user_commands()
        time.sleep(1)