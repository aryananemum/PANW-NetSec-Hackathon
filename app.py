import streamlit as st
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import DatabaseManager
from sentimentpipeline import AIAnalyzer
from styles import get_custom_css, create_stat_card

# Page configuration
st.set_page_config(
    page_title="AI Journaling Companion",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and AI analyzer in session state
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

if 'ai_analyzer' not in st.session_state:
    st.session_state.ai_analyzer = AIAnalyzer()

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Main page content
st.markdown('<div class="main-header"><h1>AI Journaling Companion</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your private space for reflection and growth</div>', unsafe_allow_html=True)

# Welcome section with feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card animate-fade-in">
        <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
        <h3>Smart Prompts</h3>
        <p style="color: #64748b;">Get AI-generated prompts based on your writing patterns and emotional state.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card animate-fade-in" style="animation-delay: 0.1s;">
        <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
        <h3>Deep Insights</h3>
        <p style="color: #64748b;">Discover patterns in your thoughts and emotions with sentiment analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card animate-fade-in" style="animation-delay: 0.2s;">
        <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
        <h3>Private & Secure</h3>
        <p style="color: #64748b;">All your data stays on your device. Complete privacy guaranteed.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Quick stats with styled cards
stats = st.session_state.db.get_statistics()

st.markdown("<h2 style='text-align: center; color: #1e3a8a; margin-bottom: 2rem;'>Your Journey at a Glance</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_stat_card("Total Entries", stats['total_entries'], "", "#667eea"), unsafe_allow_html=True)

with col2:
    st.markdown(create_stat_card("Words Written", f"{stats['total_words']:,}", "", "#f59e0b"), unsafe_allow_html=True)

with col3:
    streak_icon = "🔥" if stats['current_streak'] > 0 else "💤"
    st.markdown(create_stat_card("Current Streak", f"{stats['current_streak']} days {streak_icon}", "", "#ef4444"), unsafe_allow_html=True)

with col4:
    if stats['avg_sentiment'] is not None:
        sentiment_rate = "Happy" if stats['avg_sentiment'] > 0 else "Sad"
        sentiment_text = "Positive" if stats['avg_sentiment'] > 0 else "Negative"
        st.markdown(create_stat_card("Avg Sentiment", sentiment_rate, "", "#10b981"), unsafe_allow_html=True)
    else:
        st.markdown(create_stat_card("Avg Sentiment", "N/A", "", "#94a3b8"), unsafe_allow_html=True)

st.divider()

# Getting started guide
if stats['total_entries'] == 0:
    st.markdown("""
    <div class="glass-card animate-fade-in" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;"></div>
        <h2 style="color: #1e3a8a; margin-bottom: 1rem;">Welcome to Your Journaling Journey!</h2>
        <p style="font-size: 1.1rem; color: #64748b; margin-bottom: 2rem;">
            Get started by creating your first journal entry and unlock the power of AI-driven self-reflection.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #1e3a8a; margin-bottom: 1.5rem;">🚀 How to Use This App</h3>
            
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: #667eea;"> New Entry</h4>
                <p style="color: #64748b;">Start writing! Get AI-powered prompts to inspire your reflection and track your emotions.</p>
            </div>
            
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: #667eea;">Insights</h4>
                <p style="color: #64748b;">View emotional patterns and discover themes in your writing through beautiful visualizations.</p>
            </div>
            
            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: #667eea;">Past Entries</h4>
                <p style="color: #64748b;">Browse and reflect on your journal history with powerful search and filtering.</p>
            </div>
            
            <div>
                <h4 style="color: #667eea;">Weekly Summary</h4>
                <p style="color: #64748b;">Get AI-generated insights about your week and track your personal growth.</p>
            </div>
            
            <div style="text-align: center; margin-top: 2rem;">
                <p style="color: #667eea; font-weight: 600;">
                     Use the sidebar on the left to navigate between pages!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Recent activity
    st.markdown("<h2 style='color: #1e3a8a; margin-bottom: 1.5rem;'>📖 Recent Activity</h2>", unsafe_allow_html=True)
    
    recent_entries = st.session_state.db.get_all_entries(limit=3)
    
    if recent_entries:
        for entry in recent_entries:
            from utils.styles import get_sentiment_badge, get_theme_badges
            
            sentiment_badge = get_sentiment_badge(entry.get('sentiment_label'), entry.get('sentiment_score')) if entry.get('sentiment_label') else ""
            theme_badges = get_theme_badges(entry.get('themes', []))
            
            with st.expander(f"{entry['timestamp'][:10]} - {entry['content'][:60]}...", expanded=False):
                st.markdown(f"""
                <div class="entry-card">
                    <div style="margin-bottom: 1rem;">
                        {sentiment_badge}
                        {theme_badges}
                    </div>
                    <p style="color: #334155; line-height: 1.6;">{entry['content']}</p>
                    <div style="margin-top: 1rem; color: #94a3b8; font-size: 0.875rem;">
                        {entry.get('word_count', 0)} words
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: #f8fafc; border-radius: 12px;">
        <p style="color: #667eea; font-weight: 500;">
            Navigate using the sidebar to see all features →
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("###  Navigation")
    st.markdown("Use the pages above to:")
    st.markdown("- Write new entries")
    st.markdown("- View insights")
    st.markdown("- Read past entries")
    st.markdown("- Get weekly summaries")
    
    st.divider()
    
    st.markdown("### Settings")
    
    # Theme preference
    theme = st.selectbox(
        "Journal Theme",
        ["Light", "Dark", "Auto"],
        index=0
    )
    
    # Export option
    st.markdown("### Export Data")
    if st.button("Export All Entries"):
        from utils.helpers import export_to_markdown
        entries = st.session_state.db.get_all_entries()
        
        if entries:
            md_content = export_to_markdown(entries)
            st.download_button(
                label="Download Markdown",
                data=md_content,
                file_name=f"journal_export_{st.session_state.db.get_statistics()['total_entries']}_entries.md",
                mime="text/markdown"
            )
        else:
            st.warning("No entries to export")
    
    # Danger zone
    with st.expander("Danger Zone"):
        st.warning("This will delete ALL your journal entries permanently!")
        confirm = st.text_input("Type 'DELETE' to confirm:")
        if st.button("Delete All Data"):
            if confirm == "DELETE":
                st.session_state.db.clear_all_entries()
                st.success("All data deleted!")
                st.rerun()
            else:
                st.error("Please type 'DELETE' to confirm")
    
    st.divider()
    
    st.markdown("### Tips")
    st.caption("- Write regularly for better insights")
    st.caption("- Be honest with yourself")
    st.caption("- Review past entries to see growth")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "</div>",
    unsafe_allow_html=True
)