import streamlit as st
from get_transcript import get_demo_transcript
from split_text import split_text
from summarize import summarize_chunk, get_summarization_status
import time

st.set_page_config(page_title="VibeChapters Debug", page_icon="🔧")

st.title("🔧 VibeChapters Debug Mode")

# Show current status
method_type, method_desc = get_summarization_status()
if method_type == "premium":
    st.success(f"✅ {method_desc}")
else:
    st.info(f"ℹ️ {method_desc} (No OpenAI API key or quota exceeded)")

st.markdown("---")
st.header("Demo Test")

if st.button("🎬 Test Demo Mode"):
    st.write("**Step 1: Getting demo transcript...**")
    
    try:
        text, transcript = get_demo_transcript("demo")
        st.success(f"✅ Got {len(text)} characters of demo text")
        
        # Show preview
        with st.expander("Preview demo text"):
            st.text(text[:300] + "...")
        
        st.write("**Step 2: Splitting into chunks...**")
        chunks = split_text(text, max_words=100)
        st.success(f"✅ Created {len(chunks)} chunks")
        
        # Show chunk preview
        with st.expander("Preview chunks"):
            for i, chunk in enumerate(chunks[:3]):  # Show first 3
                st.write(f"**Chunk {i+1}:** {chunk[:100]}...")
        
        st.write("**Step 3: Generating chapter titles...**")
        
        # Test each chunk individually to see where it fails
        chapter_titles = []
        progress_bar = st.progress(0)
        
        for i, chunk in enumerate(chunks):
            st.write(f"Processing chunk {i+1}/{len(chunks)}...")
            
            try:
                title = summarize_chunk(chunk)
                chapter_titles.append(title)
                st.write(f"✅ **{title}**")
            except Exception as e:
                st.error(f"❌ Error in chunk {i+1}: {str(e)}")
                chapter_titles.append(f"Error: Chunk {i+1}")
            
            progress_bar.progress((i + 1) / len(chunks))
        
        st.write("**Step 4: Final Results**")
        
        if chapter_titles:
            st.success(f"🎉 Generated {len(chapter_titles)} chapter titles!")
            
            for i, (title, chunk) in enumerate(zip(chapter_titles, chunks)):
                start_time = transcript[i * 100]['start'] if i * 100 < len(transcript) else 0
                minutes, seconds = divmod(int(start_time), 60)
                
                st.markdown(f"**{i+1}. {title}**")
                st.markdown(f"🕐 {minutes:02d}:{seconds:02d}")
                
                with st.expander(f"Content preview {i+1}"):
                    st.text(chunk[:200] + "..." if len(chunk) > 200 else chunk)
                
                st.markdown("---")
        else:
            st.error("❌ No chapter titles were generated")
    
    except Exception as e:
        st.error(f"❌ Demo test failed: {str(e)}")
        st.write("**Error details:**")
        import traceback
        st.code(traceback.format_exc())

st.markdown("---")
st.header("Manual Tests")

# Test individual components
col1, col2 = st.columns(2)

with col1:
    if st.button("🧪 Test Summarizer Only"):
        test_text = "Welcome to this amazing tutorial where we'll explore artificial intelligence and machine learning. This is incredibly exciting content."
        
        try:
            title = summarize_chunk(test_text)
            st.success(f"✅ Title: **{title}**")
        except Exception as e:
            st.error(f"❌ Summarizer failed: {str(e)}")

with col2:
    if st.button("🧪 Test Text Splitter"):
        test_text = "This is a test. " * 50  # 100 words
        
        try:
            chunks = split_text(test_text, max_words=20)
            st.success(f"✅ Created {len(chunks)} chunks")
            for i, chunk in enumerate(chunks[:2]):
                st.write(f"Chunk {i+1}: {chunk[:50]}...")
        except Exception as e:
            st.error(f"❌ Text splitter failed: {str(e)}")

# Debug info
st.markdown("---")
st.header("🔍 Debug Information")

st.write("**Python Environment:**")
import sys
st.code(f"Python version: {sys.version}")

st.write("**Installed packages:**")
try:
    import openai
    st.write("✅ OpenAI installed")
except ImportError:
    st.write("❌ OpenAI not installed")

try:
    import textblob
    st.write("✅ TextBlob installed")
except ImportError:
    st.write("❌ TextBlob not installed")

try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.write(f"✅ API key found: {api_key[:10]}...")
    else:
        st.write("ℹ️ No API key in environment")
except Exception as e:
    st.write(f"❌ Environment error: {e}")

st.markdown("---")
st.info("Use this debug app to identify exactly where the issue occurs!")