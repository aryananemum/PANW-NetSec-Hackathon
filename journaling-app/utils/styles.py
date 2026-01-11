"""
Custom CSS styles for the AI Journaling Companion
"""

def get_custom_css():
    """Returns custom CSS for the application"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #1e3a8a;
    }
    
    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }
    
    /* Main Header Styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 300;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Card Styles */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Prompt Card */
    .prompt-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
        border: none;
    }
    
    .prompt-card h4 {
        color: white !important;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .prompt-card p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.15rem;
        line-height: 1.6;
        font-style: italic;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton > button[kind="secondary"] {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }
    
    /* Text Area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f8fafc;
        border-color: #667eea;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 600;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1rem 1.5rem;
    }
    
    div[data-baseweb="notification"] {
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Success Message */
    .element-container:has(.stSuccess) {
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Select Box / Input */
    .stSelectbox, .stTextInput, .stNumberInput {
        border-radius: 8px;
    }
    
    .stSelectbox > div > div, 
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border-color: #e2e8f0;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
        border: 2px dashed #cbd5e1;
        padding: 2rem;
        background: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Custom Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-positive {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-negative {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .badge-neutral {
        background: #f1f5f9;
        color: #475569;
    }
    
    /* Custom Entry Card */
    .entry-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .entry-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateX(4px);
    }
    
    /* Sentiment Indicator */
    .sentiment-positive {
        color: #16a34a;
        font-weight: 600;
    }
    
    .sentiment-negative {
        color: #dc2626;
        font-weight: 600;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Data Frame */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        margin: 0.25rem 0;
        transition: all 0.3s ease;
    }
    
    .stRadio > label:hover {
        border-color: #667eea;
        background: #f8fafc;
    }
    
    /* Checkbox */
    .stCheckbox {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #64748b;
        font-size: 0.875rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
    
    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease;
    }
    
    /* Glassmorphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    
    /* Feature Cards on Home Page */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        border-top: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-top-color: #764ba2;
    }
    
    .feature-card h3 {
        color: #1e3a8a;
        margin-bottom: 1rem;
    }
    
    /* Page Title Container */
    .page-title-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
    }
    
    .page-title-container h1 {
        color: white !important;
        -webkit-text-fill-color: white !important;
        margin: 0;
    }
    
    .page-title-container p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make it responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .prompt-card {
            padding: 1.5rem;
        }
        
        .custom-card {
            padding: 1rem;
        }
    }
    </style>
    """

def get_sentiment_badge(sentiment_label, sentiment_score=None):
    """Generate a styled sentiment badge"""
    if sentiment_label == 'POSITIVE':
        emoji = "😊"
        badge_class = "badge-positive"
    else:
        emoji = "😔"
        badge_class = "badge-negative"
    
    score_text = f" ({sentiment_score:.0%})" if sentiment_score else ""
    
    return f'<span class="badge {badge_class}">{emoji} {sentiment_label}{score_text}</span>'

def get_theme_badges(themes):
    """Generate styled theme badges"""
    if not themes:
        return ""
    
    badges = []
    for theme_data in themes:
        if isinstance(theme_data, (list, tuple)) and len(theme_data) >= 1:
            theme = theme_data[0]
            badges.append(f'<span class="badge badge-neutral">🎯 {theme}</span>')
    
    return " ".join(badges)

def create_stat_card(title, value, icon="📊", color="#667eea"):
    """Create a styled stat card"""
    return f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid {color};
        margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="color: #64748b; font-size: 0.875rem; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">
                    {title}
                </p>
                <p style="color: #1e3a8a; font-size: 2rem; font-weight: 700; margin: 0.5rem 0 0 0;">
                    {value}
                </p>
            </div>
            <div style="font-size: 2.5rem;">
                {icon}
            </div>
        </div>
    </div>
    """