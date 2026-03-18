# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Microservices for vtuber infrastructure: a TTS (text-to-speech) service and a Whisper (speech-to-text) service, each packaged as a Docker image and published to GHCR.

## Architecture

Two independent services, no shared code:

- **tts/** — Python Flask server using KittenTTS. Serves `POST /api/tts` (params: `text`, `voice`) returning WAV audio on port 5002.
- **whisper/** — Multi-stage Docker build that compiles [whisper.cpp](https://github.com/ggml-org/whisper.cpp) from source. Runtime is just the compiled binary + shared libs.

## Build & Deploy

All builds happen via GitHub Actions (`.github/workflows/build.yml`) on push to `main`. Each service has a `VERSION` file containing a semver string. Images are pushed to:

```
ghcr.io/magicfun1241/vtuber/tts:<version>
ghcr.io/magicfun1241/vtuber/whisper:<version>
```

To release a new version, bump the `VERSION` file in the relevant service directory.

## Local Docker Builds

```bash
docker build -t vtuber/tts tts/
docker build -t vtuber/whisper whisper/
```

## Whisper Build Notes

The whisper Dockerfile targets broad CPU compatibility: AVX is on, but AVX2/FMA/F16C/NATIVE are disabled. The runtime stage needs only the compiled binaries and shared libs — `libgomp1` is required at runtime but not installed by default (it was recently added).
