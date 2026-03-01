import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.recommender import SchumacherRecommender


st.set_page_config(page_title="Schumacher AI | Designer Insights", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #e0e0e0; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Schumacher Trade Intelligence Dashboard")
st.markdown("---")

@st.cache_resource
def load_data():
    return SchumacherRecommender(data_path='data/processed/notebooks/final_analytics_data.parquet')

try:
    engine = load_data()
    df = engine.df
except Exception as e:
    st.error(f"Error loading data: {e}. Ensure 'final_analytics_data.parquet' exists in data/processed/")
    st.stop()

st.sidebar.header("🔍 Designer Search")
all_accounts = df['trade_account_id'].unique()
target_account = st.sidebar.selectbox("Select a Trade Account ID", options=all_accounts[:500]) # Sample for speed

if target_account:

    user_data = df[df['trade_account_id'] == target_account].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Segment", user_data['Cluster']) 
    with col2:
        st.metric("Total Net Revenue", f"${user_data['netrevenue']:,.2f}")
    with col3:
        st.metric("Samples Requested", int(user_data['Sample_Count']))
    with col4:
        # Calculate individual conversion rate
        individual_cr = (df[(df['trade_account_id'] == target_account) & (df['type'] == 'SALE')].shape[0] / 
                        max(1, user_data['Sample_Count'])) * 100
        st.metric("Conversion Rate", f"{individual_cr:.1f}%")

    st.markdown("### 🎯 Personalized Recommendations")
    
    recs = engine.recommend_for_account(target_account, top_n=5)
    
    if isinstance(recs, pd.DataFrame) and not recs.empty:
        st.dataframe(recs[['item_number', 'category_name', 'motif']], use_container_width=True)
        
        st.success(f"**Strategy:** This designer is highly active in the **{user_data['Cluster']}** group. "
                "We are recommending trending motifs they haven't purchased yet to expand their project scope.")
    else:
        st.warning("No new recommendations available for this account (they may have already purchased our top-sellers).")

    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("📊 **Purchase Category Mix**")
        cat_counts = df[df['trade_account_id'] == target_account]['category_name'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        cat_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=sns.color_palette("viridis"))
        plt.ylabel("")
        st.pyplot(fig)

    with c2:
        st.write("📈 **Activity Timeline**")
        timeline = df[df['trade_account_id'] == target_account].groupby('year')['netrevenue'].sum()
        st.line_chart(timeline)

else:
    st.info("Please select an Account ID from the sidebar to view the profile and recommendations.")