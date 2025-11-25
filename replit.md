# Video Dubbing & Translation App

## Overview
A Flask-based web application that automatically translates and dubs videos into multiple languages. Users can upload a video, select a target language, and the app will extract audio, transcribe it, translate the text, generate dubbed audio using text-to-speech, and merge it back with the video.

## Recent Changes
- **November 25, 2025**: Initial project setup
  - Created Flask web application with video upload functionality
  - Implemented automated video dubbing pipeline with Whisper transcription
  - Added support for 15+ target languages (Spanish, French, German, Hindi, Tamil, Arabic, Japanese, Korean, Chinese, Portuguese, Italian, Russian, Dutch, Turkish, Polish)
  - Built responsive UI with drag-and-drop upload and real-time progress tracking
  - Configured for deployment on Render

## Features
- **Video Upload**: Drag-and-drop interface supporting MP4, AVI, MOV, MKV formats (up to 500MB)
- **Multi-language Support**: Translate and dub videos into 15+ languages
- **Automated Pipeline**:
  1. Extract audio from video using FFmpeg
  2. Transcribe audio using Faster Whisper AI model
  3. Generate subtitle files (SRT format)
  4. Translate subtitles to target language
  5. Generate dubbed audio using Google Text-to-Speech
  6. Merge dubbed audio with original video
- **Real-time Progress**: Live status updates during processing
- **Download**: Download completed dubbed videos

## Project Architecture
```
.
├── app.py                 # Flask application with routes
├── video_processor.py     # Core video processing pipeline
├── templates/
│   └── index.html        # Frontend UI
├── static/
│   ├── style.css         # Styles
│   └── script.js         # Client-side logic
├── uploads/              # Temporary uploaded videos
├── outputs/              # Processed videos
├── temp/                 # Temporary processing files
└── requirements.txt      # Python dependencies
```

## Technology Stack
- **Backend**: Flask (Python web framework)
- **Video Processing**: FFmpeg, MoviePy
- **AI Transcription**: Faster Whisper
- **Translation**: translate library
- **Text-to-Speech**: Google TTS (gTTS)
- **Audio Processing**: pydub
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5

## Key Dependencies
- faster-whisper: Speech-to-text transcription
- ffmpeg-python: Audio/video manipulation
- gTTS: Text-to-speech audio generation
- moviepy: Video editing and audio merging
- pysrt: Subtitle file handling
- translate: Text translation between languages

## Usage
1. Open the web application
2. Select target language from dropdown
3. Upload or drag-and-drop a video file
4. Click "Start Dubbing Process"
5. Wait for processing (progress shown in real-time)
6. Download the dubbed video when complete

## Deployment Notes
- Requires FFmpeg system dependency
- Processing time varies based on video length (typically 2-10 minutes)
- Temporary files are automatically cleaned up after processing
- Development server runs on port 5000
- For production deployment, use a WSGI server like Gunicorn

## User Preferences
- Clean, modern UI with gradient backgrounds
- Real-time progress tracking preferred
- Automatic file cleanup for storage efficiency
