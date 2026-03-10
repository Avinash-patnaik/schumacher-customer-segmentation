import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from src.recommender import SchumacherRecommender

# Page Configuration
ICON_PATH = os.path.join(os.getcwd(), "fsco.ico")
st.set_page_config(
    page_title="Intelligence Suite", 
    page_icon=ICON_PATH if os.path.exists(ICON_PATH) else "📧", 
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500&family=Montserrat:wght@300;400;600&display=swap');

    header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    .stApp {
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94)), 
                        url('https://www.transparenttextures.com/patterns/linen.png');
        background-attachment: fixed;
    }

    /* Global Typography */
    .main, p, span, label, [data-testid="stMetricLabel"] > label { 
        font-family: 'Montserrat', sans-serif !important; 
        color: #000000 !important; 
        letter-spacing: 0.05em;
    }

    /* CENTER HEADLINE - MAXIMUM SIZE & PRESTIGE */
    .headline-style {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 700 !important;
        color: #000000 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6em !important; 
        font-size: 3rem !important;    /* SIGNIFICANTLY INCREASED SIZE */
        margin-bottom: 0px !important;
        text-align: center !important;
        padding-top: 10px !important;
        line-height: 1.0 !important;
        display: block !important;
    }

    h2, h3, h4 { 
        font-family: 'Cormorant Garamond', serif !important; 
        font-weight: 700 !important; 
        color: #000000 !important;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    /* BRUSHED GOLD METRIC CONTAINERS */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #d4af37 0%, #f1d592 45%, #b4975a 100%) !important;
        border: 1px solid #9c7e41 !important;
        padding: 30px !important;
        border-radius: 0px !important; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    div[data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }

    /* SIDEBAR - GOLD FONT COLOR */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
    }

    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #B4975A !important; 
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    div[data-baseweb="select"] > div {
        background-color: #B4975A !important;
        border: 1px solid #8A6D3B !important;
        border-radius: 0px !important;
    }

    div[data-baseweb="select"] * {
        color: #000000 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
    }

    .rec-card {
        background: white;
        padding: 30px;
        border: 1px solid #EAEAEA;
        border-bottom: 6px solid #B4975A;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_engine():
    return SchumacherRecommender(data_path='data/processed/notebooks/final_analytics_data.parquet')

try:
    engine = load_engine()
    df = engine.df
except Exception as e:
    st.error(f"System Offline: {e}")
    st.stop()


try:
    brand_logo = Image.open("fsco.jpeg")
    st.sidebar.image(brand_logo, use_container_width=True)
except:
    st.sidebar.markdown("<h2 style='color:#B4975A; letter-spacing:5px;'>SCHUMACHER</h2>", unsafe_allow_html=True)

st.sidebar.markdown("""
    <p style='color: #B4975A; font-family: "Montserrat", sans-serif; font-size: 0.8rem; font-weight: 600; letter-spacing: 3px; margin-bottom: -15px; margin-top: 20px;'>
        DESIGNER ACCOUNT
    </p>""", unsafe_allow_html=True)

st.sidebar.markdown("---")
target_account = st.sidebar.selectbox("SELECT ID", options=df['trade_account_id'].unique(), label_visibility="collapsed")


if target_account:
    account_df = df[df['trade_account_id'] == target_account].copy()
    
    if not account_df.empty:
        total_ltv = account_df['netrevenue'].sum()
        total_samples = float(account_df['Sample_Count'].sum())
        segment = account_df['Cluster'].iloc[0]
        
        st.markdown('<p class="headline-style">Schumacher Intelligence</p>', unsafe_allow_html=True)
        st.markdown(f"<p style='font-style: italic; color:#444; text-align:center; letter-spacing: 2px; margin-bottom:40px;'>2025 Trade Analytics Suite | Account: {target_account}</p>", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Account Tier", segment)
        m2.metric("2025 Revenue", f"${total_ltv:,.0f}")
        m3.metric("Sample Volume", int(total_samples))
        

        sales_count = account_df[account_df['type'].astype(str).str.upper().str.strip() == 'SALE'].shape[0]
        conv_rate = (float(sales_count) / max(1.0, total_samples)) * 100.0
        m4.metric("Conversion Rate", f"{conv_rate:.1f}%")

        st.markdown("<br><h3>Curated Selections</h3>", unsafe_allow_html=True)
        recs = engine.recommend_for_account(target_account, top_n=3)

        if recs is not None and not recs.empty:
            cols = st.columns(3)
            for i, rec in enumerate(recs.itertuples()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="rec-card">
                        <p style='color:#B4975A; font-weight:600; font-size: 0.7rem; letter-spacing:3px;'>{rec.category_name.upper()}</p>
                        <h4 style='margin:10px 0; text-transform: none; letter-spacing:1px;'>{rec.motif}</h4>
                        <p style='font-size: 0.75rem; border-top: 1px solid #EEE; padding-top:10px;'>SKU: {rec.item_number}</p>
                    </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Category Affinity")
            st.bar_chart(account_df['category_name'].value_counts(), color="#B4975A")
            
        with c2:
            st.subheader("2025 Benchmark")
            avg_revenue = df[df['Cluster'] == segment]['netrevenue'].mean()
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = total_ltv,
                title = {
                    'text': "Revenue vs Cluster Avg", 
                    'font': {'family': "Montserrat", 'size': 18} 
                },
                delta = {
                    'reference': avg_revenue, 
                    'increasing': {'color': "#B4975A"},
                    'font': {'size': 18} 
                },
                gauge = {
                    'axis': {
                        'range': [None, max(total_ltv, avg_revenue) * 1.2], 
                        'tickcolor': "black",
                        'tickfont': {'size': 12}
                    },
                    'bar': {'color': "#B4975A"},
                    'bgcolor': "rgba(255,255,255,0.5)",
                    'threshold': {
                        'line': {'color': "black", 'width': 4}, 
                        'thickness': 0.8, 
                        'value': avg_revenue
                    }
                },
                number = {'font': {'size': 45}, 'prefix': "$"} 
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                font={'color': "black", 'family': "Cormorant Garamond"}, 
                height=400, 
                margin=dict(l=30, r=30, t=40, b=20) 
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data found for this account ID.")
else:
    st.title("SCHUMACHER")
    st.markdown("### Initialize Intelligence via Account Selection.")