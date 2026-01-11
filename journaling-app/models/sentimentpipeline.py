import streamlit as st
from transformers import pipeline, DistilBertTokenizer
from typing import Dict, List, Tuple
import random

# Define theme categories
THEME_CATEGORIES = [
    "work stress", "relationships", "family", "health", 
    "creativity", "personal growth", "anxiety", "gratitude",
    "accomplishments", "challenges", "hobbies", "social life"
]

@st.cache_resource
def load_sentiment_analyzer():
    """Load sentiment analysis model"""
    try:
        return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    except Exception as e:
        st.error(f"Error loading sentiment model: {e}")
        return None

@st.cache_resource
def load_tokenizer():
    """Load DistilBERT tokenizer for advanced text analysis"""
    try:
        return DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    except Exception as e:
        st.error(f"Error loading tokenizer: {e}")
        return None

@st.cache_resource
def load_zero_shot_classifier():
    """Load zero-shot classification for theme detection"""
    try:
        return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except Exception as e:
        st.error(f"Error loading classifier: {e}")
        return None

class AIAnalyzer:
    """Main class for AI-powered text analysis"""
    
    def __init__(self):
        self.sentiment_analyzer = load_sentiment_analyzer()
        self.tokenizer = load_tokenizer()
        self.theme_classifier = load_zero_shot_classifier()
    
    def analyze_entry(self, content: str) -> Dict:
        """Analyze a journal entry for sentiment, themes, and metrics"""
        analysis = {
            'sentiment': None,
            'themes': [],
            'word_count': len(content.split()),
            'token_count': 0,
            'unique_words': 0
        }
        
        # Token count using DistilBERT tokenizer
        if self.tokenizer:
            try:
                tokens = self.tokenizer.encode(content, add_special_tokens=False)
                analysis['token_count'] = len(tokens)
                
                # Count unique words
                words = content.lower().split()
                analysis['unique_words'] = len(set(words))
            except Exception as e:
                st.warning(f"Tokenization error: {e}")
        
        # Sentiment analysis
        if self.sentiment_analyzer:
            try:
                sentiment = self.sentiment_analyzer(content[:512])[0]
                analysis['sentiment'] = {
                    'label': sentiment['label'],
                    'score': sentiment['score']
                }
            except Exception as e:
                st.warning(f"Sentiment analysis error: {e}")
        
        # Theme classification
        if self.theme_classifier and len(content) > 20:
            try:
                result = self.theme_classifier(content[:512], THEME_CATEGORIES, multi_label=True)
                # Get themes with score > 0.3
                themes = [(label, score) for label, score in zip(result['labels'], result['scores']) if score > 0.3]
                analysis['themes'] = themes[:3]  # Top 3 themes
            except Exception as e:
                st.warning(f"Theme classification error: {e}")
        
        return analysis
    
    def generate_contextual_prompt(self, recent_entries: List[Dict]) -> str:
        """Generate context-aware prompts based on recent entries"""
        prompts = {
            "default": [
                "What's one thing that made you smile today?",
                "Describe a moment from today that you want to remember.",
                "What challenged you today, and how did you respond?",
                "What are you grateful for right now?",
                "How are you feeling in this moment, and why?",
                "What did you learn about yourself today?",
                "What surprised you today?",
                "If today had a color, what would it be and why?"
            ],
            "stress": [
                "What helped you find calm during a stressful moment today?",
                "What's one small thing you could do to ease your stress tomorrow?",
                "How did you take care of yourself during difficult moments today?",
                "What boundary could you set to protect your peace?",
                "What would you tell a friend feeling the way you do?"
            ],
            "positive": [
                "What positive energy are you carrying forward from today?",
                "How can you create more moments like the good ones you experienced?",
                "What strength did you discover in yourself today?",
                "What's something you're proud of right now?",
                "How did you make someone else's day better?"
            ],
            "creative": [
                "What ideas have been flowing through your mind lately?",
                "What inspires you right now?",
                "How could you nurture your creative side more?",
                "What would you create if you had unlimited time and resources?",
                "What creative project is calling to you?"
            ],
            "reflective": [
                "What pattern have you noticed in your life lately?",
                "What's one thing you'd like to change?",
                "What are you becoming?",
                "What wisdom would your future self share with you?",
                "What does success look like for you right now?"
            ]
        }
        
        if not recent_entries:
            return random.choice(prompts["default"])
        
        # Analyze sentiment of recent entries
        recent_text = " ".join([entry.get('content', '')[:200] for entry in recent_entries[-3:]])
        
        if self.sentiment_analyzer and recent_text:
            try:
                sentiment = self.sentiment_analyzer(recent_text[:512])[0]
                if sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.6:
                    return random.choice(prompts["stress"])
                elif sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.7:
                    return random.choice(prompts["positive"])
            except:
                pass
        
        # Check for creative keywords
        if any(word in recent_text.lower() for word in ['idea', 'create', 'imagine', 'design', 'art']):
            return random.choice(prompts["creative"])
        
        # Check for reflective keywords
        if any(word in recent_text.lower() for word in ['wonder', 'think', 'feel', 'realize', 'understand']):
            return random.choice(prompts["reflective"])
        
        return random.choice(prompts["default"])
    
    def get_token_count(self, text: str) -> int:
        """Get real-time token count for text"""
        if self.tokenizer and text:
            try:
                tokens = self.tokenizer.encode(text, add_special_tokens=False)
                return len(tokens)
            except:
                return 0
        return 0