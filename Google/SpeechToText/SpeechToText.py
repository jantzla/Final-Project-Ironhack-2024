import io
from google.oauth2 import service_account
from google.cloud import speech

client_file = r'C:\Users\ljant\Desktop\Ironhack\Projects\Final-Project-Ironhack-2024\Google\SpeechToText\AccessKey_API.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials = credentials)

# Load the audio file
# Test 1
audio_file = r'C:\Users\ljant\Desktop\Ironhack\Projects\Final-Project-Ironhack-2024\Google\SpeechToText\audio file.wav'
with io.open(audio_file, 'rb') as f:
    content = f.read()
    audio = speech.RecognitionAudio(content = content)

# Configure the Recognition
config = speech.RecognitionConfig(
    encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz = 24000,
    language_code = 'en-US',
    model = 'command_and_search'
)

# Transcripe the audio file
response = client.recognize(config = config, audio = audio)
for result in response.results:
    print(result.alternatives[0].transcript)