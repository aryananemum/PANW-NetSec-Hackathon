import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import DatabaseManager
from utils.helper import format_date

st.set_page_config(page_title="Past Entries", page_icon="", layout="wide")

# Initialize
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

# Header
st.title("Your Journal History")
st.markdown("*Reflect on your past thoughts and experiences*")

# Get all entries
entries = st.session_state.db.get_all_entries()

if not entries:
    st.info(" No entries yet. Start writing to build your journal!")
    
    if st.button(" Write Your First Entry"):
        st.switch_page("newentry.py")
else:
    # Search and filter sidebar
    with st.sidebar:
        st.markdown("###  Search & Filter")
        
        # Search
        search_query = st.text_input("Search entries", placeholder="Search by content...")
        
        # Filter by sentiment
        sentiment_filter = st.multiselect(
            "Filter by sentiment",
            ["POSITIVE", "NEGATIVE"],
            default=["POSITIVE", "NEGATIVE"]
        )
        
        # Date range filter
        st.markdown("#### Date Range")
        if len(entries) > 0:
            min_date = datetime.fromisoformat(entries[-1]['timestamp']).date()
            max_date = datetime.fromisoformat(entries[0]['timestamp']).date()
            
            date_range = st.date_input(
                "Select date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        # Sort options
        sort_by = st.selectbox(
            "Sort by",
            ["Newest first", "Oldest first", "Longest first", "Shortest first"]
        )
    
    # Apply filters
    filtered_entries = entries.copy()
    
    # Search filter
    if search_query:
        filtered_entries = [
            e for e in filtered_entries 
            if search_query.lower() in e['content'].lower()
        ]
    
    # Sentiment filter
    filtered_entries = [
        e for e in filtered_entries 
        if e.get('sentiment_label') in sentiment_filter or not e.get('sentiment_label')
    ]
    
    # Date range filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_entries = [
            e for e in filtered_entries
            if start_date <= datetime.fromisoformat(e['timestamp']).date() <= end_date
        ]
    
    # Apply sorting
    if sort_by == "Newest first":
        filtered_entries = sorted(filtered_entries, key=lambda x: x['timestamp'], reverse=True)
    elif sort_by == "Oldest first":
        filtered_entries = sorted(filtered_entries, key=lambda x: x['timestamp'])
    elif sort_by == "Longest first":
        filtered_entries = sorted(filtered_entries, key=lambda x: x.get('word_count', 0), reverse=True)
    elif sort_by == "Shortest first":
        filtered_entries = sorted(filtered_entries, key=lambda x: x.get('word_count', 0))
    
    # Display count
    st.markdown(f"*Showing {len(filtered_entries)} of {len(entries)} entries*")
    
    if not filtered_entries:
        st.warning("No entries match your filters. Try adjusting your search criteria.")
    else:
        # Pagination
        entries_per_page = 5
        total_pages = (len(filtered_entries) - 1) // entries_per_page + 1
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Pagination controls
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button(" Previous", disabled=st.session_state.current_page == 1):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"<h4 style='text-align: center;'>Page {st.session_state.current_page} of {total_pages}</h4>", 
                       unsafe_allow_html=True)
        
        with col3:
            if st.button("Next", disabled=st.session_state.current_page == total_pages):
                st.session_state.current_page += 1
                st.rerun()
        
        st.divider()
        
        # Calculate pagination
        start_idx = (st.session_state.current_page - 1) * entries_per_page
        end_idx = start_idx + entries_per_page
        page_entries = filtered_entries[start_idx:end_idx]
        
        # Display entries
        for idx, entry in enumerate(page_entries):
            # Create a card-like display for each entry
            with st.container():
                # Header with date and sentiment
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"###  {format_date(entry['timestamp'])}")
                
                with col2:
                    if entry.get('sentiment_label'):
                        sentiment_emoji = "😊" if entry['sentiment_label'] == 'POSITIVE' else "😔"
                        st.markdown(f"**{sentiment_emoji} {entry['sentiment_label']}**")
                
                with col3:
                    st.markdown(f"**{entry.get('word_count', 0)} words**")
                
                # Prompt if available
                if entry.get('prompt'):
                    st.markdown(f"* Prompt: {entry['prompt']}*")
                
                # Entry content
                with st.expander(" Read Entry", expanded=False):
                    st.markdown(entry['content'])
                    
                    st.divider()
                    
                    # Analysis details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if entry.get('sentiment_label'):
                            score = entry.get('sentiment_score', 0) * 100
                            st.markdown(f"""
                            **Sentiment Analysis:**
                            - Label: {entry['sentiment_label']}
                            - Confidence: {score:.1f}%
                            """)
                    
                    with col2:
                        if entry.get('themes'):
                            themes_str = ", ".join([
                                t[0] if isinstance(t, (list, tuple)) else str(t) 
                                for t in entry['themes']
                            ])
                            st.markdown(f"""
                            **Detected Themes:**
                            - {themes_str}
                            """)
                    
                    # Metrics
                    st.markdown("**Entry Metrics:**")
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    
                    with metric_col1:
                        st.metric("Words", entry.get('word_count', 0))
                    
                    with metric_col2:
                        st.metric("Tokens", entry.get('token_count', 0))
                    
                    with metric_col3:
                        st.metric("Unique Words", entry.get('unique_words', 0))
                    
                    # Action buttons
                    st.divider()
                    
                    col_a, col_b = st.columns([1, 4])
                    
                    with col_a:
                        if st.button(" Delete", key=f"delete_{entry['id']}", type="secondary"):
                            if st.session_state.db.delete_entry(entry['id']):
                                st.success("Entry deleted!")
                                st.rerun()
                            else:
                                st.error("Failed to delete entry")
                
                st.markdown("---")
        
        # Bottom pagination
        st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button(" Prev", disabled=st.session_state.current_page == 1, key="bottom_prev"):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col2:
            # Page selector
            page_num = st.number_input(
                "Go to page",
                min_value=1,
                max_value=total_pages,
                value=st.session_state.current_page,
                step=1,
                key="page_selector"
            )
            if page_num != st.session_state.current_page:
                st.session_state.current_page = page_num
                st.rerun()
        
        with col3:
            if st.button("Next ", disabled=st.session_state.current_page == total_pages, key="bottom_next"):
                st.session_state.current_page += 1
                st.rerun()

# Sidebar stats
with st.sidebar:
    st.divider()
    st.markdown("### Collection Stats")
    
    if entries:
        stats = st.session_state.db.get_statistics()
        
        st.metric("Total Entries", stats['total_entries'])
        st.metric("Total Words", f"{stats['total_words']:,}")
        
        # Most common theme
        from collections import Counter
        all_themes = []
        for entry in entries:
            if entry.get('themes'):
                for theme_data in entry['themes']:
                    if isinstance(theme_data, (list, tuple)) and len(theme_data) >= 1:
                        all_themes.append(theme_data[0])
        
        if all_themes:
            top_theme = Counter(all_themes).most_common(1)[0]
            st.metric("Top Theme", top_theme[0])
    
    st.divider()
    
    st.markdown("###  Tip")
    st.info("Use the search and filters to find specific entries or reflect on particular time periods.")