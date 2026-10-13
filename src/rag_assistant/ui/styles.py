"""Injects the app-wide CSS theme. Identical look to the Session 4 demo."""
import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --bg:      #080C14;
    --surface: #0D1320;
    --card:    #131C2E;
    --border:  #253450;
    --accent:  #00D4AA;
    --purple:  #8B7FFF;
    --amber:   #F5A623;
    --green:   #4ADE80;
    --red:     #FF6B6B;
    --text:    #F0F2FF;
    --sub:     #A8B4CC;
    --muted:   #6A7A96;
    --mono:    'Space Mono', monospace;
    --sans:    'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1100px !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.25rem !important;
}

/* ── ALL labels — large and visible ── */
label, .stTextInput label, .stTextArea label,
.stSelectbox label, .stFileUploader label,
.stNumberInput label, [data-testid="stWidgetLabel"] p {
    color: var(--sub) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    font-family: var(--sans) !important;
    margin-bottom: 6px !important;
}

/* ── Text inputs — large and visible ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    padding: 12px 16px !important;
    line-height: 1.5 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--muted) !important;
    font-size: 14px !important;
}

/* ── Password input ── */
input[type="password"] {
    font-family: var(--mono) !important;
    letter-spacing: 3px !important;
    color: var(--sub) !important;
    font-size: 14px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploadDropzone"] p {
    color: var(--sub) !important;
    font-size: 14px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00D4AA, #6C63FF) !important;
    color: #080C14 !important;
    font-family: var(--mono) !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 15px !important;
}

/* ── Tabs — the source selector tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-family: var(--sans) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--card) !important;
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.25rem !important;
    margin-top: 0 !important;
}

/* ── Section labels ── */
.section-label {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 2.5px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
    display: block;
}

/* ── Dividers ── */
.custom-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Answer card ── */
.answer-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1rem 0;
    line-height: 1.85;
    font-size: 16px;
    color: var(--text);
}

/* ── Source chunk cards ── */
.source-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--purple);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 6px 0;
    font-size: 14px;
    color: var(--sub);
    line-height: 1.7;
}
.source-url {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--purple);
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}

/* ── URL display badge ── */
.url-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--purple);
    border-radius: 8px;
    padding: 8px 14px;
    margin: 5px 0;
    font-family: var(--mono);
    font-size: 12px;
    color: var(--sub);
    word-break: break-all;
}

/* ── Stats row ── */
.stats-row { display: flex; gap: 1rem; margin: 1.2rem 0; flex-wrap: wrap; }
.stat-card {
    flex: 1;
    min-width: 100px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-value {
    font-family: var(--mono);
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-label {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
}

/* ── Info/success/warning/error boxes ── */
[data-testid="stInfo"]    { background:#253450!important;border:1px solid #3A5080!important;color:var(--sub)!important; }
[data-testid="stSuccess"] { background:#0D2A1E!important;border:1px solid #1A5C38!important;color:#4ADE80!important; }
[data-testid="stWarning"] { background:#2A1E00!important;border:1px solid #5C3D00!important;color:#F5A623!important; }
[data-testid="stError"]   { background:#2A0D0D!important;border:1px solid #5C1A1A!important;color:#FF6B6B!important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Sidebar section header ── */
.sidebar-header {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 2.5px;
    color: var(--accent);
    text-transform: uppercase;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

/* ── Hero title ── */
.hero-title {
    font-family: var(--mono);
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--accent);
    margin: 0 0 0.5rem;
    line-height: 1.1;
}
.hero-sub {
    font-size: 16px;
    color: var(--sub);
    font-weight: 400;
    margin: 0 0 1.5rem;
}

/* ── Tab content helper text ── */
.tab-helper {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.7;
    margin-bottom: 1rem;
    padding: 8px 12px;
    background: var(--surface);
    border-radius: 8px;
    border-left: 2px solid var(--border);
}
</style>
"""

def inject():
    st.markdown(_CSS, unsafe_allow_html=True)
