from dotenv import load_dotenv
import os
import re
from textblob import TextBlob

load_dotenv()  # Load environment variables from .env

# Global state for Gemini availability
_gemini_available = False
_gemini_client = None
_quota_exceeded = False

def _initialize_gemini():
    """Initialize Gemini client if possible"""
    global _gemini_available, _gemini_client, _quota_exceeded
    
    if _quota_exceeded:
        return False
        
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key.strip() and not api_key.startswith("your_"):
            genai.configure(api_key=api_key)
            _gemini_client = genai.GenerativeModel('gemini-1.5-flash')
            _gemini_available = True
            print("✅ Google Gemini configured and ready")
            return True
        else:
            print("ℹ️ Gemini API key not found or invalid")
            return False
    except ImportError:
        print("ℹ️ Google Generative AI library not installed")
        return False
    except Exception as e:
        print(f"⚠️ Gemini setup failed: {e}")
        return False

# Initialize on import
_initialize_gemini()

def summarize_chunk(chunk):
    """
    Generate a short chapter title using Gemini or free fallback
    """
    global _gemini_available, _quota_exceeded
    
    # Try Gemini if available and not quota exceeded
    if _gemini_available and not _quota_exceeded and _gemini_client:
        try:
            return _summarize_chunk_gemini(chunk)
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str or "limit" in error_str:
                print("⚠️ Gemini quota exceeded, switching to free mode")
                _quota_exceeded = True
            else:
                print(f"⚠️ Gemini error: {str(e)[:100]}...")
            
            return _summarize_chunk_free(chunk)
    else:
        return _summarize_chunk_free(chunk)

def _summarize_chunk_gemini(chunk):
    """Use Google Gemini to generate a short chapter title"""
    if not _gemini_client:
        raise Exception("Gemini client not available")
    
    prompt = f"""Generate a concise, engaging chapter title (maximum 6 words) for this video transcript segment. 
    Make it descriptive and interesting. Add a relevant emoji at the beginning if appropriate.
    
    Rules:
    - Maximum 6 words
    - Be specific and descriptive
    - Use action words when possible
    - Add emoji if it enhances understanding
    - Make it sound like a YouTube chapter
    
    Transcript: {chunk[:500]}
    
    Chapter title:"""
    
    try:
        response = _gemini_client.generate_content(prompt)
        title = response.text.strip()
        
        # Clean up the response
        title = title.replace('"', '').replace("'", "").strip()
        
        # Remove any extra text after the title
        if '\n' in title:
            title = title.split('\n')[0]
        
        # Ensure it's not too long
        if len(title) > 50:
            title = title[:47] + "..."
            
        return title
        
    except Exception as e:
        raise Exception(f"Gemini generation failed: {e}")

def _summarize_chunk_free(chunk):
    """Generate chapter title using free NLP methods (no API required)"""
    if not chunk or len(chunk.strip()) < 10:
        return "📝 Short Segment"
    
    # Clean and analyze the text
    clean_text = re.sub(r'[^\w\s]', ' ', chunk.lower())
    words = clean_text.split()
    
    # Remove stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
        'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 
        'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'just', 'now', 'then',
        'here', 'there', 'when', 'where', 'why', 'how', 'what', 'who', 'which'
    }
    
    # Get meaningful words
    meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count word frequency
    word_freq = {}
    for word in meaningful_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top keywords
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Content type detection with better patterns
    text_lower = chunk.lower()
    
    # Introduction patterns
    intro_patterns = ['welcome', 'hello', 'introduction', 'start', 'begin', 'today we', 'let me introduce']
    if any(pattern in text_lower for pattern in intro_patterns):
        return "🎬 Introduction & Welcome"
    
    # Conclusion patterns
    conclusion_patterns = ['conclusion', 'summary', 'wrap up', 'in summary', 'to conclude', 'finally', 'thank you', 'that concludes']
    if any(pattern in text_lower for pattern in conclusion_patterns):
        return "🎯 Conclusion & Summary"
    
    # Tutorial/Learning patterns
    tutorial_patterns = ['learn', 'tutorial', 'how to', 'let me show', 'demonstrate', 'explain', 'teach']
    if any(pattern in text_lower for pattern in tutorial_patterns):
        topic = top_words[0][0].title() if top_words else "Concepts"
        return f"📚 Learning {topic}"
    
    # Problem/Challenge patterns
    problem_patterns = ['problem', 'issue', 'challenge', 'difficult', 'error', 'trouble', 'fix', 'solve']
    if any(pattern in text_lower for pattern in problem_patterns):
        return "⚠️ Challenges & Solutions"
    
    # Excitement/Highlight patterns
    excitement_patterns = ['amazing', 'incredible', 'fantastic', 'awesome', 'brilliant', 'outstanding', 'wow', 'great']
    if any(pattern in text_lower for pattern in excitement_patterns):
        topic = top_words[0][0].title() if top_words else "Highlights"
        return f"🔥 {topic} Spotlight"
    
    # Example/Demo patterns
    example_patterns = ['example', 'demo', 'demonstration', 'for instance', 'let me show', 'practical']
    if any(pattern in text_lower for pattern in example_patterns):
        return "💡 Practical Examples"
    
    # Q&A patterns
    qa_patterns = ['question', 'answer', 'ask', 'discuss', 'what about', 'how about']
    if any(pattern in text_lower for pattern in qa_patterns):
        return "❓ Q&A Discussion"
    
    # Technical/Analysis patterns
    analysis_patterns = ['analyze', 'analysis', 'review', 'compare', 'evaluation', 'study', 'research']
    if any(pattern in text_lower for pattern in analysis_patterns):
        topic = top_words[0][0].title() if top_words else "Content"
        return f"📊 {topic} Analysis"
    
    # Future/Next steps patterns
    future_patterns = ['future', 'next', 'upcoming', 'plan', 'going forward', 'what\'s next']
    if any(pattern in text_lower for pattern in future_patterns):
        return "🚀 Future Directions"
    
    # Use top keywords if available
    if top_words:
        if len(top_words) >= 2:
            return f"📖 {top_words[0][0].title()} & {top_words[1][0].title()}"
        else:
            return f"📖 Focus on {top_words[0][0].title()}"
    
    # Sentiment-based fallback
    try:
        blob = TextBlob(chunk)
        sentiment = blob.sentiment.polarity
        
        if sentiment > 0.3:
            return "😊 Positive Insights"
        elif sentiment < -0.3:
            return "🤔 Critical Discussion"
        else:
            return "📝 Key Points"
    except:
        return "📝 Discussion Segment"

def get_summarization_status():
    """Return current summarization method status"""
    global _gemini_available, _quota_exceeded
    
    if _gemini_available and not _quota_exceeded and _gemini_client:
        return "premium", "🤖 AI-Powered Titles (Gemini)"
    else:
        return "free", "📝 Smart Keyword Titles"

def test_summarization():
    """Test function to verify methods work"""
    test_chunks = [
        "Welcome to this amazing tutorial where we'll explore artificial intelligence and machine learning.",
        "Now let's dive into a practical example of how neural networks actually work in real applications.",
        "In conclusion, we've covered the fundamentals and I hope this tutorial was helpful. Thank you for watching!",
        "This is an incredible breakthrough in technology that will change everything we know about computing."
    ]
    
    print("Testing summarization methods...")
    method_type, method_desc = get_summarization_status()
    print(f"Using: {method_desc} ({method_type} mode)")
    
    for i, chunk in enumerate(test_chunks, 1):
        title = summarize_chunk(chunk)
        print(f"Test {i}: {title}")
        print(f"Input: {chunk[:50]}...")
        print()

if __name__ == "__main__":
    test_summarization()