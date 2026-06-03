import streamlit as st
from auth import *
import random
import re
import time
import os
from main import run

st.set_page_config(
    page_title="Kids AI World 🌈",
    layout="wide",
    page_icon="🌈",
    initial_sidebar_state="expanded",
)

init_db()

# ══════════════════════════════════════════════════════════════════════
#  SESSION STATE — init first so theme is available for CSS
# ══════════════════════════════════════════════════════════════════════
_defaults = {
    "user": None, "history": [],
    "story": "", "image": None, "audio": None, "video": None,
    "quiz": [], "game_data": {}, "pieces": [], "current_prompt": "",
    "quiz_q_index": 0, "quiz_answers": {}, "quiz_submitted": False, "quiz_timer": 0.0,
    "game_questions": [], "game_q_index": 0, "game_score": 0,
    "game_total": 0, "game_show_answer": False, "game_user_answer": "",
    "game_started": False, "game_type": "Unscramble", "arrange_items": [],
    "notif": None, "notif_type": "success",
    "theme": "dark",   # "dark" or "light"
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

IS_LIGHT = st.session_state.theme == "light"

# ══════════════════════════════════════════════════════════════════════
#  THEME VARIABLES
# ══════════════════════════════════════════════════════════════════════
if IS_LIGHT:
    # ⚡ Lightning / bright mode
    BG_COLOR        = "#FFFDF0"
    BG_GRAD1        = "rgba(255,215,0,0.18)"
    BG_GRAD2        = "rgba(255,165,0,0.12)"
    BG_GRAD3        = "rgba(255,100,50,0.10)"
    TEXT_PRIMARY    = "#1a1a2e"
    TEXT_SECONDARY  = "#4a4a6a"
    TEXT_MUTED      = "#6b6b8a"
    CARD_BG         = "rgba(255,255,255,0.85)"
    CARD_BORDER     = "rgba(255,193,7,0.4)"
    CARD_SHADOW     = "0 4px 24px rgba(255,165,0,0.15)"
    INPUT_BG        = "rgba(255,255,255,0.95)"
    INPUT_BORDER    = "rgba(255,193,7,0.6)"
    INPUT_TEXT      = "#1a1a2e"
    INPUT_LABEL     = "#2a2a4e"
    SIDEBAR_BG      = "rgba(255,250,220,0.98)"
    SIDEBAR_BORDER  = "rgba(255,193,7,0.3)"
    SIDEBAR_TEXT    = "#2a2a4e"
    BTN_BG          = "rgba(255,193,7,0.15)"
    BTN_BORDER      = "rgba(255,193,7,0.5)"
    BTN_TEXT        = "#1a1a2e"
    BTN_HOVER_BG    = "rgba(255,193,7,0.35)"
    RADIO_TEXT      = "#1a1a2e"
    PROGRESS_FROM   = "#FFD700"
    PROGRESS_TO     = "#FF8C00"
    ORB1_COLOR      = "rgba(255,215,0,0.25)"
    ORB2_COLOR      = "rgba(255,165,0,0.20)"
    ORB3_COLOR      = "rgba(255,100,50,0.18)"
    THEME_ICON      = "⚡"
    THEME_LABEL     = "Lightning Mode ON"
    STAR_OPACITY    = "0.15"
    QCARD_BG        = "rgba(255,250,230,0.95)"
    QCARD_BORDER    = "#FF8C00"
    SCORE_GRAD      = "linear-gradient(135deg, rgba(255,215,0,0.25) 0%, rgba(255,165,0,0.20) 50%, rgba(255,100,50,0.15) 100%)"
    HISTORY_BG      = "rgba(255,250,230,0.85)"
    GAME_WORD_BG    = "rgba(255,215,0,0.15)"
    TOAST_S_BG      = "rgba(74,222,128,0.15)"
    TOAST_E_BG      = "rgba(248,113,113,0.15)"
    TOAST_I_BG      = "rgba(255,193,7,0.15)"
    TOAST_S_BORDER  = "rgba(74,222,128,0.6)"
    TOAST_E_BORDER  = "rgba(248,113,113,0.6)"
    TOAST_I_BORDER  = "rgba(255,193,7,0.6)"
    TOAST_S_TEXT    = "#166534"
    TOAST_E_TEXT    = "#991b1b"
    TOAST_I_TEXT    = "#92400e"
    EXPANDER_BG     = "rgba(255,250,230,0.90)"
    SELECT_TEXT     = "#1a1a2e"
else:
    # 🌙 Dark / space mode
    BG_COLOR        = "#0B0D1A"
    BG_GRAD1        = "rgba(168,85,247,0.15)"
    BG_GRAD2        = "rgba(56,189,248,0.12)"
    BG_GRAD3        = "rgba(255,107,107,0.10)"
    TEXT_PRIMARY    = "#f0f0f0"
    TEXT_SECONDARY  = "#d0d0d0"
    TEXT_MUTED      = "#94a3b8"
    CARD_BG         = "rgba(255,255,255,0.06)"
    CARD_BORDER     = "rgba(255,255,255,0.12)"
    CARD_SHADOW     = "0 4px 24px rgba(0,0,0,0.3)"
    INPUT_BG        = "rgba(255,255,255,0.10)"
    INPUT_BORDER    = "rgba(255,255,255,0.28)"
    INPUT_TEXT      = "#ffffff"
    INPUT_LABEL     = "#e0e0e0"
    SIDEBAR_BG      = "rgba(11,13,26,0.97)"
    SIDEBAR_BORDER  = "rgba(255,255,255,0.07)"
    SIDEBAR_TEXT    = "#c0c0c0"
    BTN_BG          = "rgba(255,255,255,0.08)"
    BTN_BORDER      = "rgba(255,255,255,0.16)"
    BTN_TEXT        = "#f0f0f0"
    BTN_HOVER_BG    = "rgba(255,255,255,0.18)"
    RADIO_TEXT      = "#e0e0e0"
    PROGRESS_FROM   = "#A855F7"
    PROGRESS_TO     = "#38BDF8"
    ORB1_COLOR      = "rgba(168,85,247,0.18)"
    ORB2_COLOR      = "rgba(56,189,248,0.15)"
    ORB3_COLOR      = "rgba(255,107,107,0.13)"
    THEME_ICON      = "🌙"
    THEME_LABEL     = "Dark Mode ON"
    STAR_OPACITY    = "0.5"
    QCARD_BG        = "rgba(255,255,255,0.05)"
    QCARD_BORDER    = "#FFD700"
    SCORE_GRAD      = "linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(168,85,247,0.15) 50%, rgba(78,205,196,0.15) 100%)"
    HISTORY_BG      = "rgba(255,255,255,0.05)"
    GAME_WORD_BG    = "rgba(255,215,0,0.07)"
    TOAST_S_BG      = "rgba(74,222,128,0.18)"
    TOAST_E_BG      = "rgba(248,113,113,0.18)"
    TOAST_I_BG      = "rgba(56,189,248,0.18)"
    TOAST_S_BORDER  = "rgba(74,222,128,0.5)"
    TOAST_E_BORDER  = "rgba(248,113,113,0.5)"
    TOAST_I_BORDER  = "rgba(56,189,248,0.5)"
    TOAST_S_TEXT    = "#86efac"
    TOAST_E_TEXT    = "#fca5a5"
    TOAST_I_TEXT    = "#7dd3fc"
    EXPANDER_BG     = "rgba(255,255,255,0.05)"
    SELECT_TEXT     = "#f0f0f0"

# ══════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════

# Built outside the f-string to avoid Python misreading decimals like 0.04 as syntax
LIGHTNING_CSS = """
.lightning-bolt {
    position: fixed;
    pointer-events: none;
    z-index: 0;
    opacity: 0.08;
    font-size: 120px;
    animation: lightning-flash 3s ease-in-out infinite alternate;
}
.lb-1 { top: 5%;  left: 2%;  animation-delay: 0s; }
.lb-2 { top: 30%; right: 3%; animation-delay: 1s; font-size: 80px; }
.lb-3 { bottom: 10%; left: 5%; animation-delay: 2s; font-size: 100px; }
@keyframes lightning-flash {
    0%   { opacity: 0.04; transform: scale(1)    rotate(-10deg); }
    50%  { opacity: 0.14; transform: scale(1.1)  rotate(-8deg);  }
    100% { opacity: 0.06; transform: scale(0.95) rotate(-12deg); }
}
""" if IS_LIGHT else ""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Boogaloo&family=Quicksand:wght@400;500;600;700&display=swap');

:root {{
    --gold:   #FFD700;
    --coral:  #FF6B6B;
    --mint:   #4ECDC4;
    --violet: #A855F7;
    --sky:    #38BDF8;
    --text-primary:   {TEXT_PRIMARY};
    --text-secondary: {TEXT_SECONDARY};
    --text-muted:     {TEXT_MUTED};
    --card-bg:        {CARD_BG};
    --card-border:    {CARD_BORDER};
    --input-bg:       {INPUT_BG};
    --input-border:   {INPUT_BORDER};
    --input-text:     {INPUT_TEXT};
}}

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Quicksand', sans-serif !important;
    color: {TEXT_PRIMARY} !important;
}}

/* ── App background ── */
.stApp {{
    background-color: {BG_COLOR} !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, {BG_GRAD1} 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, {BG_GRAD2} 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, {BG_GRAD3} 0%, transparent 50%);
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}}

/* Starfield / sparkle overlay */
.stApp::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 40%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 10%, rgba(255,215,0,0.8)   0%, transparent 100%),
        radial-gradient(1px 1px at 70% 30%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 65%, rgba(78,205,196,0.9)  0%, transparent 100%),
        radial-gradient(1px 1px at 40% 75%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 85%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 60% 50%, rgba(255,215,0,0.6)   0%, transparent 100%),
        radial-gradient(1px 1px at 90% 90%, rgba(168,85,247,0.8)  0%, transparent 100%),
        radial-gradient(1px 1px at 5%  55%, rgba(56,189,248,0.7)  0%, transparent 100%);
    animation: twinkle 4s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
    opacity: {STAR_OPACITY};
}}

@keyframes twinkle {{
    0%   {{ opacity: {STAR_OPACITY}; transform: scale(1); }}
    100% {{ opacity: 1;              transform: scale(1.05); }}
}}

/* Floating orbs */
.orb {{ position: fixed; border-radius: 50%; filter: blur(60px); opacity: 0.22;
        pointer-events: none; z-index: 0; animation: drift 12s ease-in-out infinite alternate; }}
.orb-1 {{ width:400px; height:400px; background:{ORB1_COLOR}; top:-100px; left:-100px; animation-delay:0s; }}
.orb-2 {{ width:300px; height:300px; background:{ORB2_COLOR}; bottom:-80px; right:-80px; animation-delay:3s; }}
.orb-3 {{ width:250px; height:250px; background:{ORB3_COLOR}; top:50%; left:60%; animation-delay:6s; }}
@keyframes drift {{
    0%   {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(30px,20px) scale(1.1); }}
}}

/* ── Lightning bolts for light mode ── */
{LIGHTNING_CSS}

/* ── Hero heading ── */
.hero {{
    font-family: 'Boogaloo', cursive !important;
    font-size: 58px;
    text-align: center;
    background: linear-gradient(135deg, #FFD700 0%, #FF6B6B 35%, #A855F7 65%, #38BDF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 10px 0 24px 0;
    line-height: 1.1;
    animation: fadeSlideDown 0.7s ease-out;
    position: relative; z-index: 1;
}}
@keyframes fadeSlideDown {{
    from {{ opacity: 0; transform: translateY(-24px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ── Glassmorphism card ── */
.card {{
    background: {CARD_BG};
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 22px 26px;
    border-radius: 20px;
    border: 1px solid {CARD_BORDER};
    color: {TEXT_PRIMARY};
    margin-bottom: 16px;
    position: relative; z-index: 1;
    box-shadow: {CARD_SHADOW};
    transition: transform 0.2s, box-shadow 0.2s;
}}
.card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,0.2); }}
.card p, .card span, .card b, .card div {{ color: {TEXT_PRIMARY} !important; }}

/* ── Question card ── */
.q-card {{
    background: {QCARD_BG};
    border-left: 5px solid {QCARD_BORDER};
    padding: 20px 24px;
    border-radius: 16px;
    color: {TEXT_PRIMARY} !important;
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 14px;
    position: relative; z-index: 1;
    animation: fadeIn 0.4s ease-out;
    backdrop-filter: blur(8px);
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateX(-16px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}

/* ── Score card ── */
.score-card {{
    background: {SCORE_GRAD};
    border: 1px solid rgba(255,215,0,0.3);
    padding: 32px; border-radius: 24px; text-align: center;
    position: relative; z-index: 1;
    animation: popIn 0.5s cubic-bezier(0.34,1.56,0.64,1);
}}
@keyframes popIn {{
    from {{ opacity: 0; transform: scale(0.7); }}
    to   {{ opacity: 1; transform: scale(1); }}
}}
.score-card h2, .score-card h3, .score-card p, .score-card div {{
    color: {TEXT_PRIMARY} !important;
}}

/* ── Game word display ── */
.game-word {{
    font-family: 'Boogaloo', cursive !important;
    font-size: 52px;
    letter-spacing: 10px;
    text-align: center;
    color: {"#B8860B" if IS_LIGHT else "#FFD700"};
    background: {GAME_WORD_BG};
    padding: 22px; border-radius: 18px;
    border: 2px dashed rgba(255,215,0,0.4);
    margin: 16px 0;
    animation: pulse-glow 2s ease-in-out infinite alternate;
    position: relative; z-index: 1;
}}
@keyframes pulse-glow {{
    from {{ box-shadow: 0 0 12px rgba(255,215,0,0.2); }}
    to   {{ box-shadow: 0 0 28px rgba(255,215,0,0.5); }}
}}

/* ── History item ── */
.history-item {{
    background: {HISTORY_BG};
    border-left: 4px solid var(--mint);
    padding: 13px 18px; border-radius: 12px;
    color: {TEXT_SECONDARY};
    margin-bottom: 10px;
    transition: background 0.2s;
    position: relative; z-index: 1;
    backdrop-filter: blur(8px);
}}
.history-item:hover {{ background: {CARD_BG}; }}
.history-item b {{ color: {TEXT_PRIMARY} !important; }}

/* ── Toast notifications ── */
.toast-success {{
    background: {TOAST_S_BG}; border: 1px solid {TOAST_S_BORDER};
    border-radius: 14px; padding: 14px 20px;
    color: {TOAST_S_TEXT} !important; font-weight: 700; font-size: 16px;
    text-align: center; animation: slideUp 0.4s ease-out;
    position: relative; z-index: 1;
}}
.toast-error {{
    background: {TOAST_E_BG}; border: 1px solid {TOAST_E_BORDER};
    border-radius: 14px; padding: 14px 20px;
    color: {TOAST_E_TEXT} !important; font-weight: 700; font-size: 16px;
    text-align: center; animation: slideUp 0.4s ease-out;
    position: relative; z-index: 1;
}}
.toast-info {{
    background: {TOAST_I_BG}; border: 1px solid {TOAST_I_BORDER};
    border-radius: 14px; padding: 14px 20px;
    color: {TOAST_I_TEXT} !important; font-weight: 700; font-size: 16px;
    text-align: center; animation: slideUp 0.4s ease-out;
    position: relative; z-index: 1;
}}
@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ── Listening panel ── */
.listening-panel {{
    background: linear-gradient(135deg,
        rgba(168,85,247,0.18) 0%, rgba(56,189,248,0.12) 100%);
    border: 1px solid rgba(168,85,247,0.3);
    border-radius: 22px; padding: 24px 28px; text-align: center;
    position: relative; z-index: 1;
}}
.listening-waves {{
    display: flex; justify-content: center; align-items: flex-end;
    gap: 5px; height: 40px; margin: 12px 0;
}}
.listening-bar {{
    width: 6px; border-radius: 3px; background: var(--violet);
    animation: wave-bar 1.2s ease-in-out infinite;
}}
.listening-bar:nth-child(1) {{ animation-delay: 0.0s; height: 20px; }}
.listening-bar:nth-child(2) {{ animation-delay: 0.1s; height: 30px; }}
.listening-bar:nth-child(3) {{ animation-delay: 0.2s; height: 38px; }}
.listening-bar:nth-child(4) {{ animation-delay: 0.3s; height: 26px; }}
.listening-bar:nth-child(5) {{ animation-delay: 0.4s; height: 34px; }}
.listening-bar:nth-child(6) {{ animation-delay: 0.5s; height: 18px; }}
.listening-bar:nth-child(7) {{ animation-delay: 0.4s; height: 30px; }}
.listening-bar:nth-child(8) {{ animation-delay: 0.3s; height: 40px; }}
.listening-bar:nth-child(9) {{ animation-delay: 0.2s; height: 24px; }}
@keyframes wave-bar {{
    0%, 100% {{ transform: scaleY(0.4); opacity: 0.6; }}
    50%       {{ transform: scaleY(1);   opacity: 1; }}
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {SIDEBAR_BORDER} !important;
}}
section[data-testid="stSidebar"] * {{
    color: {SIDEBAR_TEXT} !important;
}}
.sidebar-user {{
    background: linear-gradient(135deg, rgba(255,215,0,0.18), rgba(255,107,107,0.12));
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 12px; padding: 10px 14px;
    color: {"#8B6914" if IS_LIGHT else "#FFD700"} !important;
    font-weight: 700; font-size: 14px; text-align: center;
    position: relative; z-index: 1;
}}

/* ── ALL INPUT / WIDGET TEXT VISIBILITY ── */

/* Text input container */
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] p {{
    color: {INPUT_LABEL} !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}}
/* The actual input box */
div[data-testid="stTextInput"] input {{
    background: {INPUT_BG} !important;
    border: 2px solid {INPUT_BORDER} !important;
    border-radius: 12px !important;
    color: {INPUT_TEXT} !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    caret-color: {INPUT_TEXT} !important;
}}
div[data-testid="stTextInput"] input::placeholder {{
    color: {TEXT_MUTED} !important;
    opacity: 0.9 !important;
}}
div[data-testid="stTextInput"] input:focus {{
    border-color: #FFD700 !important;
    box-shadow: 0 0 0 3px rgba(255,215,0,0.25) !important;
    outline: none !important;
}}

/* Password input */
div[data-testid="stTextInput"] input[type="password"] {{
    color: {INPUT_TEXT} !important;
    background: {INPUT_BG} !important;
}}

/* Number input */
div[data-testid="stNumberInput"] label,
div[data-testid="stNumberInput"] p {{
    color: {INPUT_LABEL} !important;
    font-weight: 600 !important;
}}
div[data-testid="stNumberInput"] input {{
    background: {INPUT_BG} !important;
    border: 2px solid {INPUT_BORDER} !important;
    color: {INPUT_TEXT} !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}}

/* Selectbox */
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] p {{
    color: {INPUT_LABEL} !important;
    font-weight: 600 !important;
}}
div[data-testid="stSelectbox"] > div > div {{
    background: {INPUT_BG} !important;
    border: 2px solid {INPUT_BORDER} !important;
    border-radius: 10px !important;
    color: {INPUT_TEXT} !important;
}}
div[data-testid="stSelectbox"] svg {{ fill: {INPUT_TEXT} !important; }}

/* Radio buttons */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] p {{
    color: {RADIO_TEXT} !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}}
div[data-testid="stRadio"] > label {{
    color: {INPUT_LABEL} !important;
    font-weight: 700 !important;
}}
/* Radio button circles */
div[data-testid="stRadio"] [role="radio"] {{
    border-color: {INPUT_BORDER} !important;
}}

/* All markdown text */
.stMarkdown p, .stMarkdown span, .stMarkdown li,
.element-container p, .element-container span {{
    color: {TEXT_PRIMARY} !important;
}}

/* Streamlit default text */
p, span, label, .stText {{
    color: {TEXT_PRIMARY} !important;
}}

/* ── Buttons ── */
.stButton > button {{
    border-radius: 14px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 700 !important;
    border: 2px solid {BTN_BORDER} !important;
    background: {BTN_BG} !important;
    color: {BTN_TEXT} !important;
    font-size: 15px !important;
    transition: all 0.2s !important;
    padding: 8px 18px !important;
}}
.stButton > button:hover {{
    background: {BTN_HOVER_BG} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255,193,7,0.25) !important;
    border-color: #FFD700 !important;
}}
.stButton > button:focus {{
    color: {BTN_TEXT} !important;
    background: {BTN_HOVER_BG} !important;
}}

/* ── Progress bar ── */
.stProgress > div > div > div {{
    background: linear-gradient(90deg, {PROGRESS_FROM}, {PROGRESS_TO}) !important;
    border-radius: 8px !important;
}}

/* ── Expander ── */
div[data-testid="stExpander"] {{
    background: {EXPANDER_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 14px !important;
}}
div[data-testid="stExpander"] summary {{
    color: {TEXT_PRIMARY} !important;
    font-weight: 700 !important;
}}

/* ── Audio widget ── */
audio {{ filter: {'invert(0)' if not IS_LIGHT else 'none'}; }}

/* ── Ensure all text inside cards is visible ── */
.card * {{ color: {TEXT_PRIMARY} !important; }}

/* Override Streamlit's default white card backgrounds in light mode */
{"" if IS_LIGHT else ""}
[data-testid="stVerticalBlock"] > div {{
    position: relative; z-index: 1;
}}

/* Force sidebar radio options visible */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label p,
section[data-testid="stSidebar"] div[data-testid="stRadio"] label span {{
    color: {SIDEBAR_TEXT} !important;
    font-weight: 600 !important;
}}

/* Dropdown popup menu */
div[data-baseweb="select"] ul li,
div[data-baseweb="popover"] li {{
    color: {"#1a1a2e" if IS_LIGHT else "#f0f0f0"} !important;
    background: {"#fffef0" if IS_LIGHT else "#1a1a2e"} !important;
}}

/* Checkbox */
div[data-testid="stCheckbox"] label p {{
    color: {TEXT_PRIMARY} !important;
    font-weight: 600 !important;
}}

/* Column text */
div[data-testid="column"] p,
div[data-testid="column"] span,
div[data-testid="column"] label {{
    color: {TEXT_PRIMARY} !important;
}}
</style>

<!-- Floating orbs -->
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
{"<div class='lightning-bolt lb-1'>⚡</div><div class='lightning-bolt lb-2'>⚡</div><div class='lightning-bolt lb-3'>⚡</div>" if IS_LIGHT else ""}
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════
def set_notif(msg: str, kind: str = "success"):
    st.session_state.notif = msg
    st.session_state.notif_type = kind


def show_notif():
    if st.session_state.notif:
        kind = st.session_state.notif_type
        cls  = f"toast-{kind}"
        icons = {"success": "✅", "error": "❌", "info": "ℹ️"}
        icon  = icons.get(kind, "🔔")
        st.markdown(
            f"<div class='{cls}'>{icon} {st.session_state.notif}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.notif = None


def reset_quiz():
    st.session_state.quiz_q_index  = 0
    st.session_state.quiz_answers  = {}
    st.session_state.quiz_submitted = False
    st.session_state.quiz_timer    = time.time()


def reset_game():
    st.session_state.game_questions   = []
    st.session_state.game_q_index     = 0
    st.session_state.game_score       = 0
    st.session_state.game_total       = 0
    st.session_state.game_show_answer = False
    st.session_state.game_user_answer = ""
    st.session_state.game_started     = False
    st.session_state.arrange_items    = []


def txt(content: str, color: str = None, size: str = "16px",
        weight: str = "600", extra: str = ""):
    """Render inline text with guaranteed colour."""
    c = color or TEXT_PRIMARY
    st.markdown(
        f"<p style='color:{c};font-size:{size};font-weight:{weight};"
        f"position:relative;z-index:1;{extra}'>{content}</p>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════
#  LOGIN SCREEN
# ══════════════════════════════════════════════════════════════════════
if not st.session_state.user:
    st.markdown("<div class='hero'>🌈 Kids AI World</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center;color:{TEXT_MUTED};font-size:17px;"
        f"position:relative;z-index:1'>✨ Learn anything with stories, quizzes & games!</p>",
        unsafe_allow_html=True,
    )

    menu = st.sidebar.selectbox("Navigation", ["🚀 Login", "📝 Register", "🔑 Forgot Password"])
    show_notif()

    col_l, col_m, col_r = st.columns([1, 1.4, 1])
    with col_m:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if menu == "🚀 Login":
            st.markdown(f"<h3 style='color:{TEXT_PRIMARY}'>🚀 Welcome Back!</h3>", unsafe_allow_html=True)
            u = st.text_input("📧 Email", placeholder="your@email.com", key="login_email")
            p = st.text_input("🔒 Password", type="password", placeholder="••••••••", key="login_pass")
            if st.button("Login →", key="login_btn", use_container_width=True):
                if login(u, p):
                    st.session_state.user = u
                    set_notif(f"Welcome back! Ready to learn? 🎉", "success")
                    st.rerun()
                else:
                    set_notif("Invalid email or password. Try again!", "error")
                    st.rerun()

        elif menu == "📝 Register":
            st.markdown(f"<h3 style='color:{TEXT_PRIMARY}'>📝 Join Kids AI World!</h3>", unsafe_allow_html=True)
            u = st.text_input("📧 Email", placeholder="your@email.com", key="reg_email")
            p = st.text_input("🔒 Password", type="password", placeholder="••••••••", key="reg_pass")
            if st.button("Create Account →", key="register_btn", use_container_width=True):
                result = register(u, p)
                set_notif(result, "success")
                st.rerun()

        elif menu == "🔑 Forgot Password":
            st.markdown(f"<h3 style='color:{TEXT_PRIMARY}'>🔑 Reset Password</h3>", unsafe_allow_html=True)
            u = st.text_input("📧 Email", placeholder="your@email.com", key="reset_email")
            p = st.text_input("🔒 New Password", type="password", placeholder="••••••••", key="reset_pass")
            if st.button("Reset Password →", key="reset_btn", use_container_width=True):
                reset_password(u, p)
                set_notif("Password reset successfully!", "success")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR  (logged in)
# ══════════════════════════════════════════════════════════════════════
show_notif()

st.sidebar.markdown(
    f"<div class='sidebar-user'>👤 {st.session_state.user}</div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

# ── Theme toggle ──
theme_icon  = "⚡ Lightning Mode" if not IS_LIGHT else "🌙 Dark Mode"
theme_help  = "Switch to Lightning (bright) mode" if not IS_LIGHT else "Switch to Dark mode"
if st.sidebar.button(theme_icon, key="theme_toggle", use_container_width=True, help=theme_help):
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()

current_badge = (
    "<span style='background:#FFD700;color:#1a1a2e;padding:2px 8px;"
    "border-radius:8px;font-size:11px;font-weight:800'>⚡ LIGHTNING</span>"
    if IS_LIGHT else
    "<span style='background:#A855F7;color:#fff;padding:2px 8px;"
    "border-radius:8px;font-size:11px;font-weight:800'>🌙 DARK</span>"
)
st.sidebar.markdown(
    f"<div style='text-align:center;margin:-4px 0 8px 0'>{current_badge}</div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

st.sidebar.markdown(f"<b style='color:{SIDEBAR_TEXT}'>⚙️ Settings</b>", unsafe_allow_html=True)
language = st.sidebar.selectbox("🌐 Language", ["English", "Hindi", "Telugu", "Kannada"])
st.sidebar.markdown("---")
st.sidebar.markdown(f"<b style='color:{SIDEBAR_TEXT}'>📂 Navigate</b>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Page",
    ["🏠 Home", "🧠 Quiz", "🎮 Game", "📜 History"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")

if st.session_state.current_prompt:
    st.sidebar.markdown(
        f"<div style='background:rgba(78,205,196,0.14);border:1px solid rgba(78,205,196,0.35);"
        f"border-radius:10px;padding:8px 12px;color:#0e9488;font-size:13px;text-align:center'>"
        f"📌 Topic: <b>{st.session_state.current_prompt}</b></div>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("")

if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()


# ══════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("<div class='hero'>🌈 Learn with Fun!</div>", unsafe_allow_html=True)

    col_inp, col_btn = st.columns([4, 1])
    with col_inp:
        prompt = st.text_input(
            "✏️ What do you want to learn today?",
            placeholder="Try: Solar System, Elephants, Ocean, Robots...",
            key="home_prompt",
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("✨ Generate!", key="generate_main", use_container_width=True)

    if gen_btn:
        if not prompt.strip():
            set_notif("Please type a topic first!", "error")
            st.rerun()
        else:
            cleaned = prompt.strip()
            with st.spinner("🎨 Creating your learning world… This takes ~60s"):
                try:
                    story, image, audio, video, quiz, game_data, pieces = run(cleaned)
                    st.session_state.current_prompt = cleaned
                    st.session_state.story          = story
                    st.session_state.image          = image
                    st.session_state.audio          = audio
                    st.session_state.video          = video
                    st.session_state.quiz           = quiz
                    st.session_state.game_data      = game_data
                    st.session_state.pieces         = pieces
                    if cleaned not in st.session_state.history:
                        st.session_state.history.append(cleaned)
                    reset_quiz()
                    reset_game()
                    set_notif(f"🎉 Learning world for '{cleaned}' is ready!", "success")
                except Exception as e:
                    set_notif(f"Something went wrong: {str(e)[:80]}", "error")
            st.rerun()

    show_notif()

    if st.session_state.story:
        st.markdown("---")

        # Story section
        st.markdown(f"<h2 style='color:{TEXT_PRIMARY}'>📖 Story</h2>", unsafe_allow_html=True)
        lines = st.session_state.story.split("\n")
        story_html = "".join(
            f"<p style='margin:6px 0;font-size:17px;line-height:1.7;color:{TEXT_PRIMARY}'>🔸 {l}</p>"
            for l in lines if l.strip()
        )
        st.markdown(f"<div class='card'>{story_html}</div>", unsafe_allow_html=True)

        col_img, col_aud = st.columns([3, 2])

        with col_img:
            if st.session_state.image and os.path.exists(st.session_state.image):
                st.markdown(f"<h3 style='color:{TEXT_PRIMARY}'>🖼️ Illustration</h3>", unsafe_allow_html=True)
                st.image(st.session_state.image, use_container_width=True)

        with col_aud:
            if st.session_state.audio and os.path.exists(st.session_state.audio):
                st.markdown(f"<h3 style='color:{TEXT_PRIMARY}'>🎧 Listening Mode</h3>", unsafe_allow_html=True)
                st.markdown("""
                <div class='listening-panel'>
                    <div style='font-size:15px;color:#c084fc;font-weight:700;margin-bottom:4px'>
                        🎵 Story Narration
                    </div>
                    <div class='listening-waves'>
                        <div class='listening-bar'></div><div class='listening-bar'></div>
                        <div class='listening-bar'></div><div class='listening-bar'></div>
                        <div class='listening-bar'></div><div class='listening-bar'></div>
                        <div class='listening-bar'></div><div class='listening-bar'></div>
                        <div class='listening-bar'></div>
                    </div>
                    <div style='font-size:13px;color:#94a3b8;margin-top:4px'>
                        Press ▶ to listen to the story
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.audio(st.session_state.audio)

        if st.session_state.video and os.path.exists(str(st.session_state.video)):
            st.markdown(f"<h3 style='color:{TEXT_PRIMARY}'>🎬 Story Animation</h3>", unsafe_allow_html=True)
            st.video(st.session_state.video)
        elif st.session_state.video == "":
            st.markdown(
                f"<div class='card' style='border-left:4px solid #f59e0b;"
                f"color:{'#92400e' if IS_LIGHT else '#fbbf24'}'>"
                "⚠️ Video generation skipped. Install <code>moviepy</code> to enable videos."
                "</div>", unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            f"<div class='card' style='text-align:center;color:{TEXT_MUTED};font-size:15px'>"
            f"👈 Use the sidebar to take the <b style='color:#FFD700'>Quiz</b>, "
            f"play <b style='color:#4ECDC4'>Games</b>, or view your "
            f"<b style='color:#A855F7'>History</b>!"
            f"</div>",
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════
#  QUIZ
# ══════════════════════════════════════════════════════════════════════
elif page == "🧠 Quiz":
    st.markdown("<div class='hero'>🧠 Smart Quiz</div>", unsafe_allow_html=True)

    if not st.session_state.quiz:
        st.markdown(
            f"<div class='card' style='text-align:center;border-left:4px solid #f59e0b;"
            f"color:{'#92400e' if IS_LIGHT else '#fbbf24'}'>"
            "⚠️ Go to <b>🏠 Home</b> first and generate a topic!</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    quiz_data = st.session_state.quiz

    if st.session_state.quiz_timer == 0.0:
        st.session_state.quiz_timer = time.time()

    # ── Active quiz ──
    if not st.session_state.quiz_submitted:
        i = max(0, min(st.session_state.quiz_q_index, len(quiz_data) - 1))
        st.session_state.quiz_q_index = i
        q = quiz_data[i]

        elapsed   = int(time.time() - st.session_state.quiz_timer)
        remaining = max(60 - elapsed, 0)

        top_col1, top_col2, top_col3 = st.columns([3, 1, 1])
        with top_col1:
            st.progress((i) / len(quiz_data))
            st.markdown(
                f"<div style='color:{TEXT_MUTED};font-size:13px;position:relative;z-index:1'>"
                f"Question <b style='color:{TEXT_PRIMARY}'>{i+1}</b> "
                f"of <b style='color:{TEXT_PRIMARY}'>{len(quiz_data)}</b></div>",
                unsafe_allow_html=True,
            )
        with top_col2:
            timer_color = "#16a34a" if remaining > 30 else ("#ca8a04" if remaining > 15 else "#dc2626")
            st.markdown(
                f"<div style='text-align:center;font-family:Boogaloo,cursive;font-size:28px;"
                f"color:{timer_color};position:relative;z-index:1'>⏱ {remaining}s</div>",
                unsafe_allow_html=True,
            )
        with top_col3:
            answered = len(st.session_state.quiz_answers)
            st.markdown(
                f"<div style='text-align:center;color:{TEXT_MUTED};font-size:13px;"
                f"position:relative;z-index:1'>"
                f"✅ {answered}/{len(quiz_data)}<br>answered</div>",
                unsafe_allow_html=True,
            )

        if remaining == 0:
            st.session_state.quiz_q_index += 1
            st.session_state.quiz_timer    = time.time()
            if st.session_state.quiz_q_index >= len(quiz_data):
                st.session_state.quiz_submitted = True
            st.rerun()

        # Question card
        st.markdown(
            f"<div class='q-card' style='color:{TEXT_PRIMARY} !important'>"
            f"Q{i+1}. {q['q']}</div>",
            unsafe_allow_html=True,
        )

        # Options as radio
        saved     = st.session_state.quiz_answers.get(i)
        saved_idx = None
        if saved in q["options"]:
            saved_idx = q["options"].index(saved)

        choice = st.radio(
            "Choose your answer:",
            q["options"],
            index=saved_idx,
            key=f"quiz_radio_{i}_{st.session_state.current_prompt}",
        )
        if choice:
            st.session_state.quiz_answers[i] = choice

        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            if i > 0:
                if st.button("⬅️ Back", key=f"qback_{i}", use_container_width=True):
                    st.session_state.quiz_q_index -= 1
                    st.session_state.quiz_timer    = time.time()
                    st.rerun()
        with nav2:
            if i < len(quiz_data) - 1:
                if st.button("➡️ Next", key=f"qnext_{i}", use_container_width=True):
                    st.session_state.quiz_q_index += 1
                    st.session_state.quiz_timer    = time.time()
                    st.rerun()
        with nav3:
            if i == len(quiz_data) - 1:
                if st.button("🎯 Submit Quiz", key="qsubmit", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    st.rerun()

        # Question mini-map
        st.markdown("<br>", unsafe_allow_html=True)
        mini_cols = st.columns(len(quiz_data))
        for qi, col in enumerate(mini_cols):
            with col:
                is_answered = qi in st.session_state.quiz_answers
                is_current  = qi == i
                bg     = "#a855f7" if is_current else ("#22c55e" if is_answered else ("rgba(0,0,0,0.12)" if IS_LIGHT else "rgba(255,255,255,0.1)"))
                border = "2px solid #1a1a2e" if is_current else "1px solid transparent"
                num_color = "#fff" if (is_current or is_answered) else TEXT_MUTED
                st.markdown(
                    f"<div style='width:28px;height:28px;background:{bg};border-radius:50%;"
                    f"border:{border};text-align:center;line-height:28px;font-size:12px;"
                    f"font-weight:700;margin:auto;color:{num_color};position:relative;z-index:1'>"
                    f"{qi+1}</div>",
                    unsafe_allow_html=True,
                )

    # ── Results ──
    else:
        st.balloons()
        score = sum(
            1 for idx, q in enumerate(quiz_data)
            if st.session_state.quiz_answers.get(idx) == q["answer"]
        )
        total = len(quiz_data)
        pct   = int(score / total * 100)

        if pct >= 80:
            grade, grade_color, grade_msg = "🏆 Excellent!", "#ca8a04" if IS_LIGHT else "#FFD700", "You're a superstar learner!"
        elif pct >= 60:
            grade, grade_color, grade_msg = "👍 Good Job!", "#0d9488", "Keep practicing and you'll be amazing!"
        elif pct >= 40:
            grade, grade_color, grade_msg = "📚 Keep Going!", "#7c3aed", "Read the story again and retry!"
        else:
            grade, grade_color, grade_msg = "💪 Try Again!", "#dc2626", "Don't give up — you can do it!"

        st.markdown(f"""
        <div class='score-card'>
            <div style='font-family:Boogaloo,cursive;font-size:52px;color:{TEXT_PRIMARY}'>{grade}</div>
            <h2 style='color:{grade_color};font-family:Boogaloo,cursive;font-size:38px'>{score} / {total}</h2>
            <h3 style='color:{TEXT_MUTED}'>{pct}% correct</h3>
            <p style='color:{TEXT_SECONDARY}'>{grade_msg}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score / total)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:{TEXT_PRIMARY}'>📘 Answer Review</h2>", unsafe_allow_html=True)

        for idx, q in enumerate(quiz_data):
            user_ans = st.session_state.quiz_answers.get(idx, "⏭ Skipped")
            correct  = q["answer"]
            is_right = user_ans == correct
            icon     = "✅" if is_right else "❌"
            bg       = "rgba(74,222,128,0.12)" if is_right else "rgba(248,113,113,0.12)"
            border   = "rgba(74,222,128,0.5)"  if is_right else "rgba(248,113,113,0.5)"
            st.markdown(
                f"<div class='card' style='background:{bg};border-color:{border}'>"
                f"<b style='color:{TEXT_PRIMARY}'>Q{idx+1}.</b> "
                f"<span style='color:{TEXT_PRIMARY}'>{q['q']}</span><br><br>"
                f"<span style='color:{TEXT_SECONDARY}'>Your answer: <b>{user_ans}</b> {icon}</span><br>"
                f"<span style='color:#16a34a'>✔ Correct: <b>{correct}</b></span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        if st.button("🔄 Try Again", key="quiz_retry"):
            reset_quiz()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
#  GAME
# ══════════════════════════════════════════════════════════════════════
elif page == "🎮 Game":
    st.markdown("<div class='hero'>🎮 Game Zone!</div>", unsafe_allow_html=True)

    if not st.session_state.game_data:
        st.markdown(
            f"<div class='card' style='text-align:center;border-left:4px solid #f59e0b;"
            f"color:{'#92400e' if IS_LIGHT else '#fbbf24'}'>"
            "⚠️ Go to <b>🏠 Home</b> first and generate a topic!</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    words  = st.session_state.game_data.get("words", [])
    pieces = st.session_state.pieces

    game_type = st.selectbox(
        "🎲 Choose your game:",
        ["🔀 Unscramble", "🧩 Puzzle (Guess Word)", "✏️ Crossword Fill", "🖼️ Image Arrangement"],
        key="game_type_select",
    )

    def build_game_questions(gtype: str) -> list:
        qs     = []
        sample = random.sample(words, min(8, len(words)))
        for w in sample:
            w = w.lower().strip()
            if not w or len(w) < 3:
                continue
            if "Unscramble" in gtype:
                shuffled = list(w)
                for _ in range(30):
                    random.shuffle(shuffled)
                    if "".join(shuffled) != w:
                        break
                qs.append({"type": "unscramble", "display": "".join(shuffled).upper(), "answer": w})
            elif "Puzzle" in gtype:
                hint = w[0] + " _ " * (len(w) - 1)
                qs.append({"type": "puzzle", "display": hint.upper(), "answer": w,
                           "hint": f"Starts with '{w[0].upper()}', {len(w)} letters long"})
            elif "Crossword" in gtype:
                idx   = random.randint(1, len(w) - 1)
                chars = list(w.upper())
                chars[idx] = "_"
                qs.append({"type": "crossword", "display": " ".join(chars),
                           "answer": w[idx], "full_word": w})
            elif "Image" in gtype:
                if pieces and len(pieces) >= 4:
                    qs.append({"type": "arrange", "answer": w, "pieces": pieces[:6]})
                else:
                    shuffled = list(w)
                    random.shuffle(shuffled)
                    qs.append({"type": "unscramble", "display": "".join(shuffled).upper(), "answer": w})
        return qs

    if st.button("▶️ Start Game", key="start_game_btn", use_container_width=False):
        st.session_state.game_questions   = build_game_questions(game_type)
        st.session_state.game_q_index     = 0
        st.session_state.game_score       = 0
        st.session_state.game_total       = 0
        st.session_state.game_show_answer = False
        st.session_state.game_user_answer = ""
        st.session_state.game_started     = True
        st.session_state.game_type        = game_type
        st.session_state.arrange_items    = []
        set_notif("🎮 Game started! Good luck!", "info")
        st.rerun()

    show_notif()

    if not st.session_state.game_started or not st.session_state.game_questions:
        st.markdown(
            f"<div class='card' style='text-align:center;color:{TEXT_MUTED}'>"
            f"👆 Choose a game type and press <b style='color:#4ECDC4'>Start Game</b>!</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Game over ──
    if st.session_state.game_q_index >= len(st.session_state.game_questions):
        st.balloons()
        score = st.session_state.game_score
        total = st.session_state.game_total
        pct   = int(score / total * 100) if total > 0 else 0

        st.markdown(f"""
        <div class='score-card'>
            <div style='font-family:Boogaloo,cursive;font-size:52px;color:{TEXT_PRIMARY}'>🎉 Game Over!</div>
            <h2 style='color:#FFD700;font-family:Boogaloo,cursive;font-size:42px'>{score} / {total}</h2>
            <h3 style='color:{TEXT_MUTED}'>{pct}% Correct</h3>
        </div>
        """, unsafe_allow_html=True)
        if total > 0:
            st.progress(score / total)
        if st.button("🔄 Play Again", key="game_play_again"):
            reset_game()
            st.rerun()
        st.stop()

    # ── Current question ──
    qi       = st.session_state.game_q_index
    q        = st.session_state.game_questions[qi]
    total_qs = len(st.session_state.game_questions)

    st.progress(qi / total_qs)
    prog_col1, prog_col2 = st.columns(2)
    with prog_col1:
        st.markdown(
            f"<div style='color:{TEXT_MUTED};font-size:13px;position:relative;z-index:1'>"
            f"Question <b style='color:{TEXT_PRIMARY}'>{qi+1}</b> "
            f"of <b style='color:{TEXT_PRIMARY}'>{total_qs}</b></div>",
            unsafe_allow_html=True,
        )
    with prog_col2:
        st.markdown(
            f"<div style='text-align:right;color:#0d9488;font-size:13px;"
            f"position:relative;z-index:1'>"
            f"Score: <b>{st.session_state.game_score}</b> / {st.session_state.game_total}</div>",
            unsafe_allow_html=True,
        )

    qtype = q["type"]

    # ══ UNSCRAMBLE ══
    if qtype == "unscramble":
        st.markdown(
            f"<div class='card'><b style='color:#2563eb'>🔀 Unscramble the word!</b></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='game-word'>{q['display']}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:center;color:{TEXT_MUTED};font-size:14px;"
            f"position:relative;z-index:1'>({len(q['answer'])} letters)</div>",
            unsafe_allow_html=True,
        )
        if not st.session_state.game_show_answer:
            ans = st.text_input("Your answer:", key=f"u_inp_{qi}", placeholder="Type the word here...").strip().lower()
            if st.button("✅ Check Answer", key=f"u_chk_{qi}", use_container_width=False):
                st.session_state.game_total += 1
                if ans == q["answer"]:
                    st.session_state.game_score += 1
                st.session_state.game_user_answer = ans
                st.session_state.game_show_answer = True
                st.rerun()

    # ══ PUZZLE ══
    elif qtype == "puzzle":
        st.markdown(
            f"<div class='card'><b style='color:#7c3aed'>🧩 Guess the hidden word!</b></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='game-word'>{q['display']}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:center;color:#7c3aed;font-size:15px;margin-bottom:12px;"
            f"position:relative;z-index:1'>💡 Hint: {q['hint']}</div>",
            unsafe_allow_html=True,
        )
        if not st.session_state.game_show_answer:
            ans = st.text_input("Your answer:", key=f"p_inp_{qi}", placeholder="Type the full word...").strip().lower()
            if st.button("✅ Check Answer", key=f"p_chk_{qi}", use_container_width=False):
                st.session_state.game_total += 1
                if ans == q["answer"]:
                    st.session_state.game_score += 1
                st.session_state.game_user_answer = ans
                st.session_state.game_show_answer = True
                st.rerun()

    # ══ CROSSWORD ══
    elif qtype == "crossword":
        st.markdown(
            f"<div class='card'><b style='color:#0d9488'>✏️ Fill the missing letter!</b></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='game-word'>{q['display']}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:center;color:{TEXT_MUTED};font-size:14px;"
            f"position:relative;z-index:1'>"
            f"Word: <b style='color:{'#ca8a04' if IS_LIGHT else '#FFD700'}'>"
            f"{q['full_word'].upper()}</b> — what letter goes in the blank?</div>",
            unsafe_allow_html=True,
        )
        if not st.session_state.game_show_answer:
            ans = st.text_input("Missing letter:", key=f"c_inp_{qi}", max_chars=1,
                               placeholder="One letter only").strip().lower()
            if st.button("✅ Check Answer", key=f"c_chk_{qi}", use_container_width=False):
                st.session_state.game_total += 1
                if ans == q["answer"].lower():
                    st.session_state.game_score += 1
                st.session_state.game_user_answer = ans
                st.session_state.game_show_answer = True
                st.rerun()

    # ══ IMAGE ARRANGEMENT ══
    elif qtype == "arrange":
        st.markdown(
            f"<div class='card'><b style='color:#dc2626'>🖼️ Arrange the image pieces in the correct order!</b></div>",
            unsafe_allow_html=True,
        )
        img_paths = [p for p in q["pieces"] if os.path.exists(p)]
        n         = len(img_paths)

        if not st.session_state.arrange_items or len(st.session_state.arrange_items) != n:
            st.session_state.arrange_items = list(range(n))

        if not st.session_state.game_show_answer:
            st.markdown(
                f"<b style='color:{TEXT_PRIMARY}'>Current arrangement:</b>",
                unsafe_allow_html=True,
            )
            cols = st.columns(n)
            for display_pos, piece_idx in enumerate(st.session_state.arrange_items):
                with cols[display_pos]:
                    st.image(img_paths[piece_idx], use_container_width=True)
                    st.markdown(
                        f"<div style='text-align:center;color:{'#ca8a04' if IS_LIGHT else '#FFD700'};"
                        f"font-size:12px;font-weight:700;position:relative;z-index:1'>#{display_pos+1}</div>",
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f"<br><b style='color:{TEXT_PRIMARY}'>Swap two pieces to rearrange:</b>",
                unsafe_allow_html=True,
            )
            s1, s2, s3 = st.columns([1, 1, 1])
            with s1:
                swap_a = st.number_input("Position A", min_value=1, max_value=n, value=1,
                                        key=f"sa_{qi}") - 1
            with s2:
                swap_b = st.number_input("Position B", min_value=1, max_value=n, value=2,
                                        key=f"sb_{qi}") - 1
            with s3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Swap", key=f"swap_{qi}"):
                    arr                            = list(st.session_state.arrange_items)
                    arr[int(swap_a)], arr[int(swap_b)] = arr[int(swap_b)], arr[int(swap_a)]
                    st.session_state.arrange_items = arr
                    st.rerun()

            if st.button("✅ Submit Arrangement", key=f"arr_sub_{qi}"):
                correct_pos = sum(1 for k, v in enumerate(st.session_state.arrange_items) if v == k)
                is_correct  = correct_pos >= n // 2
                st.session_state.game_total += 1
                if is_correct:
                    st.session_state.game_score += 1
                st.session_state.game_user_answer = f"{correct_pos}/{n} pieces in place"
                st.session_state.game_show_answer = True
                st.rerun()

    # ══ Result panel ══
    if st.session_state.game_show_answer:
        user_ans   = st.session_state.game_user_answer
        correct_ans = q["answer"]

        if qtype == "arrange":
            parts  = user_ans.split("/")
            got    = int(parts[0])
            tot_p  = int(parts[1].split()[0])
            is_right = got >= tot_p // 2
        else:
            is_right = user_ans.lower().strip() == correct_ans.lower().strip()

        if is_right:
            st.markdown(
                f"<div class='toast-success'>✅ Correct! The answer is <b>{correct_ans.upper()}</b> 🎉</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='toast-error'>❌ Wrong! You said: <b>{user_ans.upper() or '(nothing)'}</b></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='toast-info' style='margin-top:8px'>"
                f"✏️ Correct answer: <b>{correct_ans.upper()}</b></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➡️ Next Question", key=f"gnext_{qi}", use_container_width=False):
            st.session_state.game_q_index     += 1
            st.session_state.game_show_answer  = False
            st.session_state.game_user_answer  = ""
            st.session_state.arrange_items     = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
#  HISTORY
# ══════════════════════════════════════════════════════════════════════
elif page == "📜 History":
    st.markdown("<div class='hero'>📜 Your Journey</div>", unsafe_allow_html=True)
    show_notif()

    if not st.session_state.history:
        st.markdown(
            f"<div class='card' style='text-align:center;color:{TEXT_MUTED}'>"
            "🔍 You haven't explored any topics yet.<br>"
            f"Go to <b style='color:{'#ca8a04' if IS_LIGHT else '#FFD700'}'>🏠 Home</b> and type something amazing!</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='card' style='text-align:center'>"
            f"<b style='color:#0d9488;font-size:18px'>🌟 {len(st.session_state.history)} topic(s) explored!</b>"
            f"</div>",
            unsafe_allow_html=True,
        )
        for idx, h in enumerate(reversed(st.session_state.history), 1):
            st.markdown(
                f"<div class='history-item'>"
                f"<span style='color:{TEXT_MUTED};font-size:12px'>#{idx}</span> &nbsp;"
                f"<b style='color:{TEXT_PRIMARY};font-size:16px'>🔍 {h}</b>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear History", key="clear_hist"):
            st.session_state.history = []
            set_notif("History cleared!", "info")
            st.rerun()