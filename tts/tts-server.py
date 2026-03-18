"""KittenTTS server with Flask API."""

import io
import logging

import soundfile as sf
from flask import Flask, request, send_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

_tts = None

VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]


def get_tts():
    global _tts
    if _tts is None:
        from kittentts import KittenTTS

        logger.info("Loading KittenTTS model...")
        _tts = KittenTTS("KittenML/kitten-tts-micro-0.8")
        logger.info("Model loaded")
    return _tts


@app.route("/")
def index():
    return {"status": "ok", "model": "KittenTTS micro-0.8", "voices": VOICES}


@app.route("/api/tts", methods=["POST"])
def tts():
    text = request.values.get("text", "").strip()
    if not text:
        return {"error": "text is required"}, 400

    voice = request.values.get("voice", "Luna")
    if voice not in VOICES:
        return {"error": f"voice must be one of {VOICES}"}, 400

    logger.info("Text: %s", text)
    logger.info("Voice: %s", voice)

    try:
        model = get_tts()
        audio = model.generate(text=text, voice=voice)

        out = io.BytesIO()
        sf.write(out, audio, 24000, format="WAV", subtype="PCM_16")
        out.seek(0)

        return send_file(out, mimetype="audio/wav")
    except Exception as e:
        logger.error("TTS failed: %s", e)
        return {"error": str(e)}, 500


if __name__ == "__main__":
    get_tts()
    app.run(host="0.0.0.0", port=5002)
