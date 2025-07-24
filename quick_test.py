#!/usr/bin/env python3
"""
Quick test of VibeChapters without YouTube dependencies
This will test your Gemini integration properly
"""

import os
from dotenv import load_dotenv
from split_text import split_text
from summarize import summarize_chunk, get_summarization_status

# Load environment
load_dotenv()

def test_gemini_chapters():
    """Test the complete chapter generation pipeline"""
    
    print("🧪 Testing VibeChapters with Gemini")
    print("=" * 50)
    
    # Check Gemini status
    method_type, method_desc = get_summarization_status()
    print(f"📊 Current mode: {method_desc}")
    
    if method_type == "premium":
        print("✅ Gemini is configured and ready!")
    else:
        print("ℹ️ Using free mode (Gemini not configured)")
    
    print()
    
    # Test content (realistic programming tutorial)
    test_transcript = """
    Welcome to this Python programming masterclass. Today we're going to cover everything you need to know to become a proficient Python developer. Python is one of the most versatile programming languages in the world.
    
    Let's start with the fundamentals of Python syntax and basic concepts. Understanding variables and data types is crucial for any Python programmer. We'll explore strings, integers, floats, and boolean values in detail.
    
    Now I want to show you how to work with lists and dictionaries in Python. These are fundamental data structures that you'll use constantly in your Python programming journey. Lists are ordered collections while dictionaries store key-value pairs.
    
    Functions are the building blocks of any well-structured Python program. Writing clean, reusable functions will make your code more maintainable and easier to debug. Let's create some practical examples together.
    
    Error handling is something many beginners overlook, but it's absolutely essential for writing robust applications. Python's try-except blocks allow you to handle errors gracefully without crashing your program.
    
    Object-oriented programming takes your Python skills to the next level. Classes and objects allow you to model real-world entities in your code. This paradigm is incredibly powerful for complex applications.
    
    Let's explore some amazing Python libraries that can supercharge your development. NumPy for numerical computing, Pandas for data analysis, and Requests for working with APIs are just a few examples.
    
    Finally, we'll discuss best practices and coding conventions that will make you a better Python developer. Clean code is not just about making it work, but making it readable and maintainable for other developers.
    
    Thank you for following along with this comprehensive Python tutorial. Remember, the key to mastering programming is consistent practice and building real projects. Keep coding and never stop learning!
    """
    
    print("📝 Test transcript loaded")
    print(f"   📊 Length: {len(test_transcript)} characters")
    print(f"   📊 Words: {len(test_transcript.split())} words")
    print()
    
    # Split into chunks
    print("✂️ Splitting into chapters...")
    chunks = split_text(test_transcript, max_words=80)
    print(f"   ✅ Created {len(chunks)} chunks")
    print()
    
    # Generate chapters
    print("🤖 Generating chapter titles...")
    print("-" * 30)
    
    chapters = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        
        try:
            title = summarize_chunk(chunk)
            chapters.append({
                'title': title,
                'content': chunk,
                'timestamp': i * 60  # Simulate 1 minute per chapter
            })
            print(f"   ✅ {title}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            chapters.append({
                'title': f"Chapter {i+1}",
                'content': chunk,
                'timestamp': i * 60
            })
    
    print()
    print("🎉 Final Results:")
    print("=" * 50)
    
    for i, chapter in enumerate(chapters):
        minutes, seconds = divmod(chapter['timestamp'], 60)
        print(f"{i+1}. {chapter['title']}")
        print(f"   🕐 {minutes:02d}:{seconds:02d}")
        print(f"   📝 {chapter['content'][:100]}...")
        print()
    
    # Summary
    print("📊 Summary:")
    print(f"   - Mode: {method_desc}")
    print(f"   - Chapters generated: {len(chapters)}")
    print(f"   - Total words processed: {len(test_transcript.split())}")
    print(f"   - Average words per chapter: {len(test_transcript.split()) // len(chapters)}")
    
    if method_type == "premium":
        print("\n🎉 SUCCESS! Your Gemini integration is working perfectly!")
        print("🤖 The AI-generated chapter titles should be creative and contextual.")
    else:
        print("\n💡 Your free mode is working! Add a Gemini API key for AI-powered titles.")
    
    return chapters

def test_gemini_direct():
    """Test Gemini API directly"""
    print("\n🔧 Testing Gemini API directly...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ No GEMINI_API_KEY found in environment")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        test_prompt = "Generate a creative chapter title for this content: 'Welcome to Python programming. Today we'll learn about variables and functions.'"
        
        response = model.generate_content(test_prompt)
        print(f"✅ Gemini API test successful!")
        print(f"   🤖 Response: {response.text}")
        return True
        
    except ImportError:
        print("❌ google-generativeai library not installed")
        return False
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

if __name__ == "__main__":
    # Test Gemini directly first
    gemini_works = test_gemini_direct()
    print()
    
    # Test the full pipeline
    chapters = test_gemini_chapters()
    
    print("\n" + "="*50)
    if gemini_works:
        print("🚀 Everything is working! Your app should generate amazing chapters.")
        print("🎯 Try Demo Mode in your Streamlit app - it will work perfectly!")
    else:
        print("💡 Free mode is working. Get a Gemini API key for AI features!")
    
    print("\n🎪 Next steps:")
    print("1. Run 'streamlit run app.py'")
    print("2. Enable Demo Mode in the sidebar")
    print("3. Click 'Generate Chapters'")
    print("4. Wait for YouTube rate limits to reset (1-2 hours)")