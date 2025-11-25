# 🎬 Video Dubbing & Translation App

A powerful Flask web application that automatically translates and dubs videos into multiple languages using AI.

## Features

- 🎥 **Upload Videos**: Support for MP4, AVI, MOV, and MKV formats
- 🌍 **15+ Languages**: Translate to Spanish, French, German, Hindi, Tamil, Arabic, Japanese, Korean, Chinese, Portuguese, and more
- 🤖 **AI-Powered**: Uses Faster Whisper for accurate speech transcription
- 🎙️ **Natural Dubbing**: Google Text-to-Speech for high-quality voice generation
- 📊 **Real-time Progress**: Track processing status with live updates
- 💾 **Automatic Cleanup**: Temporary files are cleaned up automatically

## How It Works

1. **Upload**: User uploads a video file
2. **Extract**: Audio is extracted from the video
3. **Transcribe**: AI transcribes the audio to text
4. **Translate**: Text is translated to the target language
5. **Generate**: New audio is created in the target language
6. **Merge**: Dubbed audio is merged with the original video
7. **Download**: User downloads the dubbed video

## Installation

### Prerequisites

- Python 3.11+
- FFmpeg

### Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd video-dubbing-app

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install ffmpeg pkg-config

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at `http://localhost:5000`

## Deployment to Render

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Use these settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add system dependencies in Render:
   - Go to "Environment" → "Add Build Command"
   - Add: `apt-get install -y ffmpeg pkg-config`

## Usage

1. Open the web application
2. Select your target language from the dropdown
3. Upload your video (drag & drop or browse)
4. Click "Start Dubbing Process"
5. Wait for processing to complete
6. Download your dubbed video!

## Supported Languages

- Spanish (es)
- French (fr)
- German (de)
- Hindi (hi)
- Tamil (ta)
- Arabic (ar)
- Japanese (ja)
- Korean (ko)
- Chinese (zh-cn)
- Portuguese (pt)
- Italian (it)
- Russian (ru)
- Dutch (nl)
- Turkish (tr)
- Polish (pl)

## Technical Stack

- **Backend**: Flask
- **AI Transcription**: Faster Whisper
- **Translation**: translate library
- **Text-to-Speech**: Google TTS (gTTS)
- **Video Processing**: FFmpeg, MoviePy
- **Audio Processing**: pydub
- **Frontend**: Bootstrap 5, JavaScript

## Limitations

- Maximum file size: 500MB
- Processing time varies based on video length (typically 2-10 minutes)
- Supported formats: MP4, AVI, MOV, MKV

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
