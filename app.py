import streamlit as st
from transformers import pipeline, DistilBertTokenizer
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from collections import Counter
import re

# Page configuration
st.set_page_config(
    page_title="Serenity AI",
    layout="wide"
)

