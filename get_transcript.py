import time
import random
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
import requests

# Check if yt-dlp is available
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("yt-dlp not available, using youtube-transcript-api only")

def get_transcript(video_id, max_retries=3):
    """
    Get transcript with multiple fallback methods and rate limiting protection
    """
    print(f"Attempting to get transcript for video: {video_id}")
    
    # Method 1: Try youtube-transcript-api with retries and delays
    for attempt in range(max_retries):
        try:
            print(f"Method 1 - Attempt {attempt + 1}: youtube-transcript-api")
            
            # Add random delay to avoid rate limiting
            if attempt > 0:
                delay = random.uniform(2, 5) * attempt
                print(f"Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)
            
            # Try the simple approach first
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['en', 'en-US', 'en-GB']
            )
            
            text = " ".join([item['text'] for item in transcript_list])
            print(f"✅ Success with youtube-transcript-api! Got {len(text)} characters")
            return text, transcript_list
            
        except Exception as e:
            print(f"❌ youtube-transcript-api attempt {attempt + 1} failed: {str(e)[:100]}...")
            if "429" in str(e) or "Too Many Requests" in str(e):
                print("Rate limited - waiting longer...")
                time.sleep(random.uniform(10, 20))
            continue
    
    # Method 2: Try yt-dlp for subtitle extraction
    if YT_DLP_AVAILABLE:
        try:
            print("Method 2: Trying yt-dlp...")
            return get_transcript_with_ytdlp(video_id)
        except Exception as e:
            print(f"❌ yt-dlp failed: {str(e)[:100]}...")
    
    # Method 3: Try alternative YouTube transcript approach
    try:
        print("Method 3: Trying alternative transcript API...")
        return get_transcript_alternative(video_id)
    except Exception as e:
        print(f"❌ Alternative method failed: {str(e)[:100]}...")
    
    # If all methods fail
    print("❌ All transcript methods failed")
    return "", []

def get_transcript_with_ytdlp(video_id):
    """Use yt-dlp to extract subtitles"""
    if not YT_DLP_AVAILABLE:
        raise Exception("yt-dlp not available")
    
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en', 'en-US'],
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'format': 'best[height<=480]',
    }
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            # Try automatic subtitles first
            if 'automatic_captions' in info and info['automatic_captions']:
                for lang in ['en', 'en-US', 'en-GB']:
                    if lang in info['automatic_captions']:
                        for format_info in info['automatic_captions'][lang]:
                            if format_info['ext'] in ['json3', 'srv1', 'srv2', 'srv3']:
                                try:
                                    response = requests.get(format_info['url'], timeout=10)
                                    if response.status_code == 200:
                                        subtitle_text = parse_json_captions(response.text)
                                        if subtitle_text:
                                            print(f"✅ Got JSON auto captions via yt-dlp ({lang})")
                                            return subtitle_text, create_transcript_data(subtitle_text)
                                except:
                                    continue
                            
                            elif format_info['ext'] == 'vtt':
                                try:
                                    response = requests.get(format_info['url'], timeout=10)
                                    if response.status_code == 200:
                                        subtitle_text = parse_vtt_captions(response.text)
                                        if subtitle_text:
                                            print(f"✅ Got VTT auto captions via yt-dlp ({lang})")
                                            return subtitle_text, create_transcript_data(subtitle_text)
                                except:
                                    continue
        
        except Exception as e:
            raise Exception(f"yt-dlp extraction failed: {e}")
    
    raise Exception("No subtitles found via yt-dlp")

def parse_json_captions(json_content):
    """Parse JSON format captions from YouTube"""
    try:
        data = json.loads(json_content)
        if 'events' in data:
            text_parts = []
            for event in data['events']:
                if 'segs' in event:
                    for seg in event['segs']:
                        if 'utf8' in seg:
                            text_parts.append(seg['utf8'])
            return ' '.join(text_parts)
    except:
        pass
    return ""

def parse_vtt_captions(vtt_content):
    """Parse VTT format captions and clean up the text"""
    # Skip if this looks like M3U playlist data
    if vtt_content.startswith('#EXTM3U') or '#EXT-X-' in vtt_content:
        return ""
    
    lines = vtt_content.split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip VTT headers, timing lines, and empty lines
        if (not line or 
            line.startswith('WEBVTT') or 
            line.startswith('NOTE') or 
            line.startswith('#') or  # Skip M3U/playlist lines
            '-->' in line or
            line.startswith('<') or
            line.isdigit() or
            'http' in line.lower()):  # Skip URLs
            continue
        
        # Skip timing patterns
        if re.match(r'^\d{2}:\d{2}:\d{2}', line):
            continue
            
        # Clean up HTML tags and common artifacts
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'\[.*?\]', '', line)
        line = re.sub(r'\(.*?\)', '', line)
        line = re.sub(r'&\w+;', ' ', line)  # Remove HTML entities
        
        # Only keep lines with actual words (not just punctuation/numbers)
        if line and len(line) > 3 and any(c.isalpha() for c in line):
            text_lines.append(line)
    
    result = ' '.join(text_lines)
    # Final cleanup
    result = ' '.join(result.split())  # Normalize whitespace
    return result

def create_transcript_data(text):
    """Create fake transcript data with timestamps for compatibility"""
    words = text.split()
    transcript_data = []
    
    for i, word in enumerate(words):
        transcript_data.append({
            'text': word,
            'start': i * 0.6,  # 0.6 seconds per word
            'duration': 0.6
        })
    
    return transcript_data

def get_transcript_alternative(video_id):
    """Alternative method using different transcript approach"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try different language combinations
        language_priorities = [
            ['en'],
            ['en-US'], 
            ['en-GB'],
            ['ar'],  # Arabic as fallback
            None     # Any available language
        ]
        
        for languages in language_priorities:
            try:
                if languages:
                    transcript = transcript_list.find_transcript(languages).fetch()
                else:
                    # Get any available transcript
                    available = list(transcript_list)
                    if available:
                        transcript = available[0].fetch()
                    else:
                        continue
                
                text = " ".join([item['text'] for item in transcript])
                if text.strip():
                    lang_str = languages[0] if languages else "auto-detected"
                    print(f"✅ Got transcript via alternative method ({lang_str})")
                    return text, transcript
                    
            except Exception as e:
                continue
        
    except Exception as e:
        raise Exception(f"Alternative transcript method failed: {e}")
    
    raise Exception("No transcript found via alternative method")

def get_demo_transcript(video_id):
    """
    Demo transcript for testing when YouTube API fails
    """
    demo_text = """
    Welcome everyone to this comprehensive tutorial on artificial intelligence and machine learning. 
    Today we're going to dive deep into how neural networks work and why they're revolutionizing every industry. 
    This is incredibly exciting because we're witnessing a transformation that will change everything we know about technology.
    
    First, let's understand what makes artificial intelligence so powerful. The key is in the way these systems can learn patterns from data.
    It's absolutely mind-blowing how a computer can recognize images, understand speech, and even generate creative content.
    
    Now, here's where things get really interesting. Machine learning algorithms can actually improve themselves over time.
    This means they become smarter and more accurate with every piece of data they process. Isn't that amazing?
    
    Let me show you a practical example of how this works in real-world applications.
    This demonstration will help you understand the core concepts we've been discussing throughout this tutorial.
    
    The applications are endless - from healthcare to transportation, from finance to entertainment.
    We're seeing breakthrough innovations that seemed impossible just a few years ago becoming reality today.
    
    Now let's address some common questions that people have about artificial intelligence and machine learning.
    These are important challenges that the field is actively working to solve with innovative approaches.
    
    But wait, there's more! The future holds even more surprising developments in store for us.
    Imagine AI systems that can understand human emotions, create art, and solve complex global challenges.
    
    This is truly a remarkable time to be alive and witness these technological marvels unfold before our eyes.
    The potential is limitless, and the excitement in the research community is absolutely contagious.
    
    Thank you for joining me on this journey through the world of artificial intelligence and machine learning.
    I hope this tutorial has given you valuable insights into this fascinating and rapidly evolving field.
    """
    
    # Create fake transcript data with timestamps
    words = demo_text.split()
    transcript_data = []
    
    for i, word in enumerate(words):
        transcript_data.append({
            'text': word,
            'start': i * 0.5,  # 0.5 seconds per word
            'duration': 0.5
        })
    
    return demo_text.strip(), transcript_data

def test_transcript_methods():
    """Test with known working videos"""
    test_videos = [
        "dQw4w9WgXcQ",  # Rick Roll - usually has captions
        "9bZkp7q19f0",  # PSY - Gangnam Style
        "kJQP7kiw5Fk"   # Despacito
    ]
    
    print("Testing transcript methods...")
    for video_id in test_videos:
        print(f"\n--- Testing {video_id} ---")
        text, transcript = get_transcript(video_id)
        if text:
            print(f"✅ Success! Got {len(text)} characters")
            print(f"Preview: {text[:100]}...")
            break
        else:
            print("❌ Failed")
    
if __name__ == "__main__":
    test_transcript_methods()