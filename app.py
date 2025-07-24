import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from get_transcript import get_transcript, get_demo_transcript
from split_text import split_text
from summarize import summarize_chunk, get_summarization_status
from urllib.parse import urlparse, parse_qs
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="VibeChapters Pro",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check if Gemini is configured
api_key = os.getenv("GEMINI_API_KEY")
GEMINI_CONFIGURED = bool(api_key and api_key.strip() and not api_key.startswith("your_"))

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .chapter-item {
        border-left: 4px solid #4ECDC4;
        padding-left: 1rem;
        margin: 1rem 0;
        background: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
    }
    .api-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
    }
    .api-enabled {
        background-color: #d4edda;
        color: #155724;
    }
    .api-disabled {
        background-color: #e2f3ff;
        color: #0c5460;
    }
    .gemini-badge {
        background: linear-gradient(45deg, #4285f4, #34a853);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">📺 VibeChapters Pro</h1>', unsafe_allow_html=True)
st.markdown("*AI-powered smart chapters from YouTube videos* <span class='gemini-badge'>🤖 Powered by Gemini</span>", unsafe_allow_html=True)

# API Status indicator
method_type, method_desc = get_summarization_status()
if method_type == "premium":
    st.markdown('<div class="api-status api-enabled">✅ Google Gemini API Configured - Premium Features Available (FREE!)</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="api-status api-disabled">ℹ️ Using Free Mode - Smart Keyword-Based Chapters</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    max_words = st.slider("Words per chapter", 50, 200, 100)
    
    st.header("🎬 Content Source")
    demo_mode = st.checkbox("Demo Mode", help="Use sample content for testing")
    
    st.header("📊 Display Options")
    show_analytics = st.checkbox("Show analytics", True)
    show_preview = st.checkbox("Show chapter previews", False)
    
    # API Configuration Section
    st.header("🔧 API Setup")
    if not GEMINI_CONFIGURED:
        st.info("ℹ️ Using free mode")
        st.markdown("""
        **To enable premium AI features:**
        1. Get FREE API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Create `.env` file in project root
        3. Add: `GEMINI_API_KEY=your_key_here`
        4. Restart the app
        
        **🎉 Gemini is FREE** with generous limits:
        - 15 requests/minute
        - 1,500 requests/day
        - No credit card required!
        """)
    else:
        st.success("✅ Google Gemini API configured")
        st.info("🤖 Premium AI chapter generation enabled")
    
    st.markdown("---")
    st.markdown("**✅ Free Features:**")
    st.markdown("- Smart keyword extraction")
    st.markdown("- Chapter organization") 
    st.markdown("- YouTube timestamp links")
    st.markdown("- Basic analytics")
    
    if GEMINI_CONFIGURED:
        st.markdown("**🚀 Premium Features (FREE!):**")
        st.markdown("- 🤖 AI-generated titles with Gemini")
        st.markdown("- 🧠 Better context understanding")
        st.markdown("- ✨ More creative descriptions")
        st.markdown("- 🆓 Completely FREE with generous limits!")

# Main input
col1, col2 = st.columns([3, 1])
with col1:
    video_url = st.text_input(
        "🔗 Enter YouTube URL:", 
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste any YouTube video URL here"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    generate_button = st.button("🚀 Generate Chapters", type="primary")

if generate_button and (video_url or demo_mode):
    # Extract video ID
    video_id = None
    if video_url and not demo_mode:
        query = urlparse(video_url)
        if query.hostname == 'youtu.be':
            video_id = query.path[1:]
        elif query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                video_id = parse_qs(query.query).get('v', [None])[0]
            elif query.path[:7] == '/embed/':
                video_id = query.path.split('/')[2]
            else:
                video_id = None
        else:
            video_id = None

    if not video_id and not demo_mode:
        st.error("❌ Invalid YouTube URL. Please check the format or enable Demo Mode.")
    else:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Get transcript
            status_text.text("📝 Fetching transcript...")
            progress_bar.progress(0.2)
            
            if demo_mode:
                st.info("🎬 Using demo content to showcase features")
                text, transcript = get_demo_transcript("demo")
            else:
                text, transcript = get_transcript(video_id)
            
            if not text:
                st.error("❌ Could not get transcript. The video might not have captions available.")
                st.info("💡 Try enabling Demo Mode to test the app functionality")
            else:
                # Step 2: Split into chunks
                status_text.text("✂️ Splitting into chapters...")
                progress_bar.progress(0.4)
                
                chunks = split_text(text, max_words=max_words)
                
                # Step 3: Generate chapters
                method = "AI-powered" if method_type == "premium" else "keyword-based"
                ai_provider = " (Gemini)" if method_type == "premium" else ""
                status_text.text(f"🤖 Generating {len(chunks)} {method} chapters{ai_provider}...")
                progress_bar.progress(0.6)
                
                chapter_titles = []
                for i, chunk in enumerate(chunks):
                    title = summarize_chunk(chunk)
                    chapter_titles.append(title)
                    progress_bar.progress(0.6 + (i + 1) / len(chunks) * 0.4)
                
                progress_bar.progress(1.0)
                status_text.text("✅ Complete!")
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()
                
                # Display results
                success_msg = f"🎉 Successfully generated {len(chapter_titles)} chapters using {method} generation!"
                if method_type == "premium":
                    success_msg += " 🤖 (Powered by FREE Gemini AI)"
                st.success(success_msg)
                
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["📑 Chapters", "📊 Analytics", "⚙️ Settings"])
                
                with tab1:
                    st.subheader("📍 Smart Chapters")
                    
                    for i, title in enumerate(chapter_titles):
                        start_time = transcript[i * max_words]['start'] if i * max_words < len(transcript) else 0
                        minutes, seconds = divmod(int(start_time), 60)
                        
                        # Chapter card
                        st.markdown(f"""
                        <div class="chapter-item">
                            <h4>{title}</h4>
                            <p>🕐 {minutes:02d}:{seconds:02d}</p>
                            {f'<a href="https://www.youtube.com/watch?v={video_id}&t={int(start_time)}s" target="_blank">▶️ Jump to timestamp</a>' if video_id and not demo_mode else '<small>Demo content - no video link available</small>'}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if show_preview:
                            with st.expander(f"👀 Preview Chapter {i+1}"):
                                preview = chunks[i][:200] + "..." if len(chunks[i]) > 200 else chunks[i]
                                st.text(preview)
                
                with tab2:
                    if show_analytics:
                        st.subheader("📈 Video Analytics")
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("📑 Chapters", len(chapter_titles))
                        
                        with col2:
                            video_length_min = int(transcript[-1]['start']) // 60 if transcript else 0
                            st.metric("⏱️ Length", f"{video_length_min} min")
                        
                        with col3:
                            total_words = len(text.split()) if text else 0
                            st.metric("📝 Words", f"{total_words:,}")
                        
                        with col4:
                            avg_chapter_length = total_words // len(chunks) if chunks else 0
                            st.metric("📊 Avg Chapter", f"{avg_chapter_length} words")
                        
                        # Chapter length distribution
                        if chunks:
                            st.subheader("📊 Chapter Length Distribution")
                            chapter_lengths = [len(chunk.split()) for chunk in chunks]
                            
                            fig = px.bar(
                                x=range(1, len(chapter_lengths) + 1),
                                y=chapter_lengths,
                                title="Words per Chapter",
                                labels={'x': 'Chapter Number', 'y': 'Word Count'}
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Enable 'Show analytics' in the sidebar to see detailed statistics.")
                
                with tab3:
                    st.subheader("⚙️ Configuration & Tips")
                    
                    st.markdown("**📝 Chapter Length Optimization:**")
                    st.markdown("- **50-75 words**: Short, focused chapters")
                    st.markdown("- **75-125 words**: Balanced chapters (recommended)")
                    st.markdown("- **125+ words**: Longer, detailed chapters")
                    
                    st.markdown("**🎯 Best Results:**")
                    st.markdown("- Videos with clear speech and good audio")
                    st.markdown("- Educational or tutorial content")
                    st.markdown("- Videos with available captions/transcripts")
                    
                    st.markdown("**🔧 Current Configuration:**")
                    st.write(f"- Mode: {method_desc}")
                    st.write(f"- Words per chapter: {max_words}")
                    st.write(f"- Total chapters generated: {len(chapter_titles)}")
                    
                    if method_type == "premium":
                        st.markdown("**🤖 AI Provider:**")
                        st.success("Google Gemini 1.5 Flash (FREE)")
                        st.info("Enjoying unlimited AI-powered chapters at no cost!")
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Try Demo Mode to test the app, or check if the video has captions available.")

elif generate_button:
    st.warning("⚠️ Please enter a YouTube URL or enable Demo Mode to test the app.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🚀 Features:**")
    st.markdown("- Smart chapter generation")
    st.markdown("- YouTube integration")
    st.markdown("- Free & premium modes")

with col2:
    st.markdown("**💻 Tech Stack:**")
    st.markdown("- Streamlit")
    st.markdown("- Google Gemini API (FREE)")
    st.markdown("- YouTube Transcript API")

with col3:
    st.markdown("**📋 Status:**")
    method_type, method_desc = get_summarization_status()
    st.markdown(f"- Mode: {method_type.title()}")
    st.markdown(f"- API: {'🤖 Gemini (Free)' if GEMINI_CONFIGURED else '💡 Free mode'}")
    st.markdown("- Version: 2.0.0")

st.markdown("<div style='text-align: center; margin-top: 2rem;'><em>Built with ❤️ using FREE Google Gemini AI</em></div>", unsafe_allow_html=True)