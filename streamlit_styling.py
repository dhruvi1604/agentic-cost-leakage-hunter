# =====================================================
# STREAMLIT DARK THEME STYLING
# Copy this entire file and save as: streamlit_styling.py
# Place in the SAME FOLDER as your streamlit_app.py
# =====================================================

import streamlit as st

def apply_dark_theme():
    """
    Applies a cohesive dark theme with minimal, professional styling
    to all Streamlit pages. No logic changes - purely visual enhancement.
    """
    
    st.markdown("""
    <style>
    /* =====================================================
       ROOT COLOR PALETTE
       ===================================================== */
    :root {
        --bg-primary: #0a0e27;
        --bg-secondary: #111a3a;
        --bg-tertiary: #1a2847;
        --accent-primary: #3b82f6;
        --accent-secondary: #10b981;
        --accent-warning: #f59e0b;
        --accent-danger: #ef4444;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --border-color: rgba(148, 163, 184, 0.1);
        --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* =====================================================
       GLOBAL STYLES
       ===================================================== */
    html, body, [class*="css"] {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Main content area */
    .main {
        background-color: var(--bg-primary);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    /* =====================================================
       HEADER & TITLE STYLES
       ===================================================== */
    h1 {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }

    h2 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--accent-primary);
        padding-bottom: 0.5rem;
    }

    h3 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 0.75rem;
    }

    h4 {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 1rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    /* =====================================================
       CARD STYLING (Your .card class)
       ===================================================== */
    .card {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 24px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }

    .card:hover {
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }

    /* =====================================================
       KPI STYLING (Your .kpi class)
       ===================================================== */
    .kpi {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent-primary);
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
        margin-bottom: 0.5rem;
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
    }

    .kpi-label {
        font-size: 0.95rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* =====================================================
       METRIC STYLING
       ===================================================== */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 16px;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        margin-bottom: 16px;
    }

    [data-testid="metric-container"] > div:first-child {
        color: var(--text-secondary);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="metric-container"] > div:nth-child(2) {
        color: var(--accent-primary);
        font-size: 1.75rem;
        font-weight: 700;
    }

    /* =====================================================
       BUTTON STYLES
       ===================================================== */
    button {
        background: linear-gradient(135deg, var(--accent-primary) 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    button:hover {
        background: linear-gradient(135deg, #2563eb 0%, var(--accent-primary) 100%);
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }

    button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.2);
    }

    /* =====================================================
       INPUT & SELECT STYLES
       ===================================================== */
    input, select, textarea {
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }

    input:focus, select:focus, textarea:focus {
        outline: none;
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        background-color: var(--bg-secondary);
    }

    /* File uploader styling */
    [data-testid="stFileUpload"] {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-tertiary));
        border: 2px dashed var(--accent-primary);
        border-radius: 10px;
        padding: 20px;
    }

    /* =====================================================
       SELECTBOX & RADIO STYLES
       ===================================================== */
    .stSelectbox > div > div {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }

    .stRadio > div {
        gap: 1rem;
    }

    .stRadio > div > label {
        color: var(--text-secondary);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .stRadio > div > label:hover {
        color: var(--text-primary);
    }

    /* =====================================================
       EXPANDER STYLES
       ===================================================== */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        font-weight: 600;
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--bg-tertiary);
        border-color: var(--accent-primary);
    }

    .streamlit-expanderContent {
        background-color: rgba(26, 40, 71, 0.5);
        border: 1px solid var(--border-color);
        border-top: none;
    }

    /* =====================================================
       INFO, WARNING, ERROR, SUCCESS MESSAGES
       ===================================================== */
    [data-testid="stAlert"] {
        border-radius: 10px;
        border-left: 4px solid;
        padding: 16px;
        margin-bottom: 16px;
    }

    /* Info message */
    [data-testid="stAlert"] > div {
        background-color: rgba(59, 130, 246, 0.1);
        border-left-color: var(--accent-primary);
    }

    /* Success message */
    [data-testid="stAlert"][kind="success"] > div {
        background-color: rgba(16, 185, 129, 0.1);
        border-left-color: var(--accent-secondary);
    }

    /* Warning message */
    [data-testid="stAlert"][kind="warning"] > div {
        background-color: rgba(245, 158, 11, 0.1);
        border-left-color: var(--accent-warning);
    }

    /* Error message */
    [data-testid="stAlert"][kind="error"] > div {
        background-color: rgba(239, 68, 68, 0.1);
        border-left-color: var(--accent-danger);
    }

    [data-testid="stAlert"] > div > div > p {
        color: var(--text-primary);
        font-weight: 500;
    }

    /* =====================================================
       DATAFRAME & TABLE STYLES
       ===================================================== */
    [data-testid="dataframe"] {
        background-color: var(--bg-secondary) !important;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Table header */
    [data-testid="dataframe"] thead {
        background-color: var(--bg-tertiary);
        border-bottom: 2px solid var(--accent-primary);
    }

    [data-testid="dataframe"] th {
        color: var(--text-primary);
        font-weight: 700;
        text-align: center;
        padding: 12px;
        background-color: var(--bg-tertiary);
    }

    /* Table body */
    [data-testid="dataframe"] td {
        color: var(--text-secondary);
        padding: 10px 12px;
        border-bottom: 1px solid var(--border-color);
    }

    [data-testid="dataframe"] tbody > tr:hover {
        background-color: rgba(59, 130, 246, 0.1);
    }

    /* =====================================================
       PLOTLY CHART STYLING
       ===================================================== */
    .plotly-graph-div {
        background-color: transparent !important;
    }

    .js-plotly-plot .plotly {
        background-color: transparent !important;
    }

    /* =====================================================
       COLUMN & LAYOUT STYLES
       ===================================================== */
    [data-testid="stHorizontalBlock"] {
        gap: 1.5rem;
    }

    /* =====================================================
       TEXT & PARAGRAPH STYLES
       ===================================================== */
    p {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }

    strong, b {
        color: var(--text-primary);
        font-weight: 700;
    }

    /* =====================================================
       LINK STYLES
       ===================================================== */
    a {
        color: var(--accent-primary);
        text-decoration: none;
        transition: all 0.2s ease;
        font-weight: 600;
    }

    a:hover {
        color: var(--accent-secondary);
        text-decoration: underline;
    }

    /* =====================================================
       SIDEBAR SPECIFIC STYLES
       ===================================================== */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    [data-testid="stSidebar"] label {
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* =====================================================
       DIVIDER STYLES
       ===================================================== */
    hr {
        border: none;
        border-top: 1px solid var(--border-color);
        margin: 2rem 0;
    }

    /* =====================================================
       SCROLLBAR STYLING
       ===================================================== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }

    /* =====================================================
       RESPONSIVE DESIGN
       ===================================================== */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.75rem;
        }

        h2 {
            font-size: 1.25rem;
        }

        .card {
            padding: 16px;
        }

        .kpi {
            font-size: 2rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.5rem;
        }
    }

    /* =====================================================
       ANIMATION & TRANSITIONS
       ===================================================== */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
    }

    /* Disable transitions on certain elements for performance */
    .plotly, .js-plotly-plot, iframe {
        transition: none;
    }

    </style>
    """, unsafe_allow_html=True)
