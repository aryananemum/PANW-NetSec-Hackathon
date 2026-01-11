import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import DatabaseManager
from sentimentpipeline import AIAnalyzer
from styles import get_custom_css, get_sentiment_badge, get_theme_badges

st.set_page_config(page_title="New Entry", page_icon="📝", layout="wide")

# Initialize if not already done
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

if 'ai_analyzer' not in st.session_state:
    st.session_state.ai_analyzer = AIAnalyzer()

if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = None

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Header with gradient background
st.markdown("""
<div class="page-title-container animate-fade-in">
    <h1> New Journal Entry</h1>
    <p>Take a moment to reflect on your day</p>
</div>
""", unsafe_allow_html=True)

# Generate contextual prompt
if st.session_state.current_prompt is None:
    recent_entries = st.session_state.db.get_all_entries(limit=5)
    st.session_state.current_prompt = st.session_state.ai_analyzer.generate_contextual_prompt(recent_entries)

# Display prompt in a beautiful card
st.markdown(f"""
<div class="prompt-card animate-fade-in">
    <h4> Today's Reflection Prompt</h4>
    <p>{st.session_state.current_prompt}</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Get New Prompt", use_container_width=True):
        recent_entries = st.session_state.db.get_all_entries(limit=5)
        st.session_state.current_prompt = st.session_state.ai_analyzer.generate_contextual_prompt(recent_entries)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Journal entry input with styling
st.markdown("""
<div class="custom-card">
    <h3 style="color: #1e3a8a; margin-bottom: 1rem;">Your Thoughts</h3>
</div>
""", unsafe_allow_html=True)
entry_content = st.text_area(
    "Write your thoughts...",
    height=350,
    placeholder="What's on your mind today? There's no right or wrong way to journal. Just let your thoughts flow...",
    help="Be honest and open. This is your private space."
)

# Real-time metrics
col1, col2, col3 = st.columns(3)

with col1:
    word_count = len(entry_content.split()) if entry_content else 0
    st.metric("Word Count", word_count)

with col2:
    token_count = st.session_state.ai_analyzer.get_token_count(entry_content) if entry_content else 0
    st.metric("Token Count", token_count)

with col3:
    char_count = len(entry_content) if entry_content else 0
    st.metric("Characters", char_count)

st.divider()

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("Save Entry", type="primary", use_container_width=True):
        if entry_content.strip():
            with st.spinner("✨ Analyzing your entry with AI..."):
                # Analyze the entry
                analysis = st.session_state.ai_analyzer.analyze_entry(entry_content)
                
                # Save to database
                entry_id = st.session_state.db.add_entry(
                    content=entry_content,
                    prompt=st.session_state.current_prompt,
                    analysis=analysis
                )
                
                st.success("Entry saved successfully!")
                
                # Show analysis results in styled cards
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #1e3a8a;'>🔍 Quick Analysis</h3>", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if analysis['sentiment']:
                        sentiment_badge = get_sentiment_badge(
                            analysis['sentiment']['label'],
                            analysis['sentiment']['score']
                        )
                        
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style='color: #667eea; margin-bottom: 0.5rem;'>Emotional Tone</h4>
                            {sentiment_badge}
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_b:
                    if analysis['themes']:
                        theme_badges = get_theme_badges(analysis['themes'])
                        st.markdown(f"""
                        <div class="custom-card">
                            <h4 style='color: #667eea; margin-bottom: 0.5rem;'>Main Themes</h4>
                            {theme_badges}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.balloons()
                
                # Reset for next entry
                st.session_state.current_prompt = None
                
                # Offer to write another
                if st.button("Write Another Entry"):
                    st.rerun()
        else:
            st.warning("Please write something before saving.")

with col2:
    if st.button("💡 Tips", use_container_width=True):
        st.info("""
        **Journaling Tips:**
        - Write freely without judging yourself
        - Focus on how you feel, not just what happened
        - Be specific and detailed
        - It's okay to write messy thoughts
        - Reflect on what you learned
        """)

with col3:
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()

# Sidebar with stats
with st.sidebar:
    st.markdown("### 📊 Your Writing Stats")
    
    stats = st.session_state.db.get_statistics()
    
    st.metric("Total Entries", stats['total_entries'])
    st.metric("Total Words", f"{stats['total_words']:,}")
    st.metric("Current Streak", f"{stats['current_streak']} days 🔥")
    
    st.divider()
    
    st.markdown("### Writing Inspiration")
    st.info("""
    "Writing is the painting of the voice."
    — Voltaire
    """)
    
    st.markdown("""
    Remember: Your journal is a judgment-free zone. 
    Write what you feel, not what you think you should feel.
    """)