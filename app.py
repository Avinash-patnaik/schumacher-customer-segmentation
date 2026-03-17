import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from src.recommender import SchumacherRecommender

ICON_PATH = os.path.join(os.getcwd(), "fsco.ico")
st.set_page_config(
    page_title="Schumacher · Intelligence Suite",
    page_icon=ICON_PATH if os.path.exists(ICON_PATH) else "◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

GOLD       = "#C9A84C"
GOLD_LIGHT = "#E8D5A3"
GOLD_DARK  = "#8A6B2E"
GOLD_DIM   = "rgba(201,168,76,0.12)"
OBSIDIAN   = "#060608"
CARBON     = "#0E0E10"
GRAPHITE   = "#161618"
SLATE      = "#202024"
GHOST      = "#2A2A30"
BORDER     = "#323238"
MUTED      = "#72706E"
SOFT       = "#9A9896"

SERIF    = "'Cormorant Garamond', Georgia, serif"
BRAND    = "'Bodoni Moda', 'Didact Gothic', Georgia, serif"
DISPLAY  = "'Playfair Display', 'Libre Baskerville', Georgia, serif"
MONO     = "'DM Mono', 'Courier New', monospace"
SANS     = "'Inter', 'DM Sans', system-ui, sans-serif"

PLOT_FONT  = dict(family=SERIF,  color=GOLD_LIGHT, size=14)
TICK_FONT  = dict(family=MONO,   color=SOFT,       size=11)
HOVER_BG   = dict(bgcolor=GRAPHITE, font=dict(family=MONO, color=GOLD_LIGHT, size=12), bordercolor=GOLD_DARK)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;0,6..96,700;0,6..96,900;1,6..96,400;1,6..96,700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400;1,700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>

:root {{
    --gold:       {GOLD};
    --gold-light: {GOLD_LIGHT};
    --gold-dark:  {GOLD_DARK};
    --gold-dim:   {GOLD_DIM};
    --obsidian:   {OBSIDIAN};
    --carbon:     {CARBON};
    --graphite:   {GRAPHITE};
    --slate:      {SLATE};
    --ghost:      {GHOST};
    --border:     {BORDER};
    --muted:      {MUTED};
    --soft:       {SOFT};
    --serif:      {SERIF};
    --brand:      {BRAND};
    --display:    {DISPLAY};
    --sans:       {SANS};
    --mono:       {MONO};
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}

html {{ font-size: 16px; }}

.stApp {{
    background: var(--obsidian) !important;
    color: var(--gold-light) !important;
    font-family: var(--sans) !important;
    font-size: 1rem !important;
}}

#MainMenu, footer, header[data-testid="stHeader"],
.stDeployButton, [data-testid="stToolbar"] {{ display: none !important; }}

.block-container {{
    padding: 2rem 2.5rem 6rem !important;
    max-width: 1600px !important;
}}

[data-testid="stSidebar"] {{
    background: var(--carbon) !important;
    border-right: 1px solid var(--ghost) !important;
    min-width: 280px !important;
    max-width: 280px !important;
}}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 0 !important; }}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {{
    color: var(--soft) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: var(--ghost) !important;
    margin: 1.25rem 0 !important;
}}

div[data-baseweb="select"] > div {{
    background: var(--slate) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    min-height: 44px !important;
}}
div[data-baseweb="select"] * {{
    color: var(--gold-light) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    background: var(--slate) !important;
    letter-spacing: 0.05em !important;
}}
[data-baseweb="popover"] {{ background: var(--slate) !important; border: 1px solid var(--border) !important; }}
[data-baseweb="menu"] {{ background: var(--slate) !important; }}
[role="option"] {{ padding: 10px 14px !important; font-size: 0.82rem !important; }}
[role="option"]:hover {{ background: var(--ghost) !important; }}

div[data-testid="stMetric"] {{
    background: var(--graphite) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 28px 26px 24px !important;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}}
div[data-testid="stMetric"]:hover {{
    border-color: var(--gold-dark) !important;
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 0 1px var(--gold-dark);
}}
div[data-testid="stMetric"]::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at top left, rgba(201,168,76,0.06), transparent 65%);
    pointer-events: none;
}}
div[data-testid="stMetricLabel"] * {{
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
}}
div[data-testid="stMetricValue"] > div {{
    color: var(--gold-light) !important;
    font-family: var(--serif) !important;
    font-weight: 600 !important;
    font-size: 2.6rem !important;
    line-height: 1.1 !important;
    letter-spacing: 0.01em !important;
    margin-top: 6px !important;
}}
div[data-testid="stMetricDelta"] > div {{
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    margin-top: 4px !important;
}}

h1, h2, h3, h4 {{
    font-family: var(--serif) !important;
    color: var(--gold-light) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}}

[data-testid="stExpander"] {{
    background: var(--graphite) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden;
}}
[data-testid="stExpander"] summary {{
    color: var(--soft) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 16px 20px !important;
}}
[data-testid="stExpander"] summary:hover {{
    color: var(--gold-light) !important;
    background: var(--slate) !important;
}}

[data-testid="stDataFrame"] {{
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
}}

::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: var(--carbon); }}
::-webkit-scrollbar-thumb {{ background: var(--gold-dark); border-radius: 4px; }}

.section-header {{
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 48px 0 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--ghost);
}}
.section-number {{
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--gold-dark);
    letter-spacing: 0.2em;
    background: var(--gold-dim);
    padding: 4px 10px;
    border-radius: 4px;
    border: 1px solid var(--gold-dark);
    white-space: nowrap;
}}
.section-title {{
    font-family: var(--serif);
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--gold-light);
    letter-spacing: 0.04em;
}}

.chart-card {{
    background: var(--graphite);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 22px 16px;
    position: relative;
    overflow: hidden;
}}
.chart-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold-dark) 0%, transparent 70%);
}}
.chart-title {{
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 16px;
    display: block;
}}

.rec-card {{
    background: var(--graphite);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 26px 24px;
    height: 100%;
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}}
.rec-card:hover {{
    border-color: var(--gold-dark);
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5), 0 0 0 1px var(--gold-dark);
}}
.rec-card::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold) 0%, transparent 60%);
}}

.kpi-badge {{
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    background: var(--gold-dim);
    color: var(--gold);
    border: 1px solid var(--gold-dark);
    border-radius: 20px;
    padding: 4px 12px;
}}

.empty-state {{
    padding: 60px 40px;
    text-align: center;
    background: var(--graphite);
    border: 1px dashed var(--border);
    border-radius: 12px;
}}
.empty-state-text {{
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}}

#main-heading {{
    font-family: 'Playfair Display', 'Georgia', serif !important;
    font-size: clamp(4rem, 9vw, 8rem) !important;
    font-weight: 900 !important;
    color: {GOLD_LIGHT} !important;
    line-height: 0.9 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 24px !important;
    text-shadow: 0 4px 40px rgba(201,168,76,0.2) !important;
    display: block !important;
}}

#brand-eyebrow {{
    font-family: 'Bodoni Moda', 'Didact Gothic', 'Georgia', serif !important;
    font-size: 1.05rem !important;
    font-weight: 400 !important;
    font-style: italic !important;
    color: {GOLD} !important;
    letter-spacing: 0.24em !important;
    margin-bottom: 20px !important;
    display: block !important;
}}
</style>
""", unsafe_allow_html=True)


def section_header(number: str, title: str):
    st.markdown(f"""
    <div class="section-header">
        <span class="section-number">{number}</span>
        <span class="section-title">{title}</span>
    </div>""", unsafe_allow_html=True)


@st.cache_resource
def load_engine():
    return SchumacherRecommender(
        data_path='data/processed/notebooks/final_analytics_data.parquet'
    )

try:
    engine = load_engine()
    df = engine.df
except Exception as e:
    st.error(f"**System Offline** — {e}")
    st.stop()


with st.sidebar:
    try:
        brand_logo = Image.open("fsco.jpeg")
        st.image(brand_logo, use_container_width=True)
    except:
        st.markdown(f"""
        <div style='padding:40px 24px 28px; text-align:center; border-bottom:1px solid {GHOST};'>
            <div style='font-family:{BRAND}; font-size:1.55rem; font-weight:700;
                        color:{GOLD}; letter-spacing:0.32em; line-height:1.1;
                        text-transform:uppercase; font-style:normal;'>
                Schumacher
            </div>
            <div style='font-family:{BRAND}; font-size:0.72rem; color:{MUTED};
                        letter-spacing:0.22em; margin-top:10px; font-weight:400;
                        font-style:italic; text-transform:none;'>
                F. Schumacher &amp; Co.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='padding:24px 24px 12px;'>
        <div style='font-family:{MONO}; font-size:0.65rem; color:{MUTED};
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:12px;'>
            Intelligence Suite · 2025
        </div>
    </div>""", unsafe_allow_html=True)

    target_account = st.selectbox(
        "DESIGNER ACCOUNT",
        options=sorted(df['trade_account_id'].unique()),
        label_visibility="visible",
    )

    st.markdown("---")

    total_accounts = df['trade_account_id'].nunique()
    total_revenue  = df['netrevenue'].sum()
    total_clusters = df['Cluster'].nunique()

    for stat_label, stat_val in [
        ("Active Accounts",   f"{total_accounts:,}"),
        ("Portfolio Revenue", f"${total_revenue:,.0f}"),
        ("Account Tiers",     str(total_clusters)),
    ]:
        st.markdown(f"""
        <div style='padding:0 24px 20px;'>
            <div style='font-family:{MONO}; font-size:0.68rem; color:{MUTED};
                        letter-spacing:0.14em; text-transform:uppercase; margin-bottom:4px;'>
                {stat_label}
            </div>
            <div style='font-family:{SERIF}; font-size:1.6rem; color:{GOLD_LIGHT};
                        font-weight:600; line-height:1.1;'>
                {stat_val}
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='padding:20px 24px 0; margin-top:8px; border-top:1px solid {GHOST};'>
        <div style='font-family:{BRAND}; font-size:0.72rem; font-style:italic;
                    color:{MUTED}; letter-spacing:0.1em; line-height:2;'>
            F. Schumacher &amp; Co.<br>
            <span style='font-family:{MONO}; font-size:0.6rem; font-style:normal;
                         letter-spacing:0.16em; text-transform:uppercase;'>
                Trade Intelligence Platform<br>© 2025 · Confidential
            </span>
        </div>
    </div>""", unsafe_allow_html=True)


if not target_account:
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; align-items:center;
                justify-content:center; height:72vh; gap:16px;'>
        <div style='font-family:{BRAND}; font-size:0.9rem; font-weight:400;
                    font-style:italic; color:{GOLD_DARK}; letter-spacing:0.2em;
                    margin-bottom:4px;'>
            F. Schumacher &amp; Co.
        </div>
        <div style='font-family:{SERIF}; font-size:5.5rem; font-weight:300;
                    color:{GHOST}; letter-spacing:0.5em; line-height:1;'>
            SCHUMACHER
        </div>
        <div style='font-family:{MONO}; font-size:0.82rem; color:{MUTED};
                    letter-spacing:0.28em; text-transform:uppercase; margin-top:8px;'>
            Select an account from the sidebar to begin
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

account_df = df[df['trade_account_id'] == target_account].copy()
if account_df.empty:
    st.warning("No data found for this account.")
    st.stop()

total_ltv       = account_df['netrevenue'].sum()
segment         = account_df['Cluster'].iloc[0]
type_col        = account_df['type'].astype(str).str.upper().str.strip()
total_samples   = int((type_col == 'SAMPLE').sum())
total_sales     = int((type_col == 'SALE').sum())
conv_rate       = (total_sales / max(1, total_samples)) * 100.0
avg_order       = account_df.loc[type_col == 'SALE', 'netrevenue'].mean()
avg_order       = avg_order if pd.notna(avg_order) else 0.0
cluster_avg_rev = df[df['Cluster'] == segment]['netrevenue'].mean()
revenue_delta   = ((total_ltv - cluster_avg_rev) / max(1, cluster_avg_rev)) * 100
delta_sign      = "▲" if revenue_delta >= 0 else "▼"


st.markdown(f"""
<div style='text-align:center; padding: 44px 0 36px;
            border-bottom:1px solid {GHOST}; margin-bottom:36px;'>
    <span id="brand-eyebrow">F. Schumacher &amp; Co.</span>
    <span id="main-heading">Designer Profile</span>
    <div style='display:flex; align-items:center; justify-content:center;
                gap:16px; flex-wrap:wrap; margin-top:6px;'>
        <span class="kpi-badge">Tier · {segment}</span>
        <span style='font-family:{MONO}; font-size:0.82rem; color:{SOFT};
                     letter-spacing:0.1em;'>
            {delta_sign} {abs(revenue_delta):.1f}% vs cluster average
        </span>
        <span style='font-family:{MONO}; font-size:0.82rem; color:{MUTED};
                     letter-spacing:0.08em;'>
            ID: {target_account}
        </span>
    </div>
</div>""", unsafe_allow_html=True)


k1, k2, k3, k4, k5 = st.columns(5, gap="medium")
k1.metric("Account Tier",    segment)
k2.metric("2025 Revenue",    f"${total_ltv:,.0f}",
          delta=f"{delta_sign} {abs(revenue_delta):.1f}% vs cluster")
k3.metric("Sample Volume",   f"{total_samples:,}")
k4.metric("Sales Converted", f"{total_sales:,}")
k5.metric("Conversion Rate", f"{conv_rate:.1f}%",
          delta=f"{total_sales} of {total_samples} samples",
          delta_color="off")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)


section_header("01", "Performance Analysis")

col_left, col_right = st.columns([1.2, 0.8], gap="large")

with col_left:
    st.markdown('<div class="chart-card"><span class="chart-title">Category Affinity · Transaction Distribution</span>',
                unsafe_allow_html=True)

    cat_counts = account_df['category_name'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Count']

    fig_bar = go.Figure(go.Bar(
        x=cat_counts['Count'],
        y=cat_counts['Category'],
        orientation='h',
        marker=dict(
            color=cat_counts['Count'],
            colorscale=[[0, SLATE], [0.35, GOLD_DARK], [1, GOLD]],
            line=dict(width=0),
        ),
        text=cat_counts['Count'],
        textposition='outside',
        textfont=dict(family=MONO, color=SOFT, size=12),
        hovertemplate='<b style="font-family:' + SERIF + '; font-size:15px;">%{y}</b><br>'
                      '<span style="font-family:' + MONO + ';">%{x} transactions</span>'
                      '<extra></extra>',
    ))
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=360,
        margin=dict(l=0, r=60, t=8, b=8),
        font=PLOT_FONT,
        xaxis=dict(
            showgrid=True, gridcolor=GHOST, gridwidth=1,
            zeroline=False, tickfont=TICK_FONT, color=SOFT,
            title=dict(text="Transaction Count", font=dict(family=MONO, color=MUTED, size=12)),
        ),
        yaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(family=SERIF, color=GOLD_LIGHT, size=14),
            color=GOLD_LIGHT,
        ),
        bargap=0.36,
        hoverlabel=HOVER_BG,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-card"><span class="chart-title">Revenue Benchmark · vs Cluster Average</span>',
                unsafe_allow_html=True)

    gauge_max = max(total_ltv, cluster_avg_rev) * 1.3

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_ltv,
        delta=dict(
            reference=cluster_avg_rev,
            increasing=dict(color=GOLD),
            decreasing=dict(color="#E05555"),
            font=dict(family=MONO, size=14, color=GOLD_LIGHT),
            valueformat="$,.0f",
        ),
        number=dict(
            prefix="$",
            font=dict(family=SERIF, size=44, color=GOLD_LIGHT),
            valueformat=",.0f",
        ),
        title=dict(
            text=(
                f"<span style='font-family:{MONO}; font-size:11px; "
                f"letter-spacing:2px; color:{MUTED};'>ACCOUNT REVENUE</span>"
            ),
            font=dict(family=SERIF, color=GOLD_LIGHT, size=14),
        ),
        gauge=dict(
            axis=dict(
                range=[0, gauge_max],
                tickcolor=BORDER,
                tickfont=dict(family=MONO, size=10, color=MUTED),
                nticks=5,
            ),
            bar=dict(color=GOLD, thickness=0.22),
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0,
            steps=[
                dict(range=[0, cluster_avg_rev * 0.5],               color=SLATE),
                dict(range=[cluster_avg_rev * 0.5, cluster_avg_rev],  color=GHOST),
                dict(range=[cluster_avg_rev, gauge_max],              color="#18160E"),
            ],
            threshold=dict(
                line=dict(color=GOLD_LIGHT, width=2),
                thickness=0.82,
                value=cluster_avg_rev,
            ),
        ),
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=PLOT_FONT,
        height=360,
        margin=dict(l=20, r=20, t=44, b=10),
        hoverlabel=HOVER_BG,
        annotations=[dict(
            x=0.5, y=-0.04,
            text=(
                f"<span style='font-family:{MONO}; font-size:10px; "
                f"color:{MUTED}; letter-spacing:2px;'>"
                f"CLUSTER AVG  ${cluster_avg_rev:,.0f}</span>"
            ),
            showarrow=False,
            xref="paper", yref="paper",
            font=dict(family=MONO, size=10, color=MUTED),
        )],
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)


section_header("02", "Conversion & Revenue Flow")

has_timeline = 'shipped_dt' in account_df.columns
fcol, tcol = st.columns([0.72, 1.28] if has_timeline else [1, 1], gap="large")

with fcol:
    st.markdown('<div class="chart-card"><span class="chart-title">Sample → Sale Conversion Funnel</span>',
                unsafe_allow_html=True)

    fig_funnel = go.Figure(go.Funnel(
        y=['Samples<br>Issued', 'Sales<br>Converted'],
        x=[total_samples, total_sales],
        textposition='inside',
        textinfo='value+percent initial',
        textfont=dict(family=SERIF, color=OBSIDIAN, size=17),
        insidetextfont=dict(family=SERIF, color=OBSIDIAN, size=17),
        outsidetextfont=dict(family=MONO, color=GOLD_LIGHT, size=13),
        constraintext='inside',
        marker=dict(
            color=[SLATE, GOLD],
            line=dict(color=[BORDER, GOLD_DARK], width=1),
        ),
        connector=dict(
            line=dict(color=GHOST, width=1, dash='dot'),
            fillcolor=GRAPHITE,
        ),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Count: <b>%{x}</b><br>'
            'Rate: <b>%{percentInitial:.1%}</b>'
            '<extra></extra>'
        ),
    ))
    fig_funnel.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        margin=dict(l=0, r=0, t=8, b=8),
        font=PLOT_FONT,
        hoverlabel=HOVER_BG,
        yaxis=dict(tickfont=dict(family=SERIF, color=GOLD_LIGHT, size=14)),
    )
    st.plotly_chart(fig_funnel, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with tcol:
    st.markdown('<div class="chart-card"><span class="chart-title">Monthly Revenue Timeline · Sales Only</span>',
                unsafe_allow_html=True)

    if has_timeline:
        timeline_df = (
            account_df[type_col == 'SALE'].copy()
            .assign(shipped_dt=lambda x: pd.to_datetime(x['shipped_dt']))
            .groupby(pd.Grouper(key='shipped_dt', freq='ME'))['netrevenue']
            .sum()
            .reset_index()
        )

        if not timeline_df.empty and timeline_df['netrevenue'].sum() > 0:
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=timeline_df['shipped_dt'],
                y=timeline_df['netrevenue'],
                fill='tozeroy',
                mode='lines+markers',
                name='Net Revenue',
                line=dict(color=GOLD, width=2.5),
                fillcolor='rgba(201,168,76,0.08)',
                marker=dict(size=7, color=GOLD, symbol='circle',
                            line=dict(color=GOLD_DARK, width=1.5)),
                hovertemplate=(
                    '<span style="font-family:' + MONO + '; font-size:11px; color:' + SOFT + ';">%{x|%b %Y}</span><br>'
                    '<b style="font-family:' + SERIF + '; font-size:16px; color:' + GOLD + ';">$%{y:,.0f}</b>'
                    '<extra></extra>'
                ),
            ))
            if avg_order > 0:
                fig_area.add_hline(
                    y=avg_order,
                    line_dash="dot",
                    line_color=BORDER,
                    line_width=1.5,
                    annotation_text=f"Avg ${avg_order:,.0f}",
                    annotation_font=dict(family=MONO, size=11, color=MUTED),
                    annotation_position="top right",
                )
            fig_area.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=320,
                margin=dict(l=0, r=24, t=8, b=8),
                font=PLOT_FONT,
                xaxis=dict(
                    showgrid=False, zeroline=False,
                    tickfont=TICK_FONT, color=SOFT,
                    tickformat="%b '%y",
                    title=dict(text="Month", font=dict(family=MONO, color=MUTED, size=12)),
                ),
                yaxis=dict(
                    showgrid=True, gridcolor=GHOST, gridwidth=1,
                    zeroline=False, tickprefix='$',
                    tickfont=TICK_FONT, color=SOFT,
                    title=dict(text="Net Revenue", font=dict(family=MONO, color=MUTED, size=12)),
                ),
                hovermode='x unified',
                hoverlabel=HOVER_BG,
                showlegend=False,
            )
            st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown(f"""
            <div class="empty-state" style='height:290px; display:flex;
                        align-items:center; justify-content:center;'>
                <span class="empty-state-text">No Sales Transactions on Record</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="empty-state" style='height:290px; display:flex;
                    align-items:center; justify-content:center;'>
            <span class="empty-state-text">Date Column Unavailable</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


section_header("03", "Curated Selections")

recs = engine.recommend_for_account(target_account, top_n=3)

if recs is not None and not recs.empty:
    r1, r2, r3 = st.columns(3, gap="large")
    numerals = ['I', 'II', 'III']

    for i, rec in enumerate(recs.itertuples()):
        with [r1, r2, r3][i]:
            st.markdown(f"""
            <div class="rec-card">
                <div style='display:flex; justify-content:space-between;
                            align-items:flex-start; margin-bottom:16px;'>
                    <span style='font-family:{MONO}; font-size:0.7rem; letter-spacing:0.18em;
                                 color:{MUTED}; text-transform:uppercase;'>
                        {rec.category_name}
                    </span>
                    <span style='font-family:{SERIF}; font-size:1.8rem;
                                 color:{GHOST}; font-weight:600; line-height:1;'>
                        {numerals[i]}
                    </span>
                </div>
                <div style='font-family:{SERIF}; font-size:1.5rem; font-weight:600;
                            color:{GOLD_LIGHT}; line-height:1.3; letter-spacing:0.02em;
                            margin-bottom:24px;'>
                    {rec.motif}
                </div>
                <div style='border-top:1px solid {GHOST}; padding-top:16px;
                            display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-family:{MONO}; font-size:0.7rem;
                                 color:{MUTED}; letter-spacing:0.14em; text-transform:uppercase;'>
                        SKU
                    </span>
                    <span style='font-family:{MONO}; font-size:0.82rem;
                                 color:{GOLD}; letter-spacing:0.1em; font-weight:500;'>
                        {rec.item_number}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="empty-state">
        <span class="empty-state-text">Insufficient Purchase History for Recommendations</span>
    </div>""", unsafe_allow_html=True)


section_header("04", "Transaction Ledger")

with st.expander("View Recent Transactions", expanded=False):
    display_cols = [c for c in
                    ['shipped_dt', 'type', 'category_name',
                     'item_number', 'motif', 'netrevenue']
                    if c in account_df.columns]

    recent = (
        account_df[display_cols]
        .sort_values('shipped_dt', ascending=False)
        .head(30)
        .rename(columns={
            'shipped_dt':    'Date',
            'type':          'Type',
            'category_name': 'Category',
            'item_number':   'SKU',
            'motif':         'Design',
            'netrevenue':    'Net Revenue',
        })
    )
    if 'Net Revenue' in recent.columns:
        recent['Net Revenue'] = recent['Net Revenue'].apply(
            lambda x: f"${x:,.0f}" if pd.notna(x) else '—'
        )
    st.dataframe(recent, use_container_width=True, hide_index=True)


st.markdown(f"""
<div style='margin-top:72px; padding:24px 0; border-top:1px solid {GHOST};
            display:flex; justify-content:space-between; align-items:center;'>
    <div style='font-family:{BRAND}; font-size:0.78rem; font-style:italic;
                color:{MUTED}; letter-spacing:0.1em;'>
        F. Schumacher &amp; Co. &nbsp;·&nbsp; Intelligence Suite &nbsp;·&nbsp; 2025
    </div>
    <div style='font-family:{MONO}; font-size:0.7rem; color:{MUTED}; letter-spacing:0.14em;'>
        CONFIDENTIAL &nbsp;·&nbsp; TRADE USE ONLY
    </div>
</div>""", unsafe_allow_html=True)