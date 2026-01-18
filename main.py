from flask import Flask, render_template,request, redirect, url_for

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def file_upload():
    file = request.files.get('file')

    if not file or file.filename == "":
        return "No file selected", 400

    # save file (example)
    file.save(f"uploads/{file.filename}")

    TTS()

    return redirect(url_for('index'))

def TTS():

        polly = Session(profile_name="rajeev_dev").client("polly")

        response = polly.synthesize_speech(
            Text="Hello world!",
            OutputFormat="mp3",
            VoiceId="Joanna"
        )

        with open("speech.mp3", "wb") as f:
            f.write(response["AudioStream"].read())

if __name__ == '__main__':
    app.run()