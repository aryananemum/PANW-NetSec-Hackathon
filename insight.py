import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import DatabaseManager
from helper import (
    create_sentiment_timeline, 
    create_theme_distribution,
    create_writing_volume_chart,
    get_streak_info
)
from styles import get_custom_css, create_stat_card

st.set_page_config(page_title="Insights", page_icon="📊", layout="wide")

# Initialize
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-title-container animate-fade-in">
    <h1>Your Emotional Patterns & Insights</h1>
    <p>Discover patterns in your thoughts and emotions</p>
</div>
""", unsafe_allow_html=True)

# Get all entries
entries = st.session_state.db.get_all_entries()

if not entries:
    st.info(" Start journaling to see your insights! Write your first entry to begin tracking your emotional journey.")
    
    st.markdown("""
    ### What You'll See Here:
    - **Sentiment Timeline**: Track your emotional ups and downs over time
    - **Theme Analysis**: See what topics you write about most
    - **Writing Patterns**: Understand your journaling habits
    - **Streak Tracking**: Monitor your consistency
    """)
else:
    # Time filter
    st.sidebar.markdown("### Time Filter")
    time_range = st.sidebar.selectbox(
        "Show data from:",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
    )
    
    # Filter entries based on time range
    if time_range != "All time":
        days = int(time_range.split()[1])
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_entries = [
            e for e in entries 
            if datetime.fromisoformat(e['timestamp']) > cutoff_date
        ]
    else:
        filtered_entries = entries
    
    if not filtered_entries:
        st.warning(f"No entries found in {time_range.lower()}. Try selecting a longer time range.")
    else:
        # Key metrics
        st.subheader("Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Entries", len(filtered_entries))
        
        with col2:
            total_words = sum(e.get('word_count', 0) for e in filtered_entries)
            st.metric("Words Written", f"{total_words:,}")
        
        with col3:
            avg_words = total_words / len(filtered_entries) if filtered_entries else 0
            st.metric("Avg Words/Entry", f"{avg_words:.0f}")
        
        with col4:
            streak_info = get_streak_info(entries)
            st.metric("Current Streak", f"{streak_info['current']} days 🔥")
        
        st.divider()
        
        # Sentiment timeline
        st.subheader("Emotional Journey")
        sentiment_fig = create_sentiment_timeline(filtered_entries)
        
        if sentiment_fig:
            st.plotly_chart(sentiment_fig, use_container_width=True)
            
            # Sentiment insights
            positive_entries = sum(1 for e in filtered_entries if e.get('sentiment_label') == 'POSITIVE')
            total_sentiment_entries = sum(1 for e in filtered_entries if e.get('sentiment_label'))
            
            if total_sentiment_entries > 0:
                positive_pct = (positive_entries / total_sentiment_entries) * 100
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if positive_pct > 70:
                        st.success(f" You're having a great time! {positive_pct:.0f}% of your entries are positive.")
                    elif positive_pct > 50:
                        st.info(f" Overall positive mood. {positive_pct:.0f}% of entries are positive.")
                    elif positive_pct > 30:
                        st.warning(f"Mixed emotions. {positive_pct:.0f}% of entries are positive.")
                    else:
                        st.error(f" You might be going through a tough time. Consider reaching out to someone you trust.")
                
                with col2:
                    # Average sentiment score
                    avg_sentiment = sum(
                        e['sentiment_score'] if e['sentiment_label'] == 'POSITIVE' else -e['sentiment_score']
                        for e in filtered_entries if e.get('sentiment_score')
                    ) / total_sentiment_entries
                    
                    st.metric("Average Sentiment", f"{avg_sentiment:.2f}", 
                             delta="Positive" if avg_sentiment > 0 else "Negative")
        else:
            st.info("Not enough sentiment data to display timeline.")
        
        st.divider()
        
        # Theme analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Theme Distribution")
            theme_fig = create_theme_distribution(filtered_entries)
            
            if theme_fig:
                st.plotly_chart(theme_fig, use_container_width=True)
                
                # Theme insights
                from collections import Counter
                all_themes = []
                for entry in filtered_entries:
                    if entry.get('themes'):
                        for theme_data in entry['themes']:
                            if isinstance(theme_data, (list, tuple)) and len(theme_data) >= 1:
                                all_themes.append(theme_data[0])
                
                if all_themes:
                    top_theme = Counter(all_themes).most_common(1)[0][0]
                    st.info(f"💡 Your dominant theme is **{top_theme}**. This is what occupies your mind most.")
            else:
                st.info("Not enough theme data available.")
        
        with col2:
            st.subheader("Writing Volume")
            volume_fig = create_writing_volume_chart(filtered_entries)
            
            if volume_fig:
                st.plotly_chart(volume_fig, use_container_width=True)
                
                # Writing insights
                max_words_entry = max(filtered_entries, key=lambda x: x.get('word_count', 0))
                max_words = max_words_entry.get('word_count', 0)
                max_date = datetime.fromisoformat(max_words_entry['timestamp']).strftime('%B %d')
                
                st.info(f"Your longest entry was **{max_words} words** on {max_date}.")
            else:
                st.info("Not enough writing volume data.")
        
        st.divider()
        
        # Streak and consistency
        st.subheader("Consistency & Streaks")
        
        streak_info = get_streak_info(entries)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Streak", f"{streak_info['current']} days")
            if streak_info['current'] >= 7:
                st.success("Amazing! You've built a solid habit!")
            elif streak_info['current'] >= 3:
                st.info("Keep it up! You're building momentum!")
        
        with col2:
            st.metric("Longest Streak", f"{streak_info['longest']} days")
            if streak_info['longest'] > streak_info['current']:
                st.caption(f"You can beat your record!")
        
        with col3:
            st.metric("Total Days Journaled", streak_info['total_days'])
        
        # Consistency percentage
        if len(entries) > 1:
            first_entry = min(entries, key=lambda x: x['timestamp'])
            first_date = datetime.fromisoformat(first_entry['timestamp'])
            days_since_start = (datetime.now() - first_date).days + 1
            consistency_pct = (streak_info['total_days'] / days_since_start) * 100
            
            st.progress(consistency_pct / 100)
            st.caption(f"You've journaled on {consistency_pct:.0f}% of days since you started")
        
        st.divider()
        
        # Recommendations
        st.subheader(" Personalized Recommendations")
        
        # Calculate average entry length
        avg_length = sum(e.get('word_count', 0) for e in filtered_entries) / len(filtered_entries)
        
        recommendations = []
        
        if streak_info['current'] == 0:
            recommendations.append("**Start a streak**: Try to journal for 3 days in a row to build momentum.")
        elif streak_info['current'] < 7:
            recommendations.append(f"**Keep going**: You're at {streak_info['current']} days. Can you reach 7?")
        
        if avg_length < 100:
            recommendations.append("**Write more**: Try to write at least 100-150 words per entry for deeper reflection.")
        
        # Check sentiment trends
        recent_entries = filtered_entries[:5]
        recent_negative = sum(1 for e in recent_entries if e.get('sentiment_label') == 'NEGATIVE')
        if recent_negative >= 4:
            recommendations.append("**Self-care reminder**: Your recent entries show some stress. Remember to take care of yourself.")
        
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("🌟 You're doing great! Keep up the excellent journaling practice!")

# Sidebar additional info
with st.sidebar:
    st.markdown("### About Your Insights")
    st.markdown("""
    This page uses AI to analyze:
    - **Sentiment**: How positive or negative your entries are
    - **Themes**: What topics you write about
    - **Patterns**: Your writing habits and consistency
    
    All analysis happens privately on your device.
    """)
    
    st.divider()
    
    if entries:
        st.markdown("### Quick Stats")
        st.metric("Oldest Entry", datetime.fromisoformat(entries[-1]['timestamp']).strftime('%b %d, %Y'))
        st.metric("Most Recent", datetime.fromisoformat(entries[0]['timestamp']).strftime('%b %d, %Y'))