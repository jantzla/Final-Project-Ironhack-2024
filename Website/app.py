# Libaries
from flask import Flask, render_template, request, redirect, url_for, session
import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
from google.cloud import texttospeech_v1
import uuid

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_key')

vision_client = vision.ImageAnnotatorClient()
text_to_speech_client = texttospeech_v1.TextToSpeechClient()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

AUDIO_FOLDER = os.path.join(app.root_path, 'static', 'audio')

if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'pdf'}

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Clear previous session data
        session.pop('audio_files', None)
        session.pop('adjusted_transcripts', None)
        session.pop('current_index', None)

        files = request.files.getlist('imagefiles')
        filenames = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                filenames.append(filename)
        
        session['filenames'] = filenames
        session['current_index'] = 0
        
        return redirect(url_for('adjust_transcription'))

    return render_template('index.html')

@app.route('/adjust_transcription', methods=['GET'])
def adjust_transcription():
    index = session.get('current_index', 0)
    filenames = session.get('filenames', [])
    
    if index >= len(filenames):
        return redirect(url_for('result_page'))
    
    filename = filenames[index]
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    docText, confidence_score = transcribe_image(image_path)
    
    if request.method == 'POST':
        adjusted_transcript = request.form.get('transcript')
        unique_audio_filename = save_transcript_as_audio(adjusted_transcript, "output_" + str(index))
        session['current_index'] = index + 1
        return redirect(url_for('adjust_transcription'))
    
    return render_template('transcription.html', transcription=docText, confidence_score=confidence_score, filename=filename)


def transcribe_image(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = vision_client.document_text_detection(image=image)
    docText = response.full_text_annotation.text

    block_confidences = [block.confidence for page in response.full_text_annotation.pages for block in page.blocks]
    average_confidence = round(sum(block_confidences) / len(block_confidences) * 100, 2) if block_confidences else 0

    return docText, average_confidence

@app.route('/submit-adjusted-transcript', methods=['POST'])
def submit_adjusted_transcript():
    if 'transcript' not in request.form:
        return redirect(url_for('upload_file', message='No transcript submitted'))
    
    adjusted_transcript = request.form['transcript']

    if 'adjusted_transcripts' not in session:
        session['adjusted_transcripts'] = []
    session['adjusted_transcripts'].append(adjusted_transcript)

    unique_audio_filename = save_transcript_as_audio(adjusted_transcript, "output_" + str(uuid.uuid4().hex))

    if 'audio_files' not in session:
        session['audio_files'] = []
    session['audio_files'].append(unique_audio_filename)

    session['adjusted_transcript'] = adjusted_transcript

    current_index = session.get('current_index', 0) + 1
    session['current_index'] = current_index 
    filenames = session.get('filenames', [])
    
    if current_index < len(filenames):
        return redirect(url_for('adjust_transcription'))
    else:
        session.modified = True
        return redirect(url_for('result_page'))


def save_transcript_as_audio(text, filename):
    client = texttospeech_v1.TextToSpeechClient()
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    
    # Retrieve the selected voice from the form
    voice_name = request.form.get('voiceName', 'en-US-Neural2-C')  # Default to 'en-US-Neural2-C'
    
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )
    audio_config = texttospeech_v1.AudioConfig(audio_encoding=texttospeech_v1.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    unique_filename = f"{filename}_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, unique_filename)
    with open(filepath, 'wb') as output:
        output.write(response.audio_content)
    return unique_filename

@app.route('/result')
def result_page():
    audio_filenames = session.get('audio_files', [])
    adjusted_transcripts = session.get('adjusted_transcripts', [])

    return render_template('result.html', audio_files=audio_filenames, transcripts=adjusted_transcripts)

@app.route('/start_over')
def start_over():
    # Clear session data
    session.pop('audio_files', None)
    session.pop('adjusted_transcripts', None)
    session.pop('current_index', None)

    # Redirect to the beginning
    return redirect(url_for('upload_files'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
