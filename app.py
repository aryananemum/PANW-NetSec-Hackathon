import streamlit as st
from transformers import pipeline, DistilBertTokenizer
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from collections import Counter
import re
import os
import sys
from db import DatabaseManager


sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

# Page configuration
st.set_page_config(
    page_title="Serenity AI",
    layout="wide"
)

# Initialize database manager
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

st.markdown(get_custom_css(), unsafe_allow_html=True)

# Main page content
st.markdown('<div class="main-header"><h1>AI Journaling Companion</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your private space for reflection and growth</div>', unsafe_allow_html=True)

# Welcome section with feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card animate-fade-in">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
        <h3>Smart Prompts</h3>
        <p style="color: #64748b;">Get AI-generated prompts based on your writing patterns and emotional state.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card animate-fade-in" style="animation-delay: 0.1s;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <h3>Deep Insights</h3>
        <p style="color: #64748b;">Discover patterns in your thoughts and emotions with sentiment analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card animate-fade-in" style="animation-delay: 0.2s;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
        <h3>Private & Secure</h3>
        <p style="color: #64748b;">All your data stays on your device. Complete privacy guaranteed.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

