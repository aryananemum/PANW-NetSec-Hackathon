import streamlit as st
import sys
import os
from datetime import datetime, timedelta
from collections import Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import DatabaseManager
from helper import generate_weekly_summary

st.set_page_config(page_title="Weekly Summary", page_icon="🔍", layout="wide")

# Initialize
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

# Header
st.title("🔍 Weekly Reflection & Summary")
st.markdown("*AI-powered insights from your week of journaling*")

# Get entries
entries = st.session_state.db.get_all_entries()

if not entries:
    st.info("📝 Start journaling to receive weekly insights! Write at least a few entries to see patterns.")
else:
    # Time period selector
    st.sidebar.markdown("### Select Time Period")
    
    period = st.sidebar.radio(
        "View summary for:",
        ["Last 7 days", "Last 14 days", "Last 30 days", "Custom range"]
    )
    
    # Calculate date range
    if period == "Custom range":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=datetime.now().date() - timedelta(days=7))
        with col2:
            end_date = st.date_input("End date", value=datetime.now().date())
    else:
        days = int(period.split()[1])
        start_date = (datetime.now() - timedelta(days=days)).date()
        end_date = datetime.now().date()
    
    # Filter entries by date range
    period_entries = [
        e for e in entries
        if start_date <= datetime.fromisoformat(e['timestamp']).date() <= end_date
    ]
    
    if not period_entries:
        st.warning(f"No entries found between {start_date} and {end_date}. Try selecting a different time period.")
    else:
        # Generate summary
        summary = generate_weekly_summary(period_entries)
        
        # Display summary in a nice card
        st.markdown(f"""
        <div style='background-color: #f0f9ff; padding: 2rem; border-radius: 10px; border-left: 5px solid #0ea5e9;'>
            {summary.replace('**', '<strong>').replace('*', '</strong>')}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Detailed breakdown
        st.subheader(" Detailed Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📝 Writing Activity")
            st.metric("Total Entries", len(period_entries))
            
            total_words = sum(e.get('word_count', 0) for e in period_entries)
            st.metric("Total Words", f"{total_words:,}")
            
            avg_words = total_words / len(period_entries) if period_entries else 0
            st.metric("Avg Words/Entry", f"{avg_words:.0f}")
            
            # Days with entries
            unique_days = len(set([
                datetime.fromisoformat(e['timestamp']).date() 
                for e in period_entries
            ]))
            total_days = (end_date - start_date).days + 1
            consistency = (unique_days / total_days) * 100
            
            st.metric("Days Journaled", f"{unique_days}/{total_days}")
            st.progress(consistency / 100)
            st.caption(f"{consistency:.0f}% consistency")
        
        with col2:
            st.markdown("### 💭 Emotional Overview")
            
            # Sentiment breakdown
            sentiments = [e.get('sentiment_label') for e in period_entries if e.get('sentiment_label')]
            
            if sentiments:
                positive_count = sentiments.count('POSITIVE')
                negative_count = sentiments.count('NEGATIVE')
                total = len(sentiments)
                
                st.metric("Positive Entries", f"{positive_count}/{total}")
                st.metric("Negative Entries", f"{negative_count}/{total}")
                
                # Sentiment pie chart
                import plotly.graph_objects as go
                
                fig = go.Figure(data=[go.Pie(
                    labels=['Positive', 'Negative'],
                    values=[positive_count, negative_count],
                    hole=.3,
                    marker_colors=['#10b981', '#ef4444']
                )])
                
                fig.update_layout(
                    showlegend=True,
                    height=250,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough sentiment data for this period.")
        
        with col3:
            st.markdown("### Top Themes")
            
            # Collect all themes
            all_themes = []
            for entry in period_entries:
                if entry.get('themes'):
                    for theme_data in entry['themes']:
                        if isinstance(theme_data, (list, tuple)) and len(theme_data) >= 1:
                            all_themes.append(theme_data[0])
            
            if all_themes:
                theme_counts = Counter(all_themes).most_common(5)
                
                for theme, count in theme_counts:
                    st.markdown(f"**{theme}**: {count} entries")
                
                # Theme bar chart
                import plotly.express as px
                import pandas as pd
                
                df_themes = pd.DataFrame(theme_counts, columns=['Theme', 'Count'])
                
                fig = px.bar(
                    df_themes,
                    x='Count',
                    y='Theme',
                    orientation='h',
                    color='Count',
                    color_continuous_scale='Blues'
                )
                
                fig.update_layout(
                    showlegend=False,
                    height=250,
                    margin=dict(t=0, b=0, l=0, r=0),
                    yaxis={'categoryorder': 'total ascending'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough theme data for this period.")
        
        st.divider()
        
        # Most significant entries
        st.subheader(" Highlighted Entries")
        
        # Find longest entry
        if period_entries:
            longest_entry = max(period_entries, key=lambda x: x.get('word_count', 0))
            
            with st.expander(f"Longest Entry ({longest_entry.get('word_count', 0)} words)"):
                st.markdown(f"**Date:** {datetime.fromisoformat(longest_entry['timestamp']).strftime('%B %d, %Y')}")
                st.markdown(f"**Content:**")
                st.write(longest_entry['content'])
            
            # Find most positive entry
            positive_entries = [e for e in period_entries if e.get('sentiment_label') == 'POSITIVE']
            if positive_entries:
                most_positive = max(positive_entries, key=lambda x: x.get('sentiment_score', 0))
                
                with st.expander("Most Positive Entry"):
                    st.markdown(f"**Date:** {datetime.fromisoformat(most_positive['timestamp']).strftime('%B %d, %Y')}")
                    st.markdown(f"**Sentiment Score:** {most_positive.get('sentiment_score', 0):.2%}")
                    st.markdown(f"**Content:**")
                    st.write(most_positive['content'])
        
        st.divider()
        
        # Reflection questions
        st.subheader("Reflection Questions")
        
        st.markdown("""
        Take a moment to reflect on these questions based on your entries:
        
        1. **What patterns do you notice in your emotional journey this week?**
           - Are there specific triggers for positive or negative emotions?
           
        2. **Which themes dominated your thoughts?**
           - What does this tell you about your current priorities or concerns?
           
        3. **How consistent was your journaling practice?**
           - What helped you maintain the habit? What got in the way?
           
        4. **What would you like to focus on in the coming week?**
           - Based on your insights, what areas deserve more attention?
           
        5. **What are you grateful for from this period?**
           - What positive moments or realizations stood out?
        """)
        
        # User notes section
        st.divider()
        
        st.subheader("Your Personal Notes")
        st.markdown("*Add your own reflections on this week:*")
        
        notes = st.text_area(
            "Weekly notes",
            height=150,
            placeholder="What did you learn about yourself this week? What will you carry forward?",
            key="weekly_notes"
        )
        
        if st.button("Save Notes"):
            # Save to database as a preference
            note_key = f"notes_{start_date.isoformat()}_{end_date.isoformat()}"
            st.session_state.db.set_preference(note_key, notes)
            st.success(" Notes saved!")
        
        # Export option
        st.divider()
        
        if st.button("Export This Summary"):
            # Create markdown export
            export_content = f"""# Weekly Journal Summary
            
**Period:** {start_date} to {end_date}

{summary}

## Your Notes
{notes if notes else "No notes added"}

---
*Generated by AI Journaling Companion*
"""
            
            st.download_button(
                label="Download Summary",
                data=export_content,
                file_name=f"weekly_summary_{start_date}_{end_date}.md",
                mime="text/markdown"
            )

# Sidebar info
with st.sidebar:
    st.divider()
    
    st.markdown("### About Weekly Summaries")
    st.markdown("""
    This AI-powered summary helps you:
    - Identify emotional patterns
    - Recognize recurring themes
    - Track your consistency
    - Reflect on your growth
    
    Review your summary regularly to gain deeper self-awareness.
    """)
    
    st.divider()
    
    st.markdown("### Tips")
    st.info("""
    - Review your summary at the end of each week
    - Compare summaries month-to-month
    - Use insights to set intentions
    - Celebrate your progress!
    """)