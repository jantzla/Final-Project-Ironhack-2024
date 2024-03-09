import os, io
from google.cloud import texttospeech
from google.cloud import texttospeech_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\ljant\Desktop\Ironhack\Projects\Final-Project-Ironhack-2024\Google\TextToSpeech\AccessKey_API.json'
client = texttospeech_v1.TextToSpeechClient()


with open("docText.txt", "r") as file:
    text = file.read()

synthesis_input = texttospeech_v1.SynthesisInput(text = text)


# Configurating the voice

'''
Voice 1
'''
voice1 = texttospeech_v1.VoiceSelectionParams(
  language_code= "en-US",
  name = "en-US-Neural2-C"
)

# print(client.list_voices())


# Configurating the output file
#https://cloud.google.com/text-to-speech/docs/reference/rest/v1/AudioConfig
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding = texttospeech_v1.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input = synthesis_input,
    voice = voice1,
    audio_config = audio_config
)

with open('audio file.mp3', 'wb') as output:
    output.write(response.audio_content)