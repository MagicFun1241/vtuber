FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl \
    flask soundfile

COPY tts-server.py /app/tts-server.py

EXPOSE 5002

CMD ["python3", "/app/tts-server.py"]
