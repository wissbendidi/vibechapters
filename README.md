# 📺 VibeChapters Pro

> AI-powered smart video chapters from YouTube videos using **Google Gemini** (FREE!)

Generate intelligent chapter titles and timestamps from any YouTube video with optional AI enhancement using Google's free Gemini API.

## ✨ Features

### 🎯 Core Features
- **Smart Chapter Generation**: Auto-generate meaningful chapter titles with timestamps
- **YouTube Integration**: Direct integration with YouTube transcript API
- **Dual Mode Operation**: Works with or without Google Gemini API
- **Interactive UI**: Beautiful Streamlit interface with progress tracking
- **Timestamp Links**: Direct links to specific video moments

### 🚀 Premium Features (with FREE Gemini API)
- **AI-Generated Titles**: More creative and contextual chapter names using Google Gemini
- **Better Context Understanding**: Advanced natural language processing
- **Enhanced Descriptions**: More engaging and descriptive titles
- **Completely FREE**: No credit card required, generous daily limits!

### 🆓 Free Features (no API required)
- **Keyword Extraction**: Smart keyword-based chapter generation
- **Sentiment Analysis**: Basic emotion detection using TextBlob
- **Chapter Organization**: Logical content segmentation
- **Analytics Dashboard**: Video statistics and insights

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/vibechapters.git
cd vibechapters
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Optional: Enable FREE Premium Features 🎉

1. **Get FREE Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with Google account
   - Click "Create API Key"
   - Copy your free API key

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add: GEMINI_API_KEY=your_api_key_here
   ```

3. **Restart the app**
   ```bash
   streamlit run app.py
   ```

## 🎮 Usage

### Demo Mode (Test Immediately)
1. Enable "Demo Mode" in the sidebar
2. Click "Generate Chapters"
3. See sample AI-generated chapters instantly!

### Real YouTube Videos
1. Paste any YouTube URL
2. Click "Generate Chapters"
3. Get smart chapters with clickable timestamps
4. Enjoy FREE AI-powered titles with Gemini!

## 🆓 Why Gemini?

**Google Gemini is completely FREE** with generous limits:
- ✅ **15 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **No credit card required**
- ✅ **No billing setup needed**
- ✅ **Better than many paid alternatives**

Compare this to OpenAI which requires:
- ❌ Credit card for API access
- ❌ Pay per token usage
- ❌ Can get expensive quickly

## 🛠️ Technical Details

### How It Works
1. **Transcript Extraction**: 
   - YouTube Transcript API (primary)
   - yt-dlp subtitle extraction (fallback)
   - Rate limiting protection with retries

2. **Text Processing**:
   - Smart text chunking based on word count
   - Context-aware segment boundaries

3. **Chapter Generation**:
   - **Premium**: Google Gemini 1.5 Flash with custom prompts
   - **Free**: Keyword extraction + sentiment analysis + pattern matching

4. **UI Enhancement**:
   - Progress tracking
   - Interactive analytics
   - Direct YouTube timestamp links

### Fallback System
- **With Gemini API**: Uses AI for creative, contextual titles
- **Without API**: Uses smart keyword extraction (still very good!)
- **Rate Limited**: Automatically falls back to free method
- **Always Works**: Never completely fails

## 📁 Project Structure

```
vibechapters/
├── app.py                 # Main Streamlit application
├── get_transcript.py      # YouTube transcript extraction with fallbacks
├── split_text.py          # Text chunking logic
├── summarize.py           # Chapter title generation (Gemini + free fallback)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

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

**"Gemini API error"**
- Check your `.env` file configuration
- Verify API key at [Google AI Studio](https://aistudio.google.com/app/apikey)
- App works without API key in free mode

### Debug Mode
```bash
# Test transcript extraction
python get_transcript.py

# Test summarization
python summarize.py
```

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
google-generativeai>=0.8.3  # For FREE premium AI features
yt-dlp>=2024.12.13          # Enhanced transcript extraction
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Google Gemini](https://ai.google.dev/) for FREE AI capabilities
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for subtitle fallback

## 🔮 Roadmap

- [ ] Batch processing multiple videos
- [ ] Export chapters to various formats (JSON, CSV, SRT)
- [ ] Video thumbnail generation for chapters
- [ ] Advanced analytics dashboard
- [ ] Integration with other video platforms

---

**Built with ❤️ for content creators using FREE AI** 🚀

[⭐ Star this repo](https://github.com/wissbendidi/vibechapters) if you find it useful!

### 🎉 Get Started Now - It's FREE!
1. `git clone` this repo
2. `pip install -r requirements.txt`
3. `streamlit run app.py`
4. Get your [FREE Gemini API key](https://aistudio.google.com/app/apikey)
5. Enjoy unlimited AI-powered chapter generation!