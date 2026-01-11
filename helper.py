import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
from typing import List, Dict

def create_sentiment_timeline(entries: List[Dict]):
    """Create a timeline visualization of sentiment"""
    if not entries:
        return None
    
    df_data = []
    for entry in entries:
        if entry.get('sentiment_label'):
            score = entry['sentiment_score'] if entry['sentiment_label'] == 'POSITIVE' else -entry['sentiment_score']
            df_data.append({
                'date': pd.to_datetime(entry['timestamp']),
                'sentiment': score,
                'label': entry['sentiment_label']
            })
    
    if not df_data:
        return None
    
    df = pd.DataFrame(df_data)
    
    fig = px.line(df, x='date', y='sentiment', 
                  title='Your Emotional Journey',
                  labels={'sentiment': 'Sentiment Score', 'date': 'Date'},
                  markers=True)
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(height=400, hovermode='x unified')
    
    return fig

def create_theme_distribution(entries: List[Dict]):
    """Create a visualization of theme distribution"""
    if not entries:
        return None
    
    theme_counts = Counter()
    for entry in entries:
        if entry.get('themes'):
            for theme_data in entry['themes']:
                if isinstance(theme_data, (list, tuple)) and len(theme_data) >= 2:
                    theme, score = theme_data[0], theme_data[1]
                    theme_counts[theme] += score
    
    if not theme_counts:
        return None
    
    df = pd.DataFrame([
        {'theme': theme, 'frequency': count} 
        for theme, count in theme_counts.most_common(8)
    ])
    
    fig = px.bar(df, x='frequency', y='theme', orientation='h',
                 title='Your Most Common Themes',
                 labels={'frequency': 'Frequency', 'theme': 'Theme'},
                 color='frequency',
                 color_continuous_scale='Blues')
    fig.update_layout(height=400, showlegend=False)
    
    return fig

def create_writing_volume_chart(entries: List[Dict]):
    """Create a chart showing writing volume over time"""
    if not entries:
        return None
    
    df_data = []
    for entry in entries:
        df_data.append({
            'date': pd.to_datetime(entry['timestamp']).date(),
            'word_count': entry.get('word_count', 0)
        })
    
    df = pd.DataFrame(df_data)
    df_grouped = df.groupby('date')['word_count'].sum().reset_index()
    
    fig = px.bar(df_grouped, x='date', y='word_count',
                 title='Writing Volume Over Time',
                 labels={'word_count': 'Words Written', 'date': 'Date'},
                 color='word_count',
                 color_continuous_scale='Greens')
    fig.update_layout(height=300)
    
    return fig

def generate_weekly_summary(entries: List[Dict]) -> str:
    """Generate insights from the past week's entries"""
    if not entries:
        return "Start journaling to receive personalized insights!"
    
    week_ago = datetime.now() - timedelta(days=7)
    recent_entries = [
        e for e in entries 
        if datetime.fromisoformat(e['timestamp']) > week_ago
    ]
    
    if not recent_entries:
        return "No entries from the past week. Keep journaling to see insights!"
    
    summary = f"**Weekly Reflection ({len(recent_entries)} entries this week)**\n\n"
    
    # Sentiment summary
    sentiments = [e['sentiment_label'] for e in recent_entries 
                  if e.get('sentiment_label')]
    if sentiments:
        positive_count = sentiments.count('POSITIVE')
        positive_pct = (positive_count / len(sentiments)) * 100
        summary += f"📊 **Emotional Tone:** {positive_pct:.0f}% of your entries had a positive sentiment.\n\n"
    
    # Theme summary
    all_themes = []
    for entry in recent_entries:
        if entry.get('themes'):
            for theme_data in entry['themes']:
                if isinstance(theme_data, (list, tuple)) and len(theme_data) >= 1:
                    all_themes.append(theme_data[0])
    
    if all_themes:
        top_themes = Counter(all_themes).most_common(3)
        summary += f"🎯 **Top Themes:** You wrote most about {', '.join([t[0] for t in top_themes])}.\n\n"
    
    # Word count
    avg_words = sum(e.get('word_count', 0) for e in recent_entries) / len(recent_entries)
    summary += f"✍️ **Writing Volume:** Average of {avg_words:.0f} words per entry.\n\n"
    
    # Pattern recognition
    summary += "💡 **Insights:**\n"
    theme_list = [t[0] for t in top_themes] if all_themes else []
    
    if 'work stress' in theme_list:
        summary += "- You've been processing work-related stress. Remember to schedule breaks.\n"
    if 'gratitude' in theme_list:
        summary += "- You're practicing gratitude! This is linked to improved mental wellbeing.\n"
    if positive_pct > 70:
        summary += "- You're experiencing a positive period! What's contributing to this?\n"
    elif positive_pct < 40:
        summary += "- You might benefit from self-care activities. What brings you joy?\n"
    
    if avg_words > 200:
        summary += "- You're writing detailed entries. This depth can lead to better self-understanding.\n"
    
    return summary

def format_date(iso_string: str) -> str:
    """Format ISO datetime string to readable format"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return iso_string

def get_streak_info(entries: List[Dict]) -> Dict:
    """Calculate journaling streak information"""
    if not entries:
        return {'current': 0, 'longest': 0, 'total_days': 0}
    
    dates = sorted(list(set([
        datetime.fromisoformat(e['timestamp']).date() 
        for e in entries
    ])), reverse=True)
    
    if not dates:
        return {'current': 0, 'longest': 0, 'total_days': 0}
    
    # Current streak
    current_streak = 1
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i+1]).days == 1:
            current_streak += 1
        else:
            break
    
    # Longest streak
    longest_streak = 1
    temp_streak = 1
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i+1]).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1
    
    return {
        'current': current_streak,
        'longest': longest_streak,
        'total_days': len(dates)
    }

def export_to_markdown(entries: List[Dict]) -> str:
    """Export entries to markdown format"""
    md = "# My Journal Entries\n\n"
    md += f"Exported on {datetime.now().strftime('%B %d, %Y')}\n\n"
    md += "---\n\n"
    
    for entry in sorted(entries, key=lambda x: x['timestamp'], reverse=True):
        md += f"## {format_date(entry['timestamp'])}\n\n"
        
        if entry.get('prompt'):
            md += f"**Prompt:** *{entry['prompt']}*\n\n"
        
        md += f"{entry['content']}\n\n"
        
        if entry.get('sentiment_label'):
            md += f"**Sentiment:** {entry['sentiment_label']}\n"
        
        if entry.get('themes'):
            themes_str = ", ".join([t[0] if isinstance(t, (list, tuple)) else str(t) for t in entry['themes']])
            md += f"**Themes:** {themes_str}\n"
        
        md += "\n---\n\n"
    
    return md