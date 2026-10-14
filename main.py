from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "HM Voice Lab API is Running!"

@app.route('/generate-voice', methods=['POST'])
def generate_voice():
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice = data.get('voice', 'bn-BD-NabanitaNeural')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        filename = f"voice_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join('/tmp', filename)

        async def create_audio():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(filepath)

        asyncio.run(create_audio())

        return send_file(filepath, mimetype='audio/mpeg')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
