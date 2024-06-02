from flask import Flask, request, jsonify, url_for
from gtts import gTTS
import os
import tempfile
import shutil

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_text_to_audio():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    tamil_text = data['text']
    tts = gTTS(text=tamil_text, lang='ta')
    
    # Use tempfile to handle file saving and cleanup
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        tts.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name

    # Move the temporary file to a static directory
    permanent_file_dir = os.path.join(app.root_path, 'static', 'audio')
    os.makedirs(permanent_file_dir, exist_ok=True)
    permanent_file_path = os.path.join(permanent_file_dir, 'Tamil-Audio.mp3')
    shutil.move(temp_audio_file_path, permanent_file_path)

    # Generate the URL for the audio file
    file_url = url_for('static', filename=f'audio/Tamil-Audio.mp3', _external=True)

    return jsonify({'message': 'File created successfully', 'file_url': file_url})

if __name__ == '__main__':
    app.run(debug=True)
