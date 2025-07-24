import re
from textblob import TextBlob
import numpy as np
from transformers import pipeline

class EmotionDetector:
    def __init__(self):
        # Load emotion detection model (lightweight)
        try:
            self.emotion_classifier = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base",
                device=-1  # Use CPU
            )
            self.use_transformer = True
        except:
            print("Transformer model failed to load, using TextBlob fallback")
            self.use_transformer = False
    
    def detect_emotions_in_chunks(self, chunks, transcript_data):
        """Detect emotions for each chunk and find emotional peaks"""
        chunk_emotions = []
        
        for i, chunk in enumerate(chunks):
            if self.use_transformer:
                # Use transformer model for better emotion detection
                emotions = self.emotion_classifier(chunk[:512])  # Limit text length
                emotion_scores = {
                    'joy': 0, 'excitement': 0, 'surprise': 0, 
                    'anger': 0, 'sadness': 0, 'fear': 0, 'neutral': 0
                }
                
                for emotion in emotions:
                    label = emotion['label'].lower()
                    score = emotion['score']
                    
                    # Map transformer labels to our categories
                    if label in ['joy', 'happiness']:
                        emotion_scores['joy'] = score
                    elif label in ['surprise']:
                        emotion_scores['surprise'] = score
                    elif label in ['anger']:
                        emotion_scores['anger'] = score
                    elif label in ['sadness']:
                        emotion_scores['sadness'] = score
                    elif label in ['fear']:
                        emotion_scores['fear'] = score
                    else:
                        emotion_scores['neutral'] = score
                
            else:
                # Fallback: Use TextBlob + keyword matching
                emotion_scores = self._analyze_with_textblob(chunk)
            
            # Calculate excitement score (combination of positive emotions)
            excitement_score = (
                emotion_scores.get('joy', 0) * 0.4 +
                emotion_scores.get('surprise', 0) * 0.3 +
                emotion_scores.get('excitement', 0) * 0.3
            )
            
            # Get timestamp for this chunk
            timestamp = transcript_data[i * 100]['start'] if i * 100 < len(transcript_data) else 0
            
            chunk_emotions.append({
                'chunk_index': i,
                'timestamp': timestamp,
                'emotions': emotion_scores,
                'excitement_score': excitement_score,
                'text_preview': chunk[:100] + "..." if len(chunk) > 100 else chunk
            })
        
        return chunk_emotions
    
    def _analyze_with_textblob(self, text):
        """Fallback emotion analysis using TextBlob and keywords"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Keyword-based emotion detection
        excitement_words = ['amazing', 'incredible', 'wow', 'awesome', 'fantastic', 
                          'brilliant', 'outstanding', 'remarkable', 'extraordinary']
        surprise_words = ['surprising', 'unexpected', 'shocking', 'unbelievable', 
                         'astonishing', 'sudden', 'sudden']
        joy_words = ['happy', 'joy', 'excited', 'thrilled', 'delighted', 'pleased']
        
        text_lower = text.lower()
        
        excitement_count = sum(1 for word in excitement_words if word in text_lower)
        surprise_count = sum(1 for word in surprise_words if word in text_lower)
        joy_count = sum(1 for word in joy_words if word in text_lower)
        
        return {
            'joy': min(1.0, (polarity + 1) / 2 + joy_count * 0.1),
            'excitement': min(1.0, excitement_count * 0.2 + max(0, polarity) * 0.5),
            'surprise': min(1.0, surprise_count * 0.3 + subjectivity * 0.2),
            'neutral': max(0, 1 - abs(polarity))
        }
    
    def find_highlights(self, chunk_emotions, top_n=5):
        """Find the most exciting/emotional moments"""
        # Sort by excitement score
        sorted_chunks = sorted(chunk_emotions, key=lambda x: x['excitement_score'], reverse=True)
        
        highlights = []
        for chunk in sorted_chunks[:top_n]:
            # Get dominant emotion
            emotions = chunk['emotions']
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            
            highlights.append({
                'timestamp': chunk['timestamp'],
                'excitement_score': chunk['excitement_score'],
                'dominant_emotion': dominant_emotion[0],
                'emotion_strength': dominant_emotion[1],
                'preview': chunk['text_preview'],
                'chunk_index': chunk['chunk_index']
            })
        
        return highlights
    
    def get_emotion_timeline(self, chunk_emotions):
        """Create data for emotion timeline visualization"""
        timeline_data = []
        for chunk in chunk_emotions:
            timeline_data.append({
                'timestamp': chunk['timestamp'],
                'joy': chunk['emotions'].get('joy', 0),
                'excitement': chunk['emotions'].get('excitement', 0),
                'surprise': chunk['emotions'].get('surprise', 0),
                'overall_excitement': chunk['excitement_score']
            })
        
        return timeline_data