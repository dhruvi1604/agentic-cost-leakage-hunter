import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Enterprise Spend Intelligence Audit",
    layout="wide",
    page_icon="💼"
)

# =====================================================
# THEME
# =====================================================
def apply_advanced_professional_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg-body: #020617;
            --bg-shell: #030712;
            --bg-surface: #020617;
            --bg-surface-soft: #071225;
            --card-bg: #06101f;
            --accent-primary: #22c55e;
            --accent-secondary: #38bdf8;
            --accent-danger: #f97373;
            --accent-warning: #facc15;
            --accent-purple: #a855f7;
            --text-strong: #f8fafc;
            --text-primary: #e2e8f0;
            --text-secondary: #cbd5e1;
            --text-subtle: #94a3b8;
            --border-subtle: rgba(148, 163, 184, 0.22);
            --radius-lg: 18px;
            --radius-md: 12px;
            --shadow-soft: 0 16px 40px rgba(2, 6, 23, 0.65);
            --shadow-strong: 0 24px 50px rgba(2, 6, 23, 0.8);
            --transition-fast: 150ms ease-out;
        }

        html, body, [class*="css"] {
            background-color: var(--bg-body) !important;
            color: var(--text-primary) !important;
            font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }

        .main {
            background:
                radial-gradient(circle at top left, #081120 0, #020617 35%, #020617 100%) !important;
        }

        [data-testid="stAppViewBlockContainer"] {
            padding-top: 1.0rem;
            padding-bottom: 2rem;
            max-width: 1380px;
        }

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background: #020617 !important;
            border-right: 1px solid rgba(15, 23, 42, 0.95) !important;
            box-shadow: 18px 0 40px rgba(15, 23, 42, 0.95);
        }

        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-size: 0.8rem !important;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--text-subtle) !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] {
            border-radius: var(--radius-lg) !important;
            border: 1px solid rgba(148, 163, 184, 0.35) !important;
            background: #06101f !important;
            padding: 0.75rem 0.8rem 1rem 0.8rem !important;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.55);
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
            border-radius: 14px !important;
            border-style: dashed !important;
            border-color: rgba(148, 163, 184, 0.55) !important;
            background: #020617 !important;
        }

        .snapshot-title {
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(30, 41, 59, 0.95);
            font-size: 0.78rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--text-subtle);
        }

        [data-baseweb="radio"] > div { gap: 0.22rem; }

        [data-baseweb="radio"] label {
            border-radius: 999px !important;
            padding: 0.42rem 0.8rem !important;
            font-size: 0.84rem !important;
            color: var(--text-secondary) !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            transition: background var(--transition-fast), color var(--transition-fast), transform var(--transition-fast), border var(--transition-fast);
        }

        [data-baseweb="radio"] label:hover {
            background: #081120 !important;
            border-color: rgba(148, 163, 184, 0.22) !important;
            transform: translateX(1px);
        }

        [data-baseweb="radio"] input:checked + div > div {
            background: #0f766e !important;
            color: #f8fafc !important;
            border-color: rgba(45, 212, 191, 0.6) !important;
            box-shadow: 0 0 0 1px rgba(45, 212, 191, 0.35);
        }

        /* HEADINGS */
        h1, h2, h3 {
            font-weight: 700 !important;
            letter-spacing: 0.01em;
        }

        h1 {
            font-size: 1.75rem !important;
            color: var(--text-strong) !important;
        }

        h2 {
            font-size: 1.2rem !important;
            color: var(--text-strong) !important;
        }

        h3 {
            font-size: 1.02rem !important;
            color: var(--text-primary) !important;
        }

        .page-subtitle {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--text-subtle);
        }

        /* CARDS */
        .card {
            background: linear-gradient(180deg, rgba(6,16,31,0.96), rgba(4,10,20,0.98));
            border-radius: var(--radius-lg);
            padding: 1rem 1.25rem 1.25rem 1.25rem;
            border: 1px solid rgba(30, 41, 59, 0.95);
            margin-bottom: 0.95rem;
            box-shadow: var(--shadow-soft);
        }

        .card.header-bar {
            padding-top: 0.9rem;
            padding-bottom: 0.95rem;
            background: linear-gradient(180deg, rgba(3,8,20,1), rgba(5,12,24,1));
            border: 1px solid rgba(30, 41, 59, 0.95);
        }

        .kpi-wrapper { display: flex; flex-direction: column; gap: 0.25rem; }

        .kpi-label {
            font-size: 0.78rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--text-subtle);
        }

        .kpi {
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--text-strong);
        }

        .kpi-secondary {
            font-size: 0.88rem;
            color: var(--text-secondary);
        }

        .micro-kpi-card {
            background: rgba(8, 17, 32, 0.9);
            border: 1px solid rgba(30, 41, 59, 0.95);
            border-radius: 14px;
            padding: 0.8rem 0.9rem;
            min-height: 132px;
        }

        .micro-kpi-label {
            font-size: 0.68rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--text-subtle);
        }

        .micro-kpi-value {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-strong);
            margin-top: 0.2rem;
            margin-bottom: 0.35rem;
        }

        /* badges */
        .badge-row {
            display: flex;
            gap: 0.55rem;
            flex-wrap: wrap;
            margin-top: 0.55rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.38rem;
            padding: 0.34rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .badge-success {
            background: rgba(34, 197, 94, 0.12);
            color: #86efac;
            border: 1px solid rgba(34, 197, 94, 0.25);
        }

        .badge-warning {
            background: rgba(250, 204, 21, 0.10);
            color: #fde68a;
            border: 1px solid rgba(250, 204, 21, 0.22);
        }

        .badge-danger {
            background: rgba(249, 115, 115, 0.12);
            color: #fca5a5;
            border: 1px solid rgba(249, 115, 115, 0.22);
        }

        .badge-info {
            background: rgba(56, 189, 248, 0.10);
            color: #7dd3fc;
            border: 1px solid rgba(56, 189, 248, 0.22);
        }

        /* AI brief cards */
        .ai-panel {
            background: linear-gradient(180deg, rgba(8,17,32,1), rgba(5,12,24,1));
            border: 1px solid rgba(30, 41, 59, 0.95);
            border-radius: 16px;
            padding: 1rem;
            margin-top: 0.75rem;
        }

        .ai-highlight-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 0.75rem;
            margin-bottom: 0.75rem;
        }

        .ai-highlight-card {
            background: rgba(2, 6, 23, 0.78);
            border: 1px solid rgba(30, 41, 59, 0.95);
            border-radius: 14px;
            padding: 0.9rem;
        }

        .ai-highlight-title {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: var(--text-subtle);
            margin-bottom: 0.35rem;
        }

        .ai-highlight-value {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-strong);
        }

        .ai-list {
            margin-top: 0.6rem;
            color: var(--text-primary);
        }

        .ai-list li {
            margin-bottom: 0.45rem;
        }

        /* metric */
        [data-testid="metric-container"] {
            background: #071225 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(30, 41, 59, 0.95) !important;
            padding: 0.7rem 0.9rem !important;
        }

        [data-testid="metric-container"] > div > div:nth-child(1) {
            font-size: 0.76rem !important;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--text-subtle) !important;
        }

        [data-testid="metric-container"] > div > div:nth-child(2) {
            font-size: 1.08rem !important;
            font-weight: 600 !important;
        }

        /* buttons */
        button, .stButton>button {
            border-radius: 999px !important;
            padding: 0.52rem 1.2rem !important;
            border: none !important;
            background: #16a34a !important;
            color: var(--text-strong) !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            box-shadow: 0 12px 24px rgba(22, 163, 74, 0.28) !important;
            transition: transform var(--transition-fast), box-shadow var(--transition-fast), filter var(--transition-fast);
        }

        button:hover, .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-strong) !important;
            filter: brightness(1.04);
        }

        .action-ghost button {
            background: #071225 !important;
            border: 1px solid rgba(148, 163, 184, 0.24) !important;
            box-shadow: none !important;
        }

        .action-ghost button:hover {
            border-color: #22c55e !important;
            box-shadow: 0 0 0 1px rgba(34, 197, 94, 0.3) !important;
        }

        /* alerts */
        [data-testid="stAlert"] {
            border-radius: 12px !important;
            border-left: 4px solid #38bdf8 !important;
            background: #071225 !important;
        }

        /* dataframe */
        [data-testid="dataframe"] {
            background: #071225 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(30, 41, 59, 0.95) !important;
        }

        [data-testid="dataframe"] thead tr {
            background: #0b1324 !important;
        }

        [data-testid="dataframe"] th {
            color: var(--text-secondary) !important;
            font-size: 0.76rem !important;
            text-transform: uppercase;
            letter-spacing: 0.16em;
        }

        [data-testid="dataframe"] tbody td {
            color: var(--text-primary) !important;
            font-size: 0.84rem !important;
        }

        [data-testid="dataframe"] tbody > tr:hover {
            background: rgba(30, 64, 175, 0.18) !important;
        }

        /* expanders */
        .streamlit-expanderHeader {
            background: #071225 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(30, 41, 59, 0.95) !important;
            color: var(--text-primary) !important;
        }

        .streamlit-expanderContent {
            background: #071225 !important;
            border-radius: 0 0 12px 12px !important;
            border: 1px solid rgba(30, 41, 59, 0.95) !important;
        }

        /* inputs */
        .stSelectbox > div > div,
        .stTextInput > div > div > input {
            background-color: #071225 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(51, 65, 85, 0.9) !important;
            color: var(--text-primary) !important;
        }

        .stSelectbox > div > div:hover {
            border-color: #38bdf8 !important;
        }

        p { color: var(--text-secondary) !important; font-size: 0.9rem; }
        a { color: #38bdf8 !important; }

        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: #020617; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 999px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_advanced_professional_theme()

# =====================================================
# IMPORTS - LOGIC UNCHANGED
# =====================================================
from src.validation.dataset_validator import (
    validate_expense_dataset,
    DatasetValidationError,
)
from src.schema.schema_adapter import normalize_schema
from src.features.build_features import build_all_features
from src.detection.anomaly_detection import detect_anomalies
from src.detection.leakage_rules import apply_leakage_rules
from src.detection.duplicate_detection import detect_duplicates
from src.rca.root_cause import assign_root_cause
from src.recommendations.recommend import generate_recommendations
from src.recommendations.savings_estimators import apply_savings_estimation
from src.memory.anomaly_log import initialize_anomaly_memory
from src.memory.metrics import (
    summarize_financials,
    top_vendors_by_exposure,
)
from src.scoring.health_score import calculate_health_grade
from src.scoring.vendor_risk import calculate_vendor_risk
from src.explainability.confidence_engine import generate_confidence_timeline
from src.llm.explain import explain_summary
from src.memory.snapshot_manager import (
    save_snapshot,
    load_snapshot,
    list_snapshots,
    compare_snapshots,
)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio(
        "",
        [
            "Executive Briefing",
            "Detected Issues",
            "Business Impact",
            "Evidence Story",
            "Duplicate Evidence",
            "Recommended Actions",
        ],
    )

    st.markdown("### Upload Expense CSV")
    uploaded_file = st.file_uploader(" ", type=["csv"], label_visibility="collapsed")

    st.markdown('<div class="snapshot-title">Snapshot Comparison</div>', unsafe_allow_html=True)
    compare_mode = st.radio(
        "Comparison Mode",
        ["No Comparison", "Compare With Previous", "Select Snapshot"],
        index=0,
    )

    st.markdown('<div class="snapshot-title">Snapshot Controls</div>', unsafe_allow_html=True)

if uploaded_file is None:
    st.info("Upload expense data to begin AI audit.")
    st.stop()

# =====================================================
# PIPELINE EXECUTION
# =====================================================
try:
    df_raw = pd.read_csv(uploaded_file)
    validate_expense_dataset(df_raw)

    df = normalize_schema(df_raw)
    df = build_all_features(df)

    df = detect_duplicates(df)
    df = apply_leakage_rules(df)
    df = detect_anomalies(df)

    df["root_cause"] = df.apply(assign_root_cause, axis=1)

    df = generate_recommendations(df)
    df = apply_savings_estimation(df)

    df = initialize_anomaly_memory(df)

    summary = summarize_financials(df)
    vendor_risk_df = calculate_vendor_risk(df)

except DatasetValidationError as e:
    st.error(str(e))
    st.stop()

# =====================================================
# SNAPSHOT BUILD
# =====================================================
summary_snapshot = {
    "total_spend": summary["total_spend"],
    "financial_exposure": summary["financial_exposure"],
    "recoverable_savings": summary["recoverable_savings"],
    "exposure_pct": summary["exposure_pct"],
    "recoverable_pct": summary.get("recoverable_pct", 0),
}

issues_snapshot = []
_grouped_issues = (
    df[df["financial_exposure"] > 0]
    .groupby("root_cause")
    .agg(
        count=("vendor", "count"),
        exposure=("financial_exposure", "sum"),
        recommended_action=("recommended_action", "first"),
    )
    .reset_index()
)

for _, row in _grouped_issues.iterrows():
    issues_snapshot.append(
        {
            "root_cause": row["root_cause"],
            "count": int(row["count"]),
            "exposure": float(row["exposure"]),
            "recommended_action": row["recommended_action"],
        }
    )

current_snapshot = {"summary": summary_snapshot, "issues": issues_snapshot}

with st.sidebar:
    available_snapshots = list_snapshots()
    previous_snapshot = None
    comparison_result = None

    if compare_mode == "Select Snapshot" and len(available_snapshots) > 0:
        snapshot_options = ["-- Clear Selection --"] + available_snapshots
        selected_file = st.selectbox("Select Snapshot", snapshot_options)
        if selected_file != "-- Clear Selection --":
            previous_snapshot = load_snapshot(selected_file)
    elif compare_mode == "Compare With Previous" and len(available_snapshots) > 0:
        previous_snapshot = load_snapshot(available_snapshots[-1])

    if previous_snapshot:
        comparison_result = compare_snapshots(previous_snapshot, current_snapshot)

    save_current = st.button("Save Current Snapshot")
    if save_current:
        file_id = save_snapshot(
            uploaded_file.name.replace(".csv", ""),
            df,
            summary_snapshot,
            issues_snapshot,
        )
        st.success(f"Snapshot saved: {file_id}")

# =====================================================
# HELPERS
# =====================================================
PLOTLY_DARK_TEMPLATE = "plotly_dark"
PAPER_BG = "#06101f"
PLOT_BG = "#020617"
AXIS_COLOR = "#94a3b8"
TITLE_COLOR = "#e2e8f0"

def style_fig(fig, title=None):
    fig.update_layout(
        template=PLOTLY_DARK_TEMPLATE,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TITLE_COLOR, family="Inter"),
        hovermode="x unified",
        margin=dict(t=45, r=24, b=40, l=55),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color=TITLE_COLOR)
        )
    )
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                x=0.01,
                xanchor="left",
                font=dict(size=16, color=TITLE_COLOR, family="Inter"),
            )
        )
    fig.update_xaxes(
        showgrid=False,
        linecolor="rgba(51, 65, 85, 0.7)",
        tickfont=dict(color=AXIS_COLOR),
    )
    fig.update_yaxes(
        gridcolor="rgba(30, 41, 59, 0.75)",
        zeroline=False,
        tickfont=dict(color=AXIS_COLOR),
    )
    return fig

def make_sparkline(series, color="#38bdf8"):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=series,
            mode="lines",
            line=dict(color=color, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(56,189,248,0.10)",
            hoverinfo="skip"
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=55,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig

def priority_badge_html(exposure_pct):
    if exposure_pct >= 5:
        return "<span class='badge badge-danger'>🔴 Critical Priority</span>"
    elif exposure_pct >= 2:
        return "<span class='badge badge-warning'>🟡 Elevated Priority</span>"
    else:
        return "<span class='badge badge-success'>🟢 Managed Exposure</span>"

def confidence_badge_html():
    return "<span class='badge badge-info'>🤖 AI Confidence Enabled</span>"

# =====================================================
# DERIVED UI SERIES
# =====================================================
anomaly_count = int(df["iforest_anomaly"].sum()) if "iforest_anomaly" in df.columns else 0
transaction_count = int(len(df))
unique_vendor_count = int(df["vendor"].nunique()) if "vendor" in df.columns else 0

df["date"] = pd.to_datetime(df["date"], errors="coerce")
daily_df = (
    df.dropna(subset=["date"])
    .groupby(df["date"].dt.date)
    .agg(
        spend=("amount", "sum"),
        anomalies=("financial_exposure", lambda x: (x > 0).sum()),
        vendors=("vendor", "nunique"),
    )
    .reset_index()
)

if len(daily_df) >= 30:
    recent_daily = daily_df.tail(30).copy()
elif len(daily_df) > 0:
    recent_daily = daily_df.copy()
else:
    recent_daily = pd.DataFrame(
        {
            "date": list(range(1, 31)),
            "spend": [0] * 30,
            "anomalies": [0] * 30,
            "vendors": [0] * 30,
        }
    )

# =====================================================
# PAGE 1 — EXECUTIVE BRIEFING
# =====================================================
if page == "Executive Briefing":
    st.markdown(
        "<div class='card header-bar'>"
        "<div class='page-subtitle'>AI CFO CONSOLE</div>"
        "<h1>Executive Briefing</h1>"
        "<p>Your enterprise spend, anomalies and savings opportunities in one narrative view.</p>"
        "<div class='badge-row'>"
        f"{priority_badge_html(summary['exposure_pct'])}"
        f"{confidence_badge_html()}"
        "<span class='badge badge-info'>📊 Live Audit View</span>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Main KPIs
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"<div class='kpi-wrapper'><div class='kpi-label'>Total Spend</div>"
            f"<div class='kpi'>₹{summary['total_spend']:,.0f}</div>"
            "<div class='kpi-secondary'>All audited transactions</div></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='kpi-wrapper'><div class='kpi-label'>Financial Exposure</div>"
            f"<div class='kpi'>₹{summary['financial_exposure']:,.0f}</div>"
            f"<div class='kpi-secondary'>{summary['exposure_pct']:.2f}% of total spend</div></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<div class='kpi-wrapper'><div class='kpi-label'>Recoverable Savings</div>"
            f"<div class='kpi'>₹{summary['recoverable_savings']:,.0f}</div>"
            "<div class='kpi-secondary'>Modeled savings potential</div></div>",
            unsafe_allow_html=True,
        )

    # Micro KPI cards + sparklines
    micro1, micro2, micro3 = st.columns(3)
    with micro1:
        st.markdown(
            f"<div class='micro-kpi-card'><div class='micro-kpi-label'>Transactions</div>"
            f"<div class='micro-kpi-value'>{transaction_count:,}</div></div>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            make_sparkline(recent_daily["spend"], "#38bdf8"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with micro2:
        st.markdown(
            f"<div class='micro-kpi-card'><div class='micro-kpi-label'>Vendors</div>"
            f"<div class='micro-kpi-value'>{unique_vendor_count:,}</div></div>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            make_sparkline(recent_daily["vendors"], "#22c55e"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with micro3:
        st.markdown(
            f"<div class='micro-kpi-card'><div class='micro-kpi-label'>Anomalies</div>"
            f"<div class='micro-kpi-value'>{anomaly_count:,}</div></div>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            make_sparkline(recent_daily["anomalies"], "#f97373"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Comparison
        # Comparison
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Change Since Selected Snapshot")

    if comparison_result is None:
        st.info("Select a snapshot from sidebar to compare.")
    else:
        delta = comparison_result["summary_delta"]

        # Top delta cards
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric(
                "Exposure Change",
                f"₹{delta['financial_exposure_change']:,.0f}",
                f"{delta['exposure_pct_change']:.2f}%"
            )
        with d2:
            st.metric(
                "Savings Change",
                f"₹{delta['recoverable_savings_change']:,.0f}"
            )
        with d3:
            st.metric(
                "Spend Change",
                f"₹{delta['total_spend_change']:,.0f}"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Issue status columns
        issue_col1, issue_col2, issue_col3 = st.columns(3)

        with issue_col1:
            st.markdown(
                """
                <div class='micro-kpi-card'>
                    <div class='micro-kpi-label'>Resolved Issues</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            resolved = comparison_result["issues_resolved"]
            if resolved:
                if isinstance(resolved, (list, tuple)):
                    for issue in resolved:
                        st.success(issue)
                else:
                    st.success(resolved)
            else:
                st.caption("None")

        with issue_col2:
            st.markdown(
                """
                <div class='micro-kpi-card'>
                    <div class='micro-kpi-label'>New Issues</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            new_issues = comparison_result["issues_new"]
            if new_issues:
                if isinstance(new_issues, (list, tuple)):
                    for issue in new_issues:
                        st.warning(issue)
                else:
                    st.warning(new_issues)
            else:
                st.caption("None")

        with issue_col3:
            st.markdown(
                """
                <div class='micro-kpi-card'>
                    <div class='micro-kpi-label'>Persisting Issues</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            persisting = comparison_result["issues_persisting"]
            if persisting:
                if isinstance(persisting, (list, tuple)):
                    for issue in persisting:
                        st.error(issue)
                else:
                    st.error(persisting)
            else:
                st.caption("None")

    st.markdown("</div>", unsafe_allow_html=True)


    # Health
    health = calculate_health_grade(summary["exposure_pct"])
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Financial Health Score")
    st.markdown(
        f"<div class='kpi-label'>Portfolio Health</div><div class='kpi'>{health['grade']}</div>",
        unsafe_allow_html=True,
    )
    st.write(f"{health['label']} — {health['description']}")
    st.markdown("</div>", unsafe_allow_html=True)

    # AI Brief
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### AI Executive Briefing")

    if "ai_summary" not in st.session_state:
        st.session_state["ai_summary"] = None

    if st.button("Generate AI Executive Report"):
        if not vendor_risk_df.empty:
            top_vendors = vendor_risk_df.head(3)[["vendor", "risk_index"]].to_dict(orient="records")
        else:
            top_vendors = []

        root_cause_breakdown = (
            df[df["financial_exposure"] > 0]
            .groupby("root_cause")["financial_exposure"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )

        if comparison_result:
            comparison_data = comparison_result
            is_first_upload = False
        else:
            comparison_data = None
            is_first_upload = True

        summary_payload = {
            "current_summary": {
                "total_spend": summary["total_spend"],
                "financial_exposure": summary["financial_exposure"],
                "recoverable_savings": summary["recoverable_savings"],
                "exposure_percentage": summary["exposure_pct"],
            },
            "top_risky_vendors": top_vendors,
            "root_cause_breakdown": root_cause_breakdown,
            "snapshot_comparison": comparison_data,
            "first_upload": is_first_upload
        }

        try:
            ai_text = explain_summary(summary_payload)
            st.session_state["ai_summary"] = ai_text
        except Exception as e:
            st.session_state["ai_summary"] = f"AI service unavailable. Error: {str(e)}"

    if st.session_state["ai_summary"]:
        top_root_cause = (
            df[df["financial_exposure"] > 0]
            .groupby("root_cause")["financial_exposure"]
            .sum()
            .sort_values(ascending=False)
        )
        top_root_cause_label = top_root_cause.index[0] if len(top_root_cause) > 0 else "No major issue"
        top_root_cause_value = top_root_cause.iloc[0] if len(top_root_cause) > 0 else 0

        st.markdown(
            "<div class='ai-panel'>"
            "<div class='badge-row'>"
            "<span class='badge badge-info'>🤖 Executive Summary</span>"
            f"{priority_badge_html(summary['exposure_pct'])}"
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class='ai-highlight-grid'>
                <div class='ai-highlight-card'>
                    <div class='ai-highlight-title'>💰 Exposure</div>
                    <div class='ai-highlight-value'>₹{summary['financial_exposure']:,.0f}</div>
                </div>
                <div class='ai-highlight-card'>
                    <div class='ai-highlight-title'>⚠️ Top Risk</div>
                    <div class='ai-highlight-value'>{top_root_cause_label}</div>
                </div>
                <div class='ai-highlight-card'>
                    <div class='ai-highlight-title'>✅ Recoverable</div>
                    <div class='ai-highlight-value'>₹{summary['recoverable_savings']:,.0f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Open AI Narrative", expanded=True):
            st.write(st.session_state["ai_summary"])

        st.download_button(
            "Copy / Download AI Brief",
            data=st.session_state["ai_summary"],
            file_name="ai_executive_brief.txt",
            mime="text/plain",
            key="download_ai_brief"
        )
    else:
        st.info("Click the button above to generate an executive-friendly AI summary.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Vendor risk
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Vendor Risk Index")
    if vendor_risk_df.empty:
        st.info("No vendor risk data available.")
    else:
        top_risk = vendor_risk_df.head(5)
        fig_risk = px.bar(
            top_risk,
            x="vendor",
            y="risk_index",
            color="risk_tier",
            color_discrete_map={
                "High Risk": "#f97373",
                "Medium Risk": "#facc15",
                "Low Risk": "#22c55e",
            },
        )
        fig_risk = style_fig(fig_risk, "Top High-Risk Vendors")
        st.plotly_chart(fig_risk, use_container_width=True)
        st.dataframe(
            top_risk[["vendor", "risk_index", "risk_tier", "total_exposure", "anomaly_count"]]
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Anomaly score
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Anomaly Score Distribution")
    if "iforest_score" in df.columns:
        fig_score = px.histogram(
            df,
            x="iforest_score",
            nbins=40,
            opacity=0.92,
            color_discrete_sequence=["#38bdf8"],
        )
        fig_score = style_fig(fig_score, "Isolation Forest Decision Score Distribution")
        st.plotly_chart(fig_score, use_container_width=True)

        anomaly_count_local = df["iforest_anomaly"].sum()
        total_count = len(df)
        st.write(
            f"Detected {anomaly_count_local} statistical anomalies out of {total_count} transactions ({(anomaly_count_local / total_count) * 100:.2f}%)."
        )
    else:
        st.info("Isolation Forest score not available.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Category distribution
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Category Distribution")
    category_df = df.groupby("category")["amount"].sum().reset_index()
    fig_cat = px.pie(
        category_df,
        names="category",
        values="amount",
        hole=0.55,
        color_discrete_sequence=["#38bdf8", "#22c55e", "#facc15", "#f97373", "#a855f7", "#94a3b8"],
    )
    fig_cat.update_traces(
        hovertemplate="<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>%{percent}",
        textfont=dict(color="#020617")
    )
    fig_cat.update_layout(
        template=PLOTLY_DARK_TEMPLATE,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TITLE_COLOR),
        margin=dict(t=40, b=40, l=20, r=20),
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# PAGE 2 — DETECTED ISSUES
# =====================================================
elif page == "Detected Issues":
    st.markdown(
        "<div class='card header-bar'>"
        "<div class='page-subtitle'>Issue Intelligence</div>"
        "<h1>Detected Issues</h1>"
        "<p>Root-cause clusters, exposures and AI reasoning for every flagged pattern.</p>"
        "<div class='badge-row'><span class='badge badge-warning'>⚠️ Investigation View</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    anomalies = df[df["financial_exposure"] > 0]
    if anomalies.empty:
        st.success("No critical anomalies detected.")
        st.stop()

    grouped = (
        anomalies.groupby("root_cause")
        .agg(exposure=("financial_exposure", "sum"), count=("vendor", "count"))
        .reset_index()
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    fig = px.pie(
        grouped,
        names="root_cause",
        values="exposure",
        hole=0.55,
        color_discrete_sequence=["#38bdf8", "#22c55e", "#facc15", "#f97373", "#a855f7"],
    )
    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Exposure: ₹%{value:,.0f}<extra></extra>",
    )
    fig.update_layout(
        template=PLOTLY_DARK_TEMPLATE,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TITLE_COLOR),
        margin=dict(t=40, b=40, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    for _, row in grouped.iterrows():
        sample_row = anomalies[anomalies["root_cause"] == row["root_cause"]].iloc[0]
        explanation = generate_confidence_timeline(sample_row)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {row['root_cause']}")
        st.write(f"Financial Exposure: ₹{row['exposure']:,.0f}")
        st.write(f"Flagged Transactions: {row['count']}")
        st.write(f"Confidence Level: {explanation['confidence']}%")

        with st.expander("AI Reasoning Timeline"):
            for step in explanation["steps"]:
                st.write(f"- {step}")

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 3 — BUSINESS IMPACT
# =====================================================
elif page == "Business Impact":
    st.markdown(
        "<div class='card header-bar'>"
        "<div class='page-subtitle'>Impact Simulator</div>"
        "<h1>Business Impact</h1>"
        "<p>Translate anomalies into exposure, savings, and vendor concentration.</p>"
        "<div class='badge-row'><span class='badge badge-info'>📈 Exposure Analytics</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    monthly_loss = summary["financial_exposure"] / 12

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Financial Exposure Impact")
    st.write(f"Projected Monthly Exposure: ₹{monthly_loss:,.0f}")
    st.write(f"Annualized Exposure: ₹{summary['financial_exposure']:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    vendor_df = pd.DataFrame(top_vendors_by_exposure(df).items(), columns=["Vendor", "Exposure"])
    fig_bar = px.bar(
        vendor_df,
        x="Vendor",
        y="Exposure",
        color="Exposure",
        color_continuous_scale="Blues",
    )
    fig_bar = style_fig(fig_bar, "Exposure by Vendor")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 4 — EVIDENCE STORY
# =====================================================
elif page == "Evidence Story":
    st.markdown(
        "<div class='card header-bar'>"
        "<div class='page-subtitle'>Vendor Storylines</div>"
        "<h1>Evidence Story</h1>"
        "<p>Timeline of spend for a selected vendor with anomaly context.</p>"
        "<div class='badge-row'><span class='badge badge-info'>🧭 Timeline View</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    df["year_month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    vendor = st.selectbox("Select Vendor", df["vendor"].unique())
    vendor_data = df[df["vendor"] == vendor]
    monthly = vendor_data.groupby("year_month")["amount"].sum().reset_index()

    fig_line = px.line(
        monthly,
        x="year_month",
        y="amount",
        markers=True,
        color_discrete_sequence=["#38bdf8"],
    )
    fig_line.update_traces(marker=dict(size=8))
    fig_line = style_fig(fig_line, f"Spend over time — {vendor}")
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 5 — DUPLICATE EVIDENCE
# =====================================================
elif page == "Duplicate Evidence":
    st.markdown(
        "<div class='card header-bar'>"
        "<div class='page-subtitle'>Leakage Clusters</div>"
        "<h1>Duplicate Evidence</h1>"
        "<p>Clusters of potential duplicate payments and their exposures.</p>"
        "<div class='badge-row'><span class='badge badge-warning'>🧾 Duplicate Review</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    duplicates = df[df["duplicate_flag"] == True]
    if duplicates.empty:
        st.success("No duplicate transactions detected.")
        st.stop()

    grouped = (
        duplicates.groupby(["vendor", "amount"])
        .agg(count=("amount", "count"), exposure=("amount", "sum"))
        .reset_index()
        .sort_values("exposure", ascending=False)
    )

    for _, row in grouped.iterrows():
        cluster = duplicates[
            (duplicates["vendor"] == row["vendor"])
            & (duplicates["amount"] == row["amount"])
        ]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### Vendor: {row['vendor']}")
        st.write(f"Duplicate Amount: ₹{row['amount']:,.2f}")
        st.write(f"Occurrences: {row['count']}")
        st.write(f"Total Duplicate Exposure: ₹{row['exposure']:,.2f}")

        fig_dup = px.scatter(
            cluster,
            x="date",
            y="amount",
            color_discrete_sequence=["#38bdf8"],
        )
        fig_dup = style_fig(fig_dup, "Duplicate Transactions Over Time")
        st.plotly_chart(fig_dup, use_container_width=True)

        with st.expander("View Transactions"):
            st.dataframe(cluster[["date", "vendor", "amount"]])

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 6 — RECOMMENDED ACTIONS
# =====================================================
elif page == "Recommended Actions":
    st.markdown(
        "<div class='card header-bar'>"
        "<div class='page-subtitle'>Playbook</div>"
        "<h1>Recommended Actions</h1>"
        "<p>Root-cause specific interventions with modeled savings impact.</p>"
        "<div class='badge-row'><span class='badge badge-success'>✅ Action Ready</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    grouped = (
        df[df["financial_exposure"] > 0]
        .groupby("root_cause")
        .agg(
            savings=("potential_savings", "sum"),
            action=("recommended_action", "first"),
        )
        .reset_index()
    )

    for idx, row in grouped.iterrows():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {row['root_cause']}")
        st.write(f"Recommended Action: {row['action']}")
        st.write(f"Estimated Recoverable Savings: ₹{row['savings']:,.0f}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="action-ghost">', unsafe_allow_html=True)
            st.button("Notify Finance Team", key=f"notify_{idx}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="action-ghost">', unsafe_allow_html=True)
            st.button("Send Vendor Email", key=f"email_{idx}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="action-ghost">', unsafe_allow_html=True)
            st.button("Schedule Review", key=f"review_{idx}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
