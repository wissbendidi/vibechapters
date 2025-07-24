# 📺 VibeChapters Pro

> AI-powered smart video chapters + emotion-based highlight generation from YouTube videos

A full-stack ML tool that automatically generates intelligent chapter titles and timestamps from any YouTube video, with optional AI enhancement and emotion analysis.
By [Wissal Bendidi]

## ✨ Features

### 🎯 Core Features
- **Smart Chapter Generation**: Auto-generate meaningful chapter titles with timestamps
- **YouTube Integration**: Direct integration with YouTube transcript API
- **Dual Mode Operation**: Works with or without OpenAI API
- **Interactive UI**: Beautiful Streamlit interface with progress tracking
- **Timestamp Links**: Direct links to specific video moments

### 🚀 Premium Features (with OpenAI API)
- **AI-Generated Titles**: More creative and contextual chapter names
- **Better Context Understanding**: Advanced natural language processing
- **Enhanced Descriptions**: More engaging and descriptive titles

### 🆓 Free Features (no API required)
- **Keyword Extraction**: Smart keyword-based chapter generation
- **Sentiment Analysis**: Basic emotion detection using TextBlob
- **Chapter Organization**: Logical content segmentation
- **Analytics Dashboard**: Video statistics and insights

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vibechapters.git
   cd vibechapters
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

### 🔧 Optional: Enable Premium Features

1. **Get OpenAI API Key**
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new secret key

2. **Configure Environment**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

3. **Restart the app**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
vibechapters/
├── app.py                 # Main Streamlit application
├── get_transcript.py      # YouTube transcript extraction with fallbacks
├── split_text.py          # Text chunking logic
├── summarize.py           # Chapter title generation (OpenAI + free fallback)
├── emotion_detector.py    # Emotion analysis (optional)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🎮 Usage

### Basic Usage
1. Open the app in your browser
2. Paste a YouTube URL
3. Click "Generate Chapters"
4. View your smart chapters with timestamps!

### Demo Mode
- Enable "Demo Mode" in the sidebar to test with sample content
- Perfect for testing the app without needing a YouTube video

### Configuration Options
- **Words per chapter**: Adjust chapter length (50-200 words)
- **Analytics**: Enable detailed video statistics
- **Preview**: Show chapter content previews

## 🔧 API Configuration

### OpenAI Setup (Optional)
```bash
# .env file
OPENAI_API_KEY=sk-proj-your-key-here
```

### Fallback Behavior
- **With API**: Uses GPT-4o-mini for intelligent chapter titles
- **Without API**: Uses TextBlob + keyword extraction for free operation
- **Rate Limited**: Automatically falls back to free method

## 📊 How It Works

1. **Transcript Extraction**: 
   - YouTube Transcript API (primary)
   - yt-dlp subtitle extraction (fallback)
   - Rate limiting protection with retries

2. **Text Processing**:
   - Smart text chunking based on word count
   - Context-aware segment boundaries

3. **Chapter Generation**:
   - **Premium**: OpenAI GPT-4o-mini with custom prompts
   - **Free**: Keyword extraction + sentiment analysis + pattern matching

4. **UI Enhancement**:
   - Progress tracking
   - Interactive analytics
   - Direct YouTube timestamp links

## 🎯 Supported Video Types

- ✅ Educational content
- ✅ Tutorials and how-tos
- ✅ Presentations and talks
- ✅ Podcasts and interviews
- ✅ Any video with available captions

## 🚨 Troubleshooting

### Common Issues

**"Could not get transcript"**
- Video may not have captions enabled
- Try with a different video
- Use Demo Mode to test the app

**"Rate limited"**
- YouTube API temporary limit
- Wait 10-15 minutes and try again
- App automatically retries with delays

**"Invalid API key"**
- Check your `.env` file configuration
- Verify API key at OpenAI platform
- App works without API key in free mode

### Debug Mode
```bash
# Test transcript extraction
python get_transcript.py

# Test summarization
python summarize.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Requirements

### Core Dependencies
```
streamlit>=1.47.0
youtube-transcript-api>=0.6.1
textblob>=0.18.0
pandas>=2.3.1
plotly>=5.17.0
python-dotenv>=1.1.1
requests>=2.32.4
```

### Optional Dependencies
```
openai>=1.97.1          # For premium AI features
yt-dlp>=2024.12.13      # Enhanced transcript extraction
transformers>=4.44.2    # Advanced emotion analysis
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenAI](https://openai.com/) for GPT API
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for subtitle fallback

## 🔮 Roadmap

- [ ] Audio-based emotion detection
- [ ] Video frame analysis for visual cues
- [ ] Export chapters to various formats
- [ ] Batch processing multiple videos
- [ ] Chapter thumbnail generation
- [ ] Advanced analytics dashboard

---

**Built with ❤️ for content creators and video enthusiasts**

[⭐ Star this repo](https://github.com/wissbendidi/vibechapters) if you find it useful!