from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return "HM Voice Lab API is Running Successfully!"

@app.route('/generate-voice', methods=['POST'])
def generate_voice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        text = data.get('text', '').strip()
        voice = data.get('voice', 'bn-BD-NabanitaNeural')
        style = data.get('style', 'default')  # romantic, motivational, emotional, sad, default

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Adjust rate and pitch based on style
        rate = "+0%"
        pitch = "+0Hz"

        if style == "romantic":
            rate = "-8%"
            pitch = "+2Hz"
        elif style == "motivational":
            rate = "+5%"
            pitch = "-2Hz"
        elif style == "emotional" or style == "sad":
            rate = "-15%"
            pitch = "-4Hz"

        filename = f"voice_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join('/tmp', filename)

        async def create_audio():
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await communicate.save(filepath)

        asyncio.run(create_audio())

        if os.path.exists(filepath):
            return send_file(filepath, mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'Audio generation failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
