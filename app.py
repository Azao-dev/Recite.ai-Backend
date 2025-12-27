from flask import Flask, request, jsonify
from flask_cors import CORS
from glob import glob
from google.cloud import texttospeech
from google.oauth2 import service_account
from PIL import Image

import os
import pytesseract 
import base64
import json

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)

cred = '/etc/secrets/google_creds.json'

try: #try extracting the json file
    with open(cred, "r") as c:
        credentials_env = c.read
except: 
    print("could not read credentials")
        
if credentials_env: #actual deployment
    print("credentials exist")
    credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_env))
else: # Local testing
    print("credentials not found")
    credentials = service_account.Credentials.from_service_account_file("google_creds.json")

client = texttospeech.TextToSpeechClient(credentials=credentials) 
# To activate venv, use . venv\scripts\activate
# To run this, use python -m flask run -p 8080

@app.route("/", methods=["POST"])
def image_to_text():
    """
    image = Image.open("daisy.png") # Test function to make sure pytesseract would work properly
    text = pytesseract.image_to_string(image)
    print("Text: ", text)
    return text
    """
    print("Converting image to text")

    if request.method == 'POST':
        print("Checking for Image")
        print("Request files: ", request.files)
        print("Request content type: ", request.content_type)

        if 'image' not in request.files:
            return 'No image', 400

        image_file = request.files['image']
        print("image found")

        if image_file:
            print("file found")
            client = texttospeech.TextToSpeechClient()
            print("tts 1 check")
            tts_voice = texttospeech.VoiceSelectionParams(
                language_code = "en-US",
                ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL
            )
            print("tts created")
            
            try: 
                print("making text response")
                image = Image.open(image_file.stream)
                text = pytesseract.image_to_string(image)
                
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )

                inp = texttospeech.SynthesisInput(text=text)

                response = client.synthesize_speech(
                    input = inp,
                    voice = tts_voice,
                    audio_config = audio_config
                )

                audio_64 = base64.b64encode(response.audio_content).decode("utf-8")

                print(text)

                return jsonify({
                    "audio": audio_64,
                    "text": text,
                    "status": "ITT and TTS Successful"
                })

            except Exception as e:
                print("error found")
                return e

if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=True, threaded=True)



















