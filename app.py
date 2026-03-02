import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from src.recommender import SchumacherRecommender

# --- Page Configuration ---
st.set_page_config(page_title="Schumacher | Intelligence Suite", layout="wide")

# --- Luxury Aesthetic CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500&family=Montserrat:wght@300;400;600&display=swap');

    header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stApp {
        background-image: linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94)), 
                          url('https://www.transparenttextures.com/patterns/linen.png');
        background-attachment: fixed;
    }
    .main, p, span, label, [data-testid="stMetricLabel"] > label { 
        font-family: 'Montserrat', sans-serif !important; 
        color: #000000 !important; 
    }
    h1, h2, h3, h4 { 
        font-family: 'Cormorant Garamond', serif !important; 
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #000000 !important;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #d4af37 0%, #f1d592 45%, #b4975a 100%) !important;
        border: 1px solid #9c7e41 !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] label { color: #B4975A !important; text-transform: uppercase; font-weight: 600; }
    div[data-baseweb="select"] > div { background-color: #B4975A !important; border: 0px; }
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
    # Sourcing optimized data from the structure [cite: 1, 4]
    return SchumacherRecommender(data_path='data/processed/notebooks/final_analytics_data.parquet')

try:
    engine = load_engine()
    df = engine.df
except Exception as e:
    st.error(f"Engine Load Error: {e}")
    st.stop()

# --- Sidebar ---
try:
    brand_logo = Image.open("fsco.jpeg") 
    st.sidebar.image(brand_logo, use_container_width=True)
except:
    st.sidebar.markdown("<h2 style='color:#B4975A;'>SCHUMACHER</h2>", unsafe_allow_html=True)

target_account = st.sidebar.selectbox("DESIGNER ACCOUNT ID", options=df['trade_account_id'].unique())

# --- Main Dashboard ---
if target_account:
    account_df = df[df['trade_account_id'] == target_account].copy()
    
    if not account_df.empty:
        total_ltv = account_df['netrevenue'].sum()
        # Ensure we aggregate samples correctly 
        total_samples = float(account_df['Sample_Count'].sum())
        segment = account_df['Cluster'].iloc[0] 
        
        st.title("SCHUMACHER INTELLIGENCE")
        st.markdown(f"**Account Analysis:** {target_account}")
        st.markdown("---")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tier", segment)
        m2.metric("LTV", f"${total_ltv:,.0f}")
        m3.metric("Samples", int(total_samples))
        
        # Fixed Case-Insensitive Conversion Logic
        sales_count = account_df[account_df['type'].astype(str).str.upper().str.strip() == 'SALE'].shape[0]
        conv_rate = (float(sales_count) / max(1.0, total_samples)) * 100.0
        m4.metric("Conversion", f"{conv_rate:.1f}%")

        # --- Recommender Section ---
        st.markdown("<br><h3>Tailored Recommendations</h3>", unsafe_allow_html=True)
        st.caption("Based on historical purchase patterns and category affinity")
        
        # engine.recommend_for_account pulls from your src/recommender.py logic 
        recs = engine.recommend_for_account(target_account, top_n=3)

        if recs is not None and not recs.empty:
            cols = st.columns(3)
            for i, rec in enumerate(recs.itertuples()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="rec-card">
                        <p style='color:#B4975A; font-weight:600; font-size: 0.7rem;'>{rec.category_name.upper()}</p>
                        <h4 style='margin:10px 0;'>{rec.motif}</h4>
                        <p style='font-size: 0.75rem; border-top: 1px solid #EEE; padding-top:10px;'>SKU: {rec.item_number}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No specific recommendations found. Suggesting trending motifs.")

        # Visuals
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Category Affinity")
            st.bar_chart(account_df['category_name'].value_counts(), color="#B4975A")
        with c2:
            st.subheader("Revenue History")
            timeline = account_df.groupby('year')['netrevenue'].sum().reset_index()
            fig = go.Figure(go.Scatter(x=timeline['year'], y=timeline['netrevenue'], mode='lines+markers', line=dict(color='#B4975A', width=4)))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select a Designer Account ID to begin.")