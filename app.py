import streamlit as st
import datetime
import time
import random
import math
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import altair as alt
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stoggle import stoggle
from streamlit_extras.let_it_rain import rain
from streamlit_extras.stateful_button import button
import streamlit.components.v1 as components
import base64
import re
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os
from math import pi
import uuid
# =============================================
# CONFIGURATION AND CONSTANTS
# =============================================

# Set page configuration
st.set_page_config(
    page_title="Our Love Journey",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
LOVE_START_DATE = datetime(2024, 4, 15)
QUOTES = [
    "In your eyes, I found my home. In your heart, I found my love. In your soul, I found my forever.",
    "Every moment with you is like a beautiful dream that I never want to wake up from.",
    "You're the first person I want to talk to when I wake up and the last person I want to talk to before I sleep.",
    "My favorite place in the world is next to you.",
    "You make my heart smile in ways no one else can.",
    "If I had to choose between breathing and loving you, I would use my last breath to tell you I love you.",
    "You are my today and all of my tomorrows.",
    "Meeting you was fate, becoming your friend was a choice, but falling in love with you was beyond my control.",
    "I've fallen in love many times... but always with you.",
    "You are the reason I believe in love.",
    "With you, I am home. You are my safe place.",
    "Your love is like the lamp in the window that guides me home through the darkest night.",
    "Every day with you is a wonderful addition to my life's journey.",
    "You are my sunshine on cloudy days, my rainbow after the rain.",
    "I never knew what love was until I met you.",
    "To the world, you may be one person, but to me, you are the world.",
    "When I'm with you, hours feel like seconds. When we're apart, days feel like years.",
    "You're not just my love, you're my best friend, my confidant, and my favorite person.",
    "Your love is the energy that keeps me going when I feel like I can't.",
    "If I know what love is, it is because of you.",
    "You and I, we're a team. There's nothing we can't handle together.",
    "I love you not only for what you are, but for what I am when I am with you.",
    "You are the missing piece to my puzzle. With you, I am complete.",
    "Every beat of my heart belongs to you.",
    "In a world full of people, my soul recognized yours.",
    "I promise to choose you every day, in every moment, for the rest of my life.",
    "You have made flowers grow where I thought the garden was dead.",
    "I never believed in soulmates until I met you.",
    "Being in your arms is my happy place. I could stay there forever.",
    "My love for you is a journey, starting at forever and ending at never."
]

SURPRISE_MESSAGES = [
    "I've prepared a special date night just for us! Check your messages for details...",
    "I'm sending you a virtual hug! Can you feel it? 🤗",
    "Let's make a bucket list of adventures we want to experience together!",
    "I've written you a love letter. Check under your pillow tonight...",
    "Let's plan our next getaway, just the two of us!",
    "I promise to always be your biggest supporter and best friend.",
    "Today, I love you more than yesterday, but less than tomorrow.",
    "Let's dance together in the moonlight tonight!",
    "I can't wait to grow old with you and still hold hands.",
    "Let's try that new restaurant you've been talking about this weekend!",
    "I've been thinking about our future together, and it's beautiful.",
    "Let's take a spontaneous road trip this weekend!",
    "I just wanted to remind you how amazing you are.",
    "Let's stay up late tonight and count the stars.",
    "I've planned a movie night with all your favorites!",
    "How about we go on a sunset picnic this evening?",
    "I can't stop thinking about that moment when we first met...",
    "Let's recreate our first date this weekend!",
    "I've hidden little love notes around for you to find today.",
    "Let's make breakfast together in pajamas this weekend!"
]

SPECIAL_MILESTONES = {
    30: {"title": "1 Month Together!", "description": "It's been a magical month since our paths crossed."},
    100: {"title": "100 Days of Love!", "description": "Triple digits of loving you more each day."},
    180: {"title": "Half a Year of Magic", "description": "180 days of building our beautiful story."},
    365: {"title": "Our First Anniversary!", "description": "A full year of loving you more each day."}
}

RELATIONSHIP_MILESTONES = [
    {"date": "April 15, 2024", "title": "First Chat", "description": "Where our story began with a simple message", "emoji": "💬"},
    {"date": "May 15, 2024", "title": "One Month Together", "description": "Our first month milestone", "emoji": "🌱"},
    {"date": "July 24, 2024", "title": "100 Days of Love", "description": "Triple digits of happiness", "emoji": "💯"},
    {"date": "October 12, 2024", "title": "Six Months Together", "description": "Half a year of beautiful memories", "emoji": "🎊"},
    {"date": "April 15, 2025", "title": "First Anniversary", "description": "One year of us ❤️", "emoji": "🎂"}
]

# Secret key and message
SECRET_KEY = "H"
SECRET_MESSAGE = """
My dearest one,

From the moment our paths crossed, I knew there was something extraordinary about you. 
The way you smile, the sound of your laughter, the depth in your eyes - everything about you captivates me.

Every day with you is a gift I cherish. When we're together, the world seems brighter, and when we're apart, 
thoughts of you keep me warm. You've shown me what it means to truly love and be loved.

I promise to stand by you through every triumph and challenge, to hold your hand when you need strength, 
and to celebrate every beautiful moment life offers us.

You are my heart's favorite person, my soul's perfect match, and my life's greatest blessing.

Forever yours,
With all my love ❤️
"""

# =============================================
# CSS STYLING
# =============================================

def load_css():
    """Load CSS styles for the app"""
    st.markdown("""
    <style>
        /* General Styling */
        .stApp {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }
        
        /* Background Gradient Animation */
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        .main {
            background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #a18cd1, #fbc2eb);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        /* Headers */
        h1 {
            color: #4a2970;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        }
        
        h2, h3 {
            color: #4a2970;
            font-weight: 600;
        }
        
        /* Cards */
        .card {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 7px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Love Counter */
        .love-counter {
            text-align: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: #e83e8c;
            margin-bottom: 1rem;
            padding: 1rem;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(232, 62, 140, 0.3);
        }
        
        /* Glowing Text Effect */
        @keyframes glow {
            0% {text-shadow: 0 0 5px #ff66b2, 0 0 10px #ff66b2;}
            50% {text-shadow: 0 0 20px #ff66b2, 0 0 30px #ff66b2;}
            100% {text-shadow: 0 0 5px #ff66b2, 0 0 10px #ff66b2;}
        }
        
        .glow-text {
            animation: glow 2s ease-in-out infinite;
            color: #e83e8c;
            font-weight: bold;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #ff66b2;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(255, 102, 178, 0.3);
        }
        
        .stButton>button:hover {
            background-color: #e83e8c;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(232, 62, 140, 0.4);
        }
        
        .stButton>button:active {
            transform: translateY(1px);
        }
        
        /* Quote styling */
        .quote-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-style: italic;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            border-left: 5px solid #ff66b2;
            border-radius: 5px;
            margin: 20px 0;
            position: relative;
        }
        
        .quote-container::before {
            content: '"';
            font-size: 50px;
            color: rgba(232, 62, 140, 0.2);
            position: absolute;
            top: -10px;
            left: 5px;
        }
        
        .quote-container::after {
            content: '"';
            font-size: 50px;
            color: rgba(232, 62, 140, 0.2);
            position: absolute;
            bottom: -40px;
            right: 5px;
        }
        
        /* Clock styling */
        .clock {
            font-family: 'Courier New', monospace;
            font-size: 1.4rem;
            font-weight: 600;
            color: #6c5ce7;
            text-align: center;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(108, 92, 231, 0.2);
        }
        
        /* Milestone styling */
        .milestone {
            padding: 15px;
            border-left: 3px solid #ff66b2;
            margin-bottom: 20px;
            position: relative;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 0 10px 10px 0;
            transition: transform 0.3s ease;
        }
        
        .milestone:hover {
            transform: translateX(5px);
        }
        
        .milestone::before {
            content: "";
            position: absolute;
            left: -8px;
            top: 15px;
            width: 15px;
            height: 15px;
            background-color: #ff66b2;
            border-radius: 50%;
            border: 2px solid white;
        }
        
        .milestone-date {
            font-weight: 600;
            color: #555;
            font-size: 0.9rem;
        }
        
        .milestone-title {
            font-weight: 700;
            color: #333;
            margin: 5px 0;
        }
        
        .milestone-description {
            color: #666;
        }
        
        /* Progress bar styling */
        .progress-container {
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 20px;
            height: 30px;
            width: 100%;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #ff66b2, #e83e8c);
            border-radius: 20px;
            height: 100%;
            text-align: center;
            transition: width 1s ease;
            color: white;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(232, 62, 140, 0.3);
        }
        
        /* Pulse effect */
        @keyframes pulse {
            0% {box-shadow: 0 0 0 0 rgba(255, 102, 178, 0.7);}
            70% {box-shadow: 0 0 0 15px rgba(255, 102, 178, 0);}
            100% {box-shadow: 0 0 0 0 rgba(255, 102, 178, 0);}
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        /* Secret button */
        .secret-button {
            background: none;
            border: none;
            color: rgba(0, 0, 0, 0.1);
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .secret-button:hover {
            color: rgba(232, 62, 140, 0.5);
        }
        
        /* Secret message container */
        .secret-message {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            max-width: 80%;
            margin: 0 auto;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            white-space: pre-line;
        }
        
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(20px);}
            to {opacity: 1; transform: translateY(0);}
        }
        
        .fade-in {
            animation: fadeIn 1s ease-out forwards;
        }
        
        /* Typewriter effect */
        @keyframes typing {
            from {width: 0;}
            to {width: 100%;}
        }
        
        .typewriter {
            overflow: hidden;
            white-space: nowrap;
            border-right: 3px solid #ff66b2;
            animation: 
                typing 3.5s steps(40, end),
                blink-caret 0.75s step-end infinite;
        }
        
        @keyframes blink-caret {
            from, to {border-color: transparent;}
            50% {border-color: #ff66b2;}
        }
        
        /* Surprise animation */
        @keyframes slideIn {
            from {transform: translateY(50px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }
        
        .surprise-message {
            animation: slideIn 0.5s ease-out forwards;
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #ff66b2;
        }
        
        /* Special celebration for anniversary */
        .celebration {
            padding: 30px;
            background: linear-gradient(135deg, #fad0c4 0%, #ff9a9e 100%);
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(255, 154, 158, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .celebration h2 {
            color: white;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
        
        .celebration p {
            color: white;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }
        
        /* Floating Hearts Animation */
        .floating-heart {
            position: fixed;
            color: rgba(232, 62, 140, 0.7);
            z-index: 99;
            animation-name: float-heart;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
            animation-direction: alternate;
        }
        
        @keyframes float-heart {
            0% {transform: translateY(0) rotate(0deg);}
            100% {transform: translateY(-20px) rotate(10deg);}
        }
        
        /* Confetti animation */
        @keyframes confetti-fall {
            0% {transform: translateY(-100px) rotate(0deg);}
            100% {transform: translateY(calc(100vh)) rotate(720deg);}
        }
        
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background-color: #f00;
            z-index: 1000;
            animation: confetti-fall linear forwards;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .card {
                padding: 15px;
            }
            
            .love-counter {
                font-size: 1.2rem;
            }
            
            .clock {
                font-size: 1.1rem;
            }
            
            .milestone {
                padding: 10px;
            }
            
            .celebration {
                padding: 20px;
            }
            
            .secret-message {
                padding: 20px;
                max-width: 95%;
            }
        }
    </style>

    """, unsafe_allow_html=True)
def render_daily_rose_bloom():
    st.markdown("<h2>🌹 Daily Blooming Roses</h2>", unsafe_allow_html=True)

    # Set first visit date (if not already)
    if "first_visit" not in st.session_state:
        st.session_state.first_visit = datetime.today().strftime('%Y-%m-%d')

    # Calculate days since first visit
    first_date = datetime.strptime(st.session_state.first_visit, '%Y-%m-%d')
    today = datetime.today()
    days_passed = (today - first_date).days + 1  # include first day

    # Romantic messages
    messages = [
        "Another day, another reason to love you more.",
        "Like this rose, our love keeps blooming.",
        "You're the sunshine that makes me blossom.",
        "Every petal holds a memory of you.",
        "With you, every day is a spring day.",
        "You're the poetry in my petals.",
        "My heart blooms only for you.",
        "You're my garden of forever.",
        "Love grows where you are.",
        "Forever isn't long enough with you.",
    ]

    # Display roses (max 30 to keep page fast)
    for i in range(min(days_passed, 30)):
        msg = messages[i % len(messages)]
        st.markdown(f"""
        <div style="margin-bottom: 20px; animation: fadeIn 1s ease;">
            <span style="font-size: 32px;">🌹</span>
            <span style="font-size: 1.1em; margin-left: 10px;">{msg}</span>
        </div>
        """, unsafe_allow_html=True)

    # Fade-in CSS animation
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
    """, unsafe_allow_html=True)
# Place this after your existing load_css() function
def reasons_i_love_you():
    """Display a beautiful 'Reasons I Love You' counter with heartfelt reasons"""
    st.markdown("<h2 style='text-align: center; color: #ff6b6b;'>💘 Reasons Why I Love You, Faryal 💘</h2>", unsafe_allow_html=True)
    
    # Create a beautiful container for the reasons
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffccd5 0%, #ffc8dd 50%, #ffafcc 100%); 
                padding: 20px; 
                border-radius: 15px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin: 20px 0;'>
        <p style='font-size: 18px; color: #590d22; font-style: italic;'>Click to discover why you're my everything...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # List of heartfelt, specific reasons
    reasons = [
        "The way your eyes light up when you laugh makes my heart skip a beat every time.",
        "Your kindness and compassion toward others shows the beautiful soul you truly are.",
        "The strength you show when facing challenges inspires me to be a better person.",
        "The sound of your voice is the most soothing melody to my ears.",
        "The way you remember the little details about my day shows how deeply you care.",
        "Your creativity and imagination bring color and joy to my world.",
        "The gentle touch of your hand feels like home to me.",
        "Your determination to achieve your dreams makes me proud every single day.",
        "The way you make even ordinary moments feel magical and special.",
        "Your wisdom and insight help me see the world in new, beautiful ways.",
        "The comfort I feel in your silence is as profound as in your words.",
        "Your smile is the first thing I want to see every morning for the rest of my life.",
        "The way you love me despite knowing all my flaws makes me feel truly blessed.",
        "Your intelligence and thoughtfulness in every conversation we have.",
        "The support you give me through difficult times is my greatest strength.",
        "Your passion for the things you love is absolutely captivating.",
        "The way you dance like nobody's watching brings pure joy to my heart.",
        "Your patience with me when I'm at my worst shows your unconditional love.",
        "The dreams we share for our future fill me with hope and excitement.",
        "Your laughter is the most beautiful sound in the entire world to me.",
        "The peace I feel when I'm by your side cannot be found anywhere else.",
        "Your courage to try new things inspires me to step out of my comfort zone.",
        "The way you care for our home makes it truly feel like a sanctuary.",
        "Your ability to see the good in everyone reflects your beautiful heart.",
        "The way you've grown with me through our journey together.",
        "Your thoughtfulness in the gifts you choose shows how well you know me.",
        "The way you understand me without words being spoken.",
        "Your grace and elegance in everything you do takes my breath away.",
        "The little notes and messages you leave for me brighten my entire day.",
        "Your faith in us gives me strength when I need it most.",
        "The way your presence alone can calm my anxieties.",
        "Your resilience through life's challenges is truly admirable.",
        "The warmth in your eyes when you look at me still gives me butterflies.",
        "Your ability to make me laugh even on my darkest days is priceless.",
        "The way you believe in me more than I believe in myself.",
        "Your honesty and integrity in all aspects of life is something I deeply respect.",
        "The dreams you've helped me achieve would have been impossible without you.",
        "Your selflessness and willingness to put others first speaks volumes about your character.",
        "The way you've helped me become the best version of myself.",
        "Your love has been my greatest blessing, and I thank the stars for you every day."
    ]
    
    # Button to generate a new reason
    if st.button("Click For Another Reason I Love You 💖", key="love_reason_btn"):
        # Get a random reason but avoid repetition if possible
        if 'shown_reasons' not in st.session_state:
            st.session_state.shown_reasons = []
        
        # Reset if we've shown all reasons
        if len(st.session_state.shown_reasons) >= len(reasons):
            st.session_state.shown_reasons = []
        
        # Get available reasons
        available_reasons = [r for r in reasons if r not in st.session_state.shown_reasons]
        if not available_reasons:
            available_reasons = reasons
        
        # Select a random reason
        reason = random.choice(available_reasons)
        st.session_state.shown_reasons.append(reason)
        
        # Display with animation effect
        st.markdown(f"""
        <div class="animated-reason" style='
            background-color: rgba(255, 255, 255, 0.8);
            border-left: 5px solid #ff4d6d;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 22px;
            color: #590d22;
            text-align: center;
            font-style: italic;
            box-shadow: 0 4px 15px rgba(255, 77, 109, 0.2);
            animation: fadeIn 1.5s;'>
            "{reason}"
        </div>
        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animated-reason {{
            animation: fadeIn 1.5s;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Add a heart animation when reason is displayed
        st.balloons()
def render_theme_selector():
    """Render a theme selector for customizing the app appearance"""
    themes = {
        "Default": {
            "background": "linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #a18cd1, #fbc2eb)",
            "primary_color": "#ff66b2",
            "secondary_color": "#4a2970"
        },
        "Ocean Love": {
            "background": "linear-gradient(-45deg, #89f7fe, #66a6ff, #4facfe, #00f2fe)",
            "primary_color": "#0066cc",
            "secondary_color": "#004080"
        },
        "Sunset Romance": {
            "background": "linear-gradient(-45deg, #ffc3a0, #ffafbd, #ff9a9e, #fad0c4)",
            "primary_color": "#ff6b6b",
            "secondary_color": "#994444"
        },
        "Forest Dreams": {
            "background": "linear-gradient(-45deg, #d4fc79, #96e6a1, #c1dfc4, #a8edea)",
            "primary_color": "#4caf50",
            "secondary_color": "#2e7d32"
        }
    }
    
    # Get current theme from session state or set default
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "Default"
    
    # Add theme selector to sidebar
    with st.sidebar:
        st.markdown("<h3>Customize Our App</h3>", unsafe_allow_html=True)
        selected_theme = st.selectbox(
            "Choose a theme",
            list(themes.keys()),
            index=list(themes.keys()).index(st.session_state.app_theme)
        )
        
        if selected_theme != st.session_state.app_theme:
            st.session_state.app_theme = selected_theme
            st.rerun()
    
    # Apply selected theme
    current_theme = themes[st.session_state.app_theme]
    
    st.markdown(
        f"""
        <style>
            .main {{
                background: {current_theme["background"]};
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
            }}
            
            h1, h2, h3 {{
                color: {current_theme["secondary_color"]};
            }}
            
            .glow-text {{
                color: {current_theme["primary_color"]};
            }}
            
            .stButton>button {{
                background-color: {current_theme["primary_color"]};
            }}
            
            .stButton>button:hover {{
                background-color: {current_theme["primary_color"]}dd;
            }}
            
            .milestone::before {{
                background-color: {current_theme["primary_color"]};
            }}
            
            .progress-bar {{
                background: linear-gradient(90deg, {current_theme["primary_color"]}, {current_theme["secondary_color"]});
            }}
            
            .quote-container {{
                border-left: 5px solid {current_theme["primary_color"]};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
# =============================================
# HELPER FUNCTIONS
# =============================================

def get_days_together():
    """Calculate days together since the start date"""
    today = datetime.now().date()
    start = LOVE_START_DATE.date()
    return (today - start).days

def is_special_date():
    """Check if today is a special date (anniversary or milestone)"""
    today = datetime.now().date()
    start = LOVE_START_DATE.date()
    days_together = (today - start).days
    
    # Check if it's a monthly anniversary (same day of month)
    monthly = today.day == start.day and (today.month != start.month or today.year != start.year)
    
    # Check if it's a milestone day
    is_milestone = days_together in SPECIAL_MILESTONES
    
    # Check if it's the anniversary date
    anniversary = today.day == start.day and today.month == start.month and today.year > start.year
    
    return {
        "is_special": monthly or is_milestone or anniversary,
        "is_monthly": monthly,
        "is_milestone": is_milestone,
        "is_anniversary": anniversary,
        "days": days_together
    }

def get_random_quote():
    """Return a random love quote"""
    # Use the date as seed for consistency throughout the day
    today = datetime.now().date()
    random.seed(today.toordinal())
    quote = random.choice(QUOTES)
    random.seed()  # Reset the seed
    return quote

def get_progress_to_anniversary():
    """Calculate progress towards anniversary in percentage"""
    days_together = get_days_together()
    
    # If already past first anniversary, calculate progress to next anniversary
    if days_together > 365:
        completed_years = days_together // 365
        days_in_current_year = days_together % 365
        progress = (days_in_current_year / 365) * 100
    else:
        progress = (days_together / 365) * 100
        
    return min(progress, 100)

def get_upcoming_milestone():
    """Get the next upcoming milestone"""
    days_together = get_days_together()
    
    # List all milestone days
    milestones = sorted(SPECIAL_MILESTONES.keys())
    
    # Find the next milestone
    for milestone in milestones:
        if days_together < milestone:
            days_left = milestone - days_together
            return {
                "milestone": milestone,
                "title": SPECIAL_MILESTONES[milestone]["title"],
                "days_left": days_left
            }
    
    # If we've passed all milestones in the first year
    if days_together < 365:
        days_left = 365 - days_together
        return {
            "milestone": 365,
            "title": "Our First Anniversary!",
            "days_left": days_left
        }
    else:
        # Calculate days until next anniversary
        completed_years = days_together // 365
        days_in_current_year = days_together % 365
        days_left = 365 - days_in_current_year
        return {
            "milestone": (completed_years + 1) * 365,
            "title": f"Our {completed_years + 1}{'st' if completed_years == 0 else 'nd' if completed_years == 1 else 'rd' if completed_years == 2 else 'th'} Anniversary!",
            "days_left": days_left
        }

# =============================================
# HTML/JS COMPONENTS
# =============================================

def clock_component():
    """Create a real-time updating clock component"""
    clock_html = """
    <div class="clock" id="live-clock">00:00:00</div>
    <script>
        function updateClock() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            document.getElementById('live-clock').innerHTML = `${hours}:${minutes}:${seconds}`;
            setTimeout(updateClock, 1000);
        }
        updateClock();
    </script>
    """
    return components.html(clock_html, height=60)

def floating_hearts_animation():
    """Create floating hearts background animation"""
    hearts_js = """
    <div id="floating-hearts-container"></div>
    <script>
        function createFloatingHeart() {
            const heart = document.createElement('div');
            heart.className = 'floating-heart';
            heart.innerHTML = ['❤️', '💖', '💕', '💗', '💓'][Math.floor(Math.random() * 5)];
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.top = Math.random() * 100 + 'vh';
            heart.style.fontSize = Math.random() * 20 + 10 + 'px';
            heart.style.opacity = Math.random() * 0.7 + 0.3;
            
            // Animation properties
            const duration = Math.random() * 10 + 10; // 10-20 seconds
            heart.style.animationDuration = duration + 's';
            
            document.getElementById('floating-hearts-container').appendChild(heart);
            
            // Remove heart after animation completes
            setTimeout(() => {
                heart.remove();
            }, duration * 1000);
        }
        
        // Create initial hearts
        for(let i = 0; i < 10; i++) {
            createFloatingHeart();
        }
        
        // Add new hearts periodically
        setInterval(createFloatingHeart, 3000);
    </script>
    """
    return components.html(hearts_js, height=0)

def create_confetti_effect():
    """Create confetti effect animation"""
    confetti_js = """
    <div id="confetti-container"></div>
    <script>
        function createConfetti() {
            const confettiCount = 100;
            const container = document.getElementById('confetti-container');
            
            for (let i = 0; i < confettiCount; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    
                    // Random properties
                    const size = Math.random() * 10 + 5;
                    const left = Math.random() * 100;
                    const duration = Math.random() * 3 + 2;
                    const hue = Math.random() * 360;
                    
                    // Apply styles
                    confetti.style.width = `${size}px`;
                    confetti.style.height = `${size}px`;
                    confetti.style.left = `${left}vw`;
                    confetti.style.top = '-10px';
                    confetti.style.backgroundColor = `hsl(${hue}, 100%, 60%)`;
                    confetti.style.animationDuration = `${duration}s`;
                    
                    container.appendChild(confetti);
                    
                    // Remove after animation
                    setTimeout(() => {
                        confetti.remove();
                    }, duration * 1000);
                }, i * 50);
            }
        }
    </script>
    """
    return components.html(confetti_js, height=0)

def trigger_confetti():
    """Trigger the confetti animation"""
    trigger_js = """
    <script>
        createConfetti();
    </script>
    """
    components.html(trigger_js, height=0)

def create_pulse_animation(element_id):
    """Create a pulse animation for a specific element"""
    pulse_js = f"""
    <script>
        document.getElementById('{element_id}').classList.add('pulse');
    </script>
    """
    return components.html(pulse_js, height=0)

def typewriter_effect(text, element_id):
    """Create typewriter effect for text"""
    typewriter_html = f"""
    <div id="{element_id}" class="typewriter"></div>
    <script>
        const text = `{text}`;
        let i = 0;
        const speed = 50; // typing speed
        
        function typeWriter() {{
            if (i < text.length) {{
                document.getElementById("{element_id}").innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }}
        }}
        
        typeWriter();
    </script>
    """
    return components.html(typewriter_html, height=30)

# =============================================
# UI COMPONENTS
# =============================================

def render_header():
    """Render the app header"""
    st.markdown("<h1>💖 Our Love Journey 💖</h1>", unsafe_allow_html=True)
    
    # Create columns for counter and clock
    col1, col2 = st.columns([3, 1])
    
    with col1:
        days = get_days_together()
        st.markdown(
            f"""
            <div class="love-counter" id="love-counter">
                💘 We've been together for <span class="glow-text">{days} days</span> of love 💘
            </div>
            """, 
            unsafe_allow_html=True
        )
        create_pulse_animation("love-counter")
        
    with col2:
        clock_component()

def render_milestone_timeline():
    """Render the relationship milestones timeline"""
    st.markdown("<h2>🚩 Our Journey Timeline</h2>", unsafe_allow_html=True)
    
    today = datetime.now().date()
    days_together = get_days_together()
    
    # Display each milestone
    for milestone in RELATIONSHIP_MILESTONES:
        milestone_date = datetime.strptime(milestone["date"], "%B %d, %Y").date()
        passed = milestone_date <= today
        
        # Calculate days until or days since
        days_diff = abs((today - milestone_date).days)
        time_text = f"{days_diff} days ago" if passed else f"in {days_diff} days"
        
        # Style based on whether milestone has passed
        status_color = "#28a745" if passed else "#6c757d"
        milestone_style = f"opacity: {1 if passed else 0.7};"
        
        # Create milestone card
        st.markdown(
            f"""
            <div class="milestone" style="{milestone_style}">
                <div class="milestone-date">{milestone["date"]} <span style="color: {status_color};">({time_text})</span></div>
                <div class="milestone-title">{milestone["emoji"]} {milestone["title"]}</div>
                <div class="milestone-description">{milestone["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
def render_progress_bar():
    """Render the love journey progress bar"""
    st.markdown("<h2>❤️ Our Journey Progress</h2>", unsafe_allow_html=True)
    
    # Calculate progress to anniversary
    progress = get_progress_to_anniversary()
    upcoming = get_upcoming_milestone()
    
    # Display progress bar
    st.markdown(
        f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;">
                {round(progress)}%
            </div>
        </div>
        <p style="text-align: center; margin-top: 10px;">
            {upcoming["days_left"]} days until {upcoming["title"]}
        </p>
        """,
        unsafe_allow_html=True
    )

def render_love_quote():
    """Render the daily love quote"""
    st.markdown("<h2>💌 Today's Love Quote</h2>", unsafe_allow_html=True)
    
    # Get today's random quote
    quote = get_random_quote()
    
    # Display the quote in a styled container
    st.markdown(
        f"""
        <div class="quote-container">
            {quote}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_surprise_button():
    """Render the 'Surprise Me' button"""
    st.markdown("<h2>🎁 Feeling Lucky?</h2>", unsafe_allow_html=True)
    
    surprise_clicked = st.button("💘 Surprise Me!", key="surprise_button")
    
    if surprise_clicked or st.session_state.get("show_surprise", False):
        st.session_state.show_surprise = True
        
        # Get a random surprise message
        random_message = random.choice(SURPRISE_MESSAGES)
        
        # Display the surprise with animation
        st.markdown(
            f"""
            <div class="surprise-message">
                {random_message}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Check if it's the first time clicking the button in this session
        if not st.session_state.get("surprise_confetti_shown", False):
            st.session_state.surprise_confetti_shown = True
            trigger_confetti()

def render_special_celebration():
    """Render special celebration content for anniversaries and milestones"""
    special_date = is_special_date()
    
    if special_date["is_special"]:
        st.markdown("<h2>✨ Special Day Alert! ✨</h2>", unsafe_allow_html=True)
        
        # Different content based on the type of special date
        if special_date["is_anniversary"]:
            years = special_date["days"] // 365
            st.markdown(
                f"""
                <div class="celebration">
                    <h2>🎂 Happy {years}{'st' if years == 1 else 'nd' if years == 2 else 'rd' if years == 3 else 'th'} Anniversary!</h2>
                    <p>Today marks {years} {'year' if years == 1 else 'years'} of our beautiful journey together. Every moment with you has been a blessing.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            trigger_confetti()
            
        elif special_date["is_monthly"]:
            months = (special_date["days"] // 30) + 1
            st.markdown(
                f"""
                <div class="celebration" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
                    <h2>🌙 Happy {months} {'Month' if months == 1 else 'Months'} Together!</h2>
                    <p>Another month of beautiful memories with you. Here's to many more!</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        elif special_date["is_milestone"]:
            milestone_data = SPECIAL_MILESTONES[special_date["days"]]
            st.markdown(
                f"""
                <div class="celebration" style="background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);">
                    <h2>🏆 {milestone_data['title']}</h2>
                    <p>{milestone_data['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            trigger_confetti()

def create_secret_button():
    """Create a hidden button for revealing a secret message"""
    secret_html = f"""
    <div class="secret-button" id="secret-button">❤</div>
    <script>
        // Function to check for key press
        document.addEventListener('keydown', function(event) {{
            if (event.key === '{SECRET_KEY}') {{
                document.getElementById('secret-message-container').style.display = 'block';
                document.getElementById('secret-message-container').classList.add('fade-in');
            }}
        }});
        
        // Function for button click
        document.getElementById('secret-button').addEventListener('click', function() {{
            document.getElementById('secret-message-container').style.display = 'block';
            document.getElementById('secret-message-container').classList.add('fade-in');
        }});
    </script>
    
    <div id="secret-message-container" style="display: none;">
        <div class="secret-message">
            {SECRET_MESSAGE}
        </div>
    </div>
    """
    return components.html(secret_html, height=0)

def render_heartbeat_graph():
    """Render a heart-beat like graph for our love intensity"""
    st.markdown("<h2>💓 Our Love Heartbeat</h2>", unsafe_allow_html=True)
    
    # Generate data for the heartbeat graph
    days = get_days_together()
    data_range = min(days + 1, 100)  # Show at most 100 days
    
    # Calculate heart beat data with periodic peaks representing special moments
    dates = []
    heartbeats = []
    
    for i in range(data_range):
        date = (LOVE_START_DATE + timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
        
        # Base heartbeat value
        base = 70
        
        # Add randomness
        random_factor = random.uniform(-5, 5)
        
        # Add peaks for special days
        if i % 7 == 0:  # Weekly peaks
            peak_value = random.uniform(10, 20)
        elif i % 30 == 0:  # Monthly peaks
            peak_value = random.uniform(20, 30)
        else:
            peak_value = 0
            
        heartbeat = base + random_factor + peak_value
        heartbeats.append(heartbeat)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'date': dates,
        'heartbeat': heartbeats
    })
    
    # Plot the heartbeat graph using Altair
    chart = alt.Chart(df).mark_line(color='#ff66b2', strokeWidth=3).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('heartbeat:Q', title='Love Intensity', scale=alt.Scale(domain=[60, 110]))
    ).properties(
        height=300
    )
    
    # Add points for peaks
    points = alt.Chart(df).mark_circle(color='#ff66b2', size=100).encode(
        x='date:T',
        y='heartbeat:Q',
        size=alt.condition(
            alt.datum.heartbeat > 85,
            alt.value(100),
            alt.value(30)
        ),
        opacity=alt.condition(
            alt.datum.heartbeat > 85,
            alt.value(1),
            alt.value(0.5)
        ),
        tooltip=['date', 'heartbeat']
    )
    
    # Display the chart
    st.altair_chart(chart + points, use_container_width=True)

def render_love_memory_journal():
    """Render a section for love memories"""
    st.markdown("<h2>📔 Our Memory Journal</h2>", unsafe_allow_html=True)
    
    # Create columns
    col1, col2 = st.columns(2)
    
    with col1:
        unique_suffix = str(uuid.uuid4())[:8]
        # Add a new memory form
        st.markdown("<h3>Add a New Memory</h3>", unsafe_allow_html=True)
        memory_date = st.date_input("When did this happen?", datetime.now(), key=f"memory_date_input_{unique_suffix}")
        memory_title = st.text_input("Title your memory", key=f"memory_title_input_{unique_suffix}")
        memory_description = st.text_area("Describe this beautiful moment", key=f"memory_desc_input_{unique_suffix}")
        
        if st.button("Save This Memory"):
            # Create a unique key for this memory
            memory_key = f"memory_{int(time.time())}"
            
            # Save memory to session state
            if "memories" not in st.session_state:
                st.session_state.memories = {}
                
            st.session_state.memories[memory_key] = {
                "date": memory_date.strftime("%Y-%m-%d"),
                "title": memory_title,
                "description": memory_description
            }
            
            st.success("Memory saved! 💖")
            
    with col2:
        # Display saved memories
        st.markdown("<h3>Our Beautiful Moments</h3>", unsafe_allow_html=True)
        
        # Check if there are any saved memories
        if "memories" in st.session_state and st.session_state.memories:
            # Sort memories by date (newest first)
            sorted_memories = sorted(
                st.session_state.memories.items(),
                key=lambda x: x[1]["date"],
                reverse=True
            )
            
            # Display each memory
            for memory_key, memory in sorted_memories:
                st.markdown(
                    f"""
                    <div class="card">
                        <small>{memory["date"]}</small>
                        <h4>{memory["title"]}</h4>
                        <p>{memory["description"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Add delete button
                if st.button("Delete", key=f"delete_{memory_key}"):
                    del st.session_state.memories[memory_key]
                    st.rerun()
        else:
            st.info("No memories saved yet. Create your first memory! 💭")

def render_photo_gallery():
    """Render a photo gallery of memorable moments"""
    st.markdown("<h2>📸 Our Photo Gallery</h2>", unsafe_allow_html=True)
    
    # Initialize photo gallery in session state if not exists
    if "photo_gallery" not in st.session_state:
        st.session_state.photo_gallery = []
    
    # Create columns for the upload form and display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h3>Add a New Photo</h3>", unsafe_allow_html=True)
        photo_date = st.date_input("Date", datetime.now(), key="photo_date")
        photo_caption = st.text_input("Caption", key="photo_caption_key")
        photo_file = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
        
        if st.button("Add to Gallery") and photo_file:
            # In a real app, you'd save the file
            # For demo, we'll just store metadata and create a placeholder
            new_photo = {
                "caption": photo_caption,
                "date": photo_date.strftime("%Y-%m-%d"),
                "file_name": photo_file.name
            }
            st.session_state.photo_gallery.append(new_photo)
            st.success("Photo added to gallery! 💖")
    
    with col2:
        st.markdown("<h3>Our Memories</h3>", unsafe_allow_html=True)
        
        if not st.session_state.photo_gallery:
            st.info("Add your first photo to start your gallery! 📸")
        else:
            # Display photos in a grid (simulated)
            gallery_cols = st.columns(3)
            
            for i, photo in enumerate(st.session_state.photo_gallery):
                with gallery_cols[i % 3]:
                    st.markdown(
                        f"""
                        <div class="card" style="padding: 10px; text-align: center;">
                            <img src="/api/placeholder/400/300" alt="Placeholder" style="width: 100%; border-radius: 10px;">
                            <p style="margin-top: 10px;">{photo['caption']}</p>
                            <small>{photo['date']}</small>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    if st.button("Remove", key=f"remove_photo_{i}"):
                        st.session_state.photo_gallery.pop(i)
                        st.rerun()
def render_love_story_highlights():
    """Render key moments and highlights of your love story"""
    st.markdown("<h2>💫 Our Love Story Highlights</h2>", unsafe_allow_html=True)
    
    # Define key moments in your story
    highlights = [
        {
            "date": "April 15, 2024",
            "title": "The Beginning",
            "description": "Our first message that started it all.",
            "icon": "💬"
        },
        {
            "date": "April 30, 2024",
            "title": "Deep Conversations",
            "description": "When we stayed up all night just talking about life.",
            "icon": "🌙"
        },
        {
            "date": "May 20, 2024",
            "title": "First Inside Joke",
            "description": "That moment we couldn't stop laughing and created our first inside joke.",
            "icon": "😂"
        },
        {
            "date": "June 10, 2024",
            "title": "Shared Dreams",
            "description": "When we talked about our future and realized how aligned our dreams are.",
            "icon": "✨"
        },
        {
            "date": "July 4, 2024",
            "title": "Overcoming Challenges",
            "description": "That difficult time we handled together and grew stronger.",
            "icon": "💪"
        }
    ]
    
    # Create an accordion for each highlight
    for i, highlight in enumerate(highlights):
        with st.expander(f"{highlight['icon']} {highlight['date']} - {highlight['title']}"):
            st.markdown(
                f"""
                <div style="padding: 10px;">
                    <p>{highlight['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Add a "memory gem" - a small inspirational note related to this moment
            memory_gems = [
                "Some moments are unforgettable.",
                "The little moments matter most.",
                "This changed everything in the best way.",
                "Sometimes magic happens when you least expect it.",
                "The beginning of something beautiful."
            ]
            
            st.markdown(
                f"""
                <div style="background-color: rgba(255,102,178,0.1); padding: 10px; border-radius: 10px; border-left: 3px solid #ff66b2; margin-top: 10px;">
                    <i>💎 Memory Gem: {memory_gems[i % len(memory_gems)]}</i>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_relationship_goals():
    """Render a section for relationship goals"""
    st.markdown("<h2>🎯 Our Relationship Goals</h2>", unsafe_allow_html=True)
    
    # Define preset goals
    preset_goals = [
        {"goal": "Take a weekend trip together", "category": "Adventure", "icon": "🧳"},
        {"goal": "Cook a new recipe together", "category": "Activities", "icon": "🍳"},
        {"goal": "Start a new tradition", "category": "Milestones", "icon": "🎭"},
        {"goal": "Learn something new together", "category": "Growth", "icon": "🌱"},
        {"goal": "Have a picnic under the stars", "category": "Romance", "icon": "🌟"}
    ]
    
    # Create tabs for categories
    st.markdown(
        """
        <div style="background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <p>Set goals together and watch your relationship grow stronger with each accomplishment! ✨</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Initialize session state for goals if not exist
    if "relationship_goals" not in st.session_state:
        st.session_state.relationship_goals = preset_goals.copy()
    
    # Allow adding new goals
    with st.form("add_goal_form"):
        st.subheader("Add a New Goal")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_goal = st.text_input("What's something you want to do together?")
        
        with col2:
            category = st.selectbox(
                "Category",
                ["Romance", "Adventure", "Growth", "Activities", "Milestones"]
            )
        
        icons = {
            "Romance": "❤️",
            "Adventure": "🗺️",
            "Growth": "🌱",
            "Activities": "🎨",
            "Milestones": "🏆"
        }
        
        submitted = st.form_submit_button("Add Goal")
        
        if submitted and new_goal:
            st.session_state.relationship_goals.append({
                "goal": new_goal,
                "category": category,
                "icon": icons.get(category, "✨")
            })
            st.success("Goal added! 🎉")
    
    # Display existing goals
    st.subheader("Our Goals List")
    
    # Use tabs to organize by category
    categories = set(goal["category"] for goal in st.session_state.relationship_goals)
    tabs = st.tabs(list(categories) + ["All"])
    
    # Populate each category tab
    for i, category in enumerate(list(categories)):
        with tabs[i]:
            category_goals = [g for g in st.session_state.relationship_goals if g["category"] == category]
            
            if not category_goals:
                st.write("No goals in this category yet.")
            
            for j, goal in enumerate(category_goals):
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(
                        f"""
                        <div style="padding: 10px; background-color: rgba(255,255,255,0.7); border-radius: 10px; margin-bottom: 10px;">
                            {goal["icon"]} {goal["goal"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col2:
                    if st.button("Done", key=f"done_{category}_{j}"):
                        # Mark as completed (in a real app, you'd move it to a completed list)
                        st.balloons()
                        st.session_state.relationship_goals.remove(goal)
                        st.rerun()
    
    # "All" tab shows all goals
    with tabs[-1]:
        for j, goal in enumerate(st.session_state.relationship_goals):
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 1.5rem;'>{goal['icon']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(
                    f"""
                    <div style="padding: 10px; background-color: rgba(255,255,255,0.7); border-radius: 10px;">
                        <b>{goal["goal"]}</b><br>
                        <small>{goal["category"]}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col3:
                if st.button("Done", key=f"done_all_{j}"):
                    st.balloons()
                    st.session_state.relationship_goals.remove(goal)
                    st.rerun()
def render_future_calendar():
    """Render a calendar of upcoming special dates and plans"""
    st.markdown("<h2>📅 Our Future Plans</h2>", unsafe_allow_html=True)
    
    # Initialize calendar events in session state if not exists
    if "calendar_events" not in st.session_state:
        # Add some example planned events
        st.session_state.calendar_events = [
            {
                "date": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "title": "Movie Night",
                "details": "Watch that new romantic comedy"
            },
            {
                "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "title": "Weekend Getaway",
                "details": "Weekend trip to the mountains"
            }
        ]
    
    # Create columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h3>Add to Our Calendar</h3>", unsafe_allow_html=True)
        
        with st.form("add_event_form"):
            event_date = st.date_input("Date", min_value=datetime.now(), key="unique_key_name")
            event_title = st.text_input("Title")
            event_details = st.text_area("Details")
            
            submit_event = st.form_submit_button("Add to Calendar")
            
            if submit_event and event_title:
                st.session_state.calendar_events.append({
                    "date": event_date.strftime("%Y-%m-%d"),
                    "title": event_title,
                    "details": event_details
                })
                st.success("Event added! Looking forward to it! 🎉")
    
    with col2:
        st.markdown("<h3>Our Upcoming Events</h3>", unsafe_allow_html=True)
        
        # Sort events by date
        sorted_events = sorted(
            st.session_state.calendar_events,
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d")
        )
        
        if not sorted_events:
            st.info("No upcoming events. Let's plan something special!")
        else:
            for i, event in enumerate(sorted_events):
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                days_until = (event_date.date() - datetime.now().date()).days
                
                if days_until < 0:
                    continue  # Skip past events
                
                st.markdown(
                    f"""
                    <div class="card" style="margin-bottom: 15px; border-left: 4px solid #ff66b2;">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <h4>{event["title"]}</h4>
                                <p>{event["date"]} <span style="color: #ff66b2;">({days_until} days from now)</span></p>
                            </div>
                        </div>
                        <p>{event["details"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("Remove", key=f"remove_event_{i}"):
                    st.session_state.calendar_events.pop(i)
                    st.rerun()
def render_anniversary_countdown():
    """Render a countdown to next anniversary or special date"""
    upcoming = get_upcoming_milestone()
    
    st.markdown(f"<h2>🎯 Countdown to {upcoming['title']}</h2>", unsafe_allow_html=True)
    
    # Calculate remaining days, hours, minutes
    days_left = upcoming["days_left"]
    
    # Get hours and minutes until midnight
    now = datetime.now()
    seconds_today = (now.hour * 3600) + (now.minute * 60) + now.second
    seconds_left_today = 86400 - seconds_today
    
    hours_left = seconds_left_today // 3600
    minutes_left = (seconds_left_today % 3600) // 60
    seconds_left = seconds_left_today % 60
    
    # Create columns for the countdown
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="card" style="text-align: center;">
                <h1 style="font-size: 3rem; margin: 0;">{days_left}</h1>
                <p>Days</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="card" style="text-align: center;">
                <h1 style="font-size: 3rem; margin: 0;">{hours_left}</h1>
                <p>Hours</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            f"""
            <div class="card" style="text-align: center;">
                <h1 style="font-size: 3rem; margin: 0;">{minutes_left}</h1>
                <p>Minutes</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f"""
            <div class="card" style="text-align: center;">
                <h1 style="font-size: 3rem; margin: 0;">{seconds_left}</h1>
                <p>Seconds</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Add note about the event
    if days_left <= 7:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px; color: #e83e8c; font-weight: 600;">
                ✨ Coming soon! Get ready for a special celebration! ✨
            </div>
            """,
            unsafe_allow_html=True
        )
def render_love_stats():
    """Render fun stats about our relationship"""
    st.markdown("<h2>📊 Our Love by Numbers</h2>", unsafe_allow_html=True)
    
    # Calculate various stats
    days = get_days_together()
    hours = days * 24
    minutes = hours * 60
    seconds = minutes * 60
    
    # Create columns for stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h3>Time Together</h3>
                <ul>
                    <li>{days} days</li>
                    <li>{hours:,} hours</li>
                    <li>{minutes:,} minutes</li>
                    <li>{seconds:,} seconds</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        # Calculate fun stats
        laughs = int(days * random.uniform(5, 15))
        smiles = int(days * random.uniform(20, 50))
        heart_beats = int(minutes * 70)  # Assuming 70 beats per minute
        
        st.markdown(
            f"""
            <div class="card">
                <h3>Fun Facts</h3>
                <ul>
                    <li>~ {laughs:,} laughs shared</li>
                    <li>~ {smiles:,} smiles exchanged</li>
                    <li>~ {heart_beats:,} heartbeats while thinking of you</li>
                    <li>~ ∞ moments of happiness</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

def set_animated_background():
    st.markdown(
        """
        <style>
        /* Full page animated gradient background */
        body {
            background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            transition: background 0.5s ease-in-out;
        }

        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Add soft glowing effect to headings */
        h1, h2, h3 {
            text-shadow: 0 0 15px #ffb6c1, 0 0 30px #ffb6c1;
        }

        /* Optional: Add blur-glow to cards or sections */
        .card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 8px 32px 0 rgba(255, 182, 193, 0.37);
        }

        </style>
        """,
        unsafe_allow_html=True
    )
def render_personalized_compliments():
    """Generates personalized compliments when button is clicked"""
    st.markdown("<h3 style='text-align: center; color: #ff4b5c;'>✨ Words From My Heart ✨</h3>", unsafe_allow_html=True)
    
    # List of personalized compliments - add as many as you like!
    compliments = [
        "Your smile lights up my entire world, even on the darkest days.",
        "The way you laugh makes my heart skip a beat every single time.",
        "Your strength and resilience inspire me to be a better person.",
        "The touch of your hand still gives me butterflies after all this time.",
        "Your kindness to others shows the beautiful soul you truly are.",
        "The way you look at me makes me feel like the luckiest person alive.",
        "Your intelligence and wit amaze me more each day.",
        "I fall in love with your beautiful eyes all over again every morning.",
        "The passion you bring to everything you do is absolutely captivating.",
        "Your creativity and imagination bring so much color to our life together.",
        "The way you care for our family shows the depth of your amazing heart.",
        "Your patience and understanding make you an incredible partner.",
        "The sound of your voice is still my favorite melody after all these years.",
        "Your thoughtfulness in the little things makes every day special.",
        "The comfort I feel in your embrace is the safest place I know.",
        "Your intuition and wisdom guide us through life's challenges.",
        "The way you pursue your dreams makes me endlessly proud.",
        "Your natural beauty takes my breath away, inside and out.",
        "The gentle way you love me heals parts of me I didn't know were broken.",
        "Your sense of adventure keeps our life exciting and full of wonder."
    ]
    
    # Button to generate a random compliment
    if st.button("💖 What I Love About You Today 💖", key="compliment_button"):
        import random
        
        # Create a colorful container for the compliment
        st.markdown("""
        <style>
        .compliment-box {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            from {
                box-shadow: 0 0 10px -10px #ff9a9e;
            }
            to {
                box-shadow: 0 0 20px 5px #ff9a9e;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Select a random compliment
        chosen_compliment = random.choice(compliments)
        
        # Display the compliment with animation
        st.markdown(f"""
        <div class="compliment-box">
            <p style="font-size: 1.2rem; color: #7d2a42; font-style: italic;">"{chosen_compliment}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add subtle heart animation
        st.markdown("""
        <style>
        .heart {
            font-size: 20px;
            color: #ff4b5c;
            display: inline-block;
            animation: beat .5s infinite alternate;
        }
        @keyframes beat {
            to { transform: scale(1.2); }
        }
        </style>
        <div style="text-align: center;">
            <span class="heart">❤️</span>
        </div>
        """, unsafe_allow_html=True)

def render_interactive_love_wordcloud():
    """Render a beautiful interactive word cloud for your romantic app."""

    # 💬 Predefined romantic words with frequency
    words_dict = {
        "Beautiful": 120,
        "My Queen": 110,
        "Hug": 90,
        "Smile": 85,
        "Forever": 100,
        "Wifey": 130,
        "Laughter": 70,
        "Cute": 95,
        "Adore": 80,
        "Together": 105,
        "Sweetheart": 75,
        "Sunshine": 115,
        "Lovely": 90,
        "Cherish": 65,
        "Kiss": 125,
        "Date": 55,
        "Warmth": 60,
        "Memories": 70,
        "Angel": 95,
        "My Love": 140
    }

    # 📍 Section title
    st.markdown("<h2 style='text-align: center; color: #e91e63;'>💖 Our Love Word Cloud 💖</h2>", unsafe_allow_html=True)

    # 🎛️ Sliders for customization
    with st.expander("🎨 Customize Your Word Cloud", expanded=True):
        max_words = st.slider("Max Words", min_value=5, max_value=30, value=20)
        font_scale = st.slider("Font Scale", min_value=1, max_value=5, value=2)

    # 🎨 Color function for romantic feel
    def love_colors(word, font_size, position, orientation, font_path, random_state):
        return f"hsl({random.randint(0, 360)}, 80%, 65%)"

    # 🌈 Create the WordCloud
    wc = WordCloud(
        width=800,
        height=400,
        max_words=max_words,
        relative_scaling=0.5,
        normalize_plurals=True,
        color_func=love_colors,
        prefer_horizontal=0.95,
        scale=font_scale,
        background_color='white'
    ).generate_from_frequencies(words_dict)

    # 🖼️ Display in Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)


def wish_upon_a_star():
    """
    Create an interactive night sky where Faryal can make wishes
    that get saved and can be granted over time.
    """
    st.markdown("## ✨ Wish Upon a Star ✨")
    st.markdown("### Make a wish, my love, and I'll make it come true...")
    
    # File to store wishes
    WISHES_FILE = "wishes.json"
    
    # Load existing wishes
    def load_wishes():
        if os.path.exists(WISHES_FILE):
            try:
                with open(WISHES_FILE, "r") as f:
                    return json.load(f)
            except:
                return {"wishes": []}
        else:
            return {"wishes": []}
    
    # Save wishes
    def save_wish(wish_text):
        wishes_data = load_wishes()
        new_wish = {
            "id": len(wishes_data["wishes"]) + 1,
            "text": wish_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "granted": False,
            "grant_date": None
        }
        wishes_data["wishes"].append(new_wish)
        
        with open(WISHES_FILE, "w") as f:
            json.dump(wishes_data, f, indent=4)
    
    # Grant a wish
    def grant_wish(wish_id):
        wishes_data = load_wishes()
        for wish in wishes_data["wishes"]:
            if wish["id"] == wish_id:
                wish["granted"] = True
                wish["grant_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        with open(WISHES_FILE, "w") as f:
            json.dump(wishes_data, f, indent=4)
    
    # Generate interactive night sky
    def create_night_sky(num_stars=100, highlighted_stars=None):
        if highlighted_stars is None:
            highlighted_stars = []
            
        # Set up the figure
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#051033')
        ax.set_facecolor('#051033')  # Dark blue night sky
        
        # Generate random star positions but make them consistent
        # Use a fixed seed to make star positions consistent between renders
        np.random.seed(42)  
        stars_x = np.random.uniform(0, 10, num_stars)
        stars_y = np.random.uniform(0, 6, num_stars)
        stars_size = np.random.uniform(5, 25, num_stars)
        
        # Draw stars
        star_colors = ['#FFFFFF', '#FFFFEE', '#EEEEFF', '#FFEEEE']
        colors = [random.choice(star_colors) for _ in range(num_stars)]
        
        for i in range(num_stars):
            if i in highlighted_stars:
                # Highlighted star (the one being wished upon)
                star = Circle((stars_x[i], stars_y[i]), stars_size[i]/100, 
                           color='#FFD700', alpha=0.9)  # Gold color
                # Add a subtle glow effect
                glow = Circle((stars_x[i], stars_y[i]), stars_size[i]/50, 
                           color='#FFD700', alpha=0.3)
                ax.add_patch(glow)
            else:
                star = Circle((stars_x[i], stars_y[i]), stars_size[i]/200, 
                           color=colors[i], alpha=0.8)
            ax.add_patch(star)
            
            # If this is a wished star, add a small label with the wish number
            if i in highlighted_stars:
                wish_index = highlighted_stars.index(i)
                ax.text(stars_x[i], stars_y[i] + 0.2, f"#{wish_index+1}", 
                        color='#FFD700', fontsize=8, ha='center')
        
        # Remove axes and set limits
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        return fig
    
    # Create tabs for wishing and viewing wishes
    tab1, tab2 = st.tabs(["✨ Make a Wish", "📜 View Wishes"])
    
    with tab1:
        wishes_data = load_wishes()
        # Get star indices for existing wishes
        highlighted_stars = []
        
        # Assign a consistent star index to each wish
        for i, wish in enumerate(wishes_data["wishes"]):
            # Use the wish ID as a seed to get a consistent star index
            random.seed(wish["id"])
            highlighted_stars.append(random.randint(0, 49))
        
        # Display the night sky with all wishes highlighted
        st.markdown("### Your wishes among the stars ✨")
        fig = create_night_sky(num_stars=50, highlighted_stars=highlighted_stars)
        st.pyplot(fig)
        
        # Add text input for new wish
        wish_text = st.text_area("What's your wish, Faryal?", 
                              placeholder="Type your wish here...",
                              key="wish_input")
        
        # Add button to submit wish
        if st.button("✨ Make My Wish", key="submit_wish"):
            if wish_text:
                # Save the wish
                save_wish(wish_text)
                st.success("Your wish has been sent to the stars! ✨")
                st.balloons()  # Show balloons for a fun effect
                st.rerun()  # Rerun to update the sky with the new wish
            else:
                st.warning("Please enter a wish first.")
    
    with tab2:
        st.markdown("### Your Wishes Among the Stars")
        
        # Load and display all wishes
        wishes_data = load_wishes()
        
        if not wishes_data["wishes"]:
            st.info("No wishes have been made yet. Go to the 'Make a Wish' tab to create your first wish!")
        else:
            # Create two columns - one for pending wishes, one for granted wishes
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ⏳ Waiting to Come True")
                
                pending_wishes = [wish for wish in wishes_data["wishes"] if not wish["granted"]]
                if not pending_wishes:
                    st.info("All wishes have been granted! 🌟")
                
                for wish in pending_wishes:
                    with st.container():
                        st.markdown(f"""
                        <div style='background-color:rgba(0,0,50,0.3); padding:10px; border-radius:10px; margin-bottom:10px;'>
                            <p style='font-style:italic;'>"{wish['text']}"</p>
                            <p style='font-size:0.8em; color:#AAAAAA;'>Made on {wish['date']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Only show the grant button if you're the one viewing
                        if st.button(f"✨ Grant This Wish", key=f"grant_{wish['id']}"):
                            grant_wish(wish['id'])
                            st.success("Wish granted! ✨")
                            st.experimental_rerun()
            
            with col2:
                st.markdown("#### 🌟 Wishes Come True")
                
                granted_wishes = [wish for wish in wishes_data["wishes"] if wish["granted"]]
                if not granted_wishes:
                    st.info("No wishes have been granted yet.")
                
                for wish in granted_wishes:
                    with st.container():
                        st.markdown(f"""
                        <div style='background-color:rgba(50,50,0,0.3); padding:10px; border-radius:10px; margin-bottom:10px;'>
                            <p style='font-style:italic;'>"{wish['text']}"</p>
                            <p style='font-size:0.8em; color:#AAAAAA;'>Made on {wish['date']}</p>
                            <p style='font-size:0.8em; color:gold;'>✨ Granted on {wish['grant_date']} ✨</p>
                        </div>
                        """, unsafe_allow_html=True)

def render_love_language_visualization():
    """
    Create a beautiful visualization showing how you and your partner
    express love to each other based on the five love languages.
    """
    st.markdown("## 💖 Our Love Languages 💖")
    st.markdown("### How we express our love to each other")
    
    # Create a container for the visualization
    viz_container = st.container()
        
    # The five love languages
    love_languages = [
        "Words of Affirmation", 
        "Quality Time", 
        "Receiving Gifts",
        "Acts of Service", 
        "Physical Touch"
    ]
    
    # Initialize default values from session state or with defaults
    if 'your_scores' not in st.session_state:
        st.session_state.your_scores = [7, 8, 5, 9, 10]  # Default values for you
    
    if 'faryal_scores' not in st.session_state:
        st.session_state.faryal_scores = [9, 8, 7, 6, 10]  # Default values for Faryal
    
    # Create two tabs - one for visualization, one for settings
    tab1, tab2 = st.tabs(["💖 Visualization", "⚙️ Settings"])
    
    with tab1:
        with viz_container:
            display_love_language_chart(love_languages, 
                                        st.session_state.your_scores, 
                                        st.session_state.faryal_scores)
    
    with tab2:
        st.markdown("### Adjust Our Love Language Scores")
        st.markdown("Rate each love language on a scale of 1-10 based on how much it matters to each of you.")
        
        # Create two columns for you and your partner
        col1, col2 = st.columns(2)
        
        # Update sliders
        new_your_scores = []
        new_faryal_scores = []
        
        with col1:
            st.markdown("#### Your Love Languages")
            for i, language in enumerate(love_languages):
                new_value = st.slider(
                    f"You - {language}", 
                    1, 10, 
                    st.session_state.your_scores[i],
                    key=f"you_{language}"
                )
                new_your_scores.append(new_value)
        
        with col2:
            st.markdown("#### Faryal's Love Languages")
            for i, language in enumerate(love_languages):
                new_value = st.slider(
                    f"Faryal - {language}", 
                    1, 10, 
                    st.session_state.faryal_scores[i],
                    key=f"faryal_{language}"
                )
                new_faryal_scores.append(new_value)
        
        # Button to update the visualization
        if st.button("Update Our Love Languages"):
            st.session_state.your_scores = new_your_scores
            st.session_state.faryal_scores = new_faryal_scores
            st.success("Love languages updated! ❤️")
            
            # Display a sweet message based on the top love languages
            your_top = love_languages[np.argmax(new_your_scores)]
            faryal_top = love_languages[np.argmax(new_faryal_scores)]
            
            st.markdown(f"""
            ### 💖 Love Insight
            
            You express love the most through **{your_top}**,  
            while Faryal feels most loved through **{faryal_top}**.
            
            {"That's a beautiful match!" if your_top == faryal_top else "Understanding each other's love languages helps us connect more deeply! ❤️"}
            """)

def display_love_language_chart(categories, values1, values2):
    """
    Create a beautiful radar chart to visualize love languages.
    
    Args:
        categories: List of love language categories
        values1: Your scores (list of values)
        values2: Faryal's scores (list of values)
    """
    # Number of variables
    N = len(categories)
    
    # Create a list with the angles for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Create values lists for the plot
    values1 = values1 + values1[:1]  # Close the loop
    values2 = values2 + values2[:1]  # Close the loop
    
    # Create a polar plot with plotly
    fig = go.Figure()
    
    # Add your data
    fig.add_trace(go.Scatterpolar(
        r=values1,
        theta=categories + [categories[0]],  # Close the loop
        fill='toself',
        name='You',
        line=dict(color='rgba(65, 105, 225, 0.8)', width=2),
        fillcolor='rgba(65, 105, 225, 0.3)'
    ))
    
    # Add Faryal's data
    fig.add_trace(go.Scatterpolar(
        r=values2,
        theta=categories + [categories[0]],  # Close the loop
        fill='toself',
        name='Faryal',
        line=dict(color='rgba(219, 112, 147, 0.8)', width=2),
        fillcolor='rgba(219, 112, 147, 0.3)'
    ))
    
    # Customize layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=False,
                ticks=''
            ),
            angularaxis=dict(
                rotation=90,  # start from the top
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=60, t=40, b=40),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Add some insights below the chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Your Top Love Languages")
        # Get the top 2 love languages for you
        top_yours = sorted(zip(values1[:-1], categories), reverse=True)[:2]
        for score, language in top_yours:
            st.markdown(f"- **{language}**: {score}/10")
    
    with col2:
        st.markdown("#### Faryal's Top Love Languages")
        # Get the top 2 love languages for Faryal
        top_faryal = sorted(zip(values2[:-1], categories), reverse=True)[:2]
        for score, language in top_faryal:
            st.markdown(f"- **{language}**: {score}/10")
            
    # Check for matches (where both have high scores)
    matches = []
    for i, cat in enumerate(categories):
        if values1[i] >= 8 and values2[i] >= 8:
            matches.append(cat)
    
    if matches:
        st.markdown("#### 💖 Your Love Language Matches")
        st.markdown("You both value these love languages highly:")
        for match in matches:
            st.markdown(f"- **{match}** ✨")
        
        st.markdown("""
        <div style='background-color:rgba(219, 112, 147, 0.1); padding:10px; border-radius:10px; margin-top:20px;'>
            <p style='text-align:center;'>Nurturing your shared love languages creates deeper connection! ❤️</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add tips based on differing love languages
    differences = []
    for i, cat in enumerate(categories):
        diff = abs(values1[i] - values2[i])
        if diff >= 3:  # If there's a significant difference
            differences.append((cat, values1[i], values2[i]))
    
    if differences:
        st.markdown("#### 💭 Love Language Tips")
        for lang, your_score, faryal_score in differences:
            if your_score > faryal_score:
                st.markdown(f"- Faryal may not value **{lang}** as much as you do. Consider expressing love in other ways too.")
            else:
                st.markdown(f"- Consider expressing more **{lang}** as Faryal values this highly.")
# =============================================
# MAIN APP
# =============================================

def main():
    """Main application function"""
    render_daily_rose_bloom()
    # Load CSS
    load_css()

    set_animated_background()

    # Apply theme customization
    render_theme_selector()
    
    # Create floating hearts animation
    floating_hearts_animation()
    
    # Create confetti effect (will be triggered on special events)
    create_confetti_effect()
    
    # Add secret message functionality
    create_secret_button()
    
    # Render header section
    render_header()
    
    # Check for special dates and show celebration if needed
    render_special_celebration()
    
    # Create main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Love journey progress bar
        render_progress_bar()
        
        # Love quote of the day
        render_love_quote()
        
        st.markdown(
        "<h2 style='text-align: center; color: #ff4b5c;'>I Love You ❤️</h2>",
        unsafe_allow_html=True
        )
    
        # Surprise button feature
        render_surprise_button()
        
        # Love heartbeat graph
        render_heartbeat_graph()

        render_love_story_highlights()  # New function you'd define
        # or
        render_relationship_goals()
        # Add this in main() after render_relationship_goals() or in another appropriate place
        render_future_calendar()
        
    with col2:
        # Milestone timeline
        render_milestone_timeline()
        
        # Anniversary countdown
        render_anniversary_countdown()
        
        # Love stats
        render_love_stats()

    # Add Love Language Visualization here (full width)
    render_love_language_visualization()
    
    # Memory journal section (full width)
    render_love_memory_journal()
    # Memory journal section (full width)
    render_love_memory_journal()
    
    # Add this in the main() function after render_love_memory_journal()
    render_photo_gallery()
    reasons_i_love_you()
    render_personalized_compliments()
    render_interactive_love_wordcloud()
    wish_upon_a_star()
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 20px; opacity: 0.7;">
            ❤️ Made with love ❤️
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    # Initialize session state for persistent features
    if "show_surprise" not in st.session_state:
        st.session_state.show_surprise = False
        
    if "surprise_confetti_shown" not in st.session_state:
        st.session_state.surprise_confetti_shown = False
    
    # Run the app
    main()
