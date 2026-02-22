import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="CyberSphere Security", layout="wide", page_icon="🛡️")

# 2. Modern Blue & White Styling
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    
    /* Custom Header */
    .header-container {
        background: linear-gradient(90deg, #003366 0%, #007BFF 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        text-align: left;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #F0F7FF;
        border: 1px solid #CCE5FF;
        padding: 15px;
        border-radius: 10px;
        color: #003366;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #003366;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    
    h1, h2, h3 { color: #003366 !important; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('''
    <div class="header-container">
        <h1 style="color: white !important; margin:0;">CYBERSPHERE MONITORING</h1>
        <p style="opacity: 0.8;">Real-time Threat Intelligence & Security Audit</p>
    </div>
    ''', unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    # This ensures it looks in the same folder as app.py
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "dataset2_threat_detection.csv")
    
    try:
        df = pd.read_csv(file_path)
        # Check if the column exists before converting
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        # This will tell us the REAL error (e.g., a missing column or path issue)
        st.error(f"Error details: {e}")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🕹️ Control Center")
    severity_choice = st.sidebar.multiselect("Filter Severity", options=df['severity'].unique(), default=df['severity'].unique())
    system_choice = st.sidebar.selectbox("Network Segment", options=["All Segments"] + list(df['affected_system'].unique()))
    
    # --- FILTERING LOGIC ---
    filt_df = df[df['severity'].isin(severity_choice)]
    if system_choice != "All Segments":
        filt_df = filt_df[filt_df['affected_system'] == system_choice]

    # --- TOP KPI ROW ---
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.metric("Active Alerts", len(filt_df))
    with k2:
        critical_count = len(filt_df[filt_df['severity'] == 'Critical'])
        st.metric("Critical Threats", critical_count, delta="-2% vs Yesterday", delta_color="inverse")
    with k3:
        st.metric("System Health", "98.2%", delta="Optimal")
    with k4:
        st.metric("Avg Resp Time", f"{filt_df['response_time_minutes'].mean():.1f}m")

    st.write("---")

    # --- ANALYTICS ROW ---
    col_left, col_right = st.columns([1.2, 0.8])

    with col_left:
        st.subheader("📈 Threat Velocity (Hourly)")
        line_data = filt_df.groupby('hour').size().reset_index(name='Incidents')
        fig_line = px.line(line_data, x='hour', y='Incidents', 
                          markers=True,
                          color_discrete_sequence=['#007BFF'])
        fig_line.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("🎯 Attack Vectors")
        fig_pie = px.pie(filt_df, names='threat_type', 
                        color_discrete_sequence=['#003366', '#005BB5', '#007BFF', '#66B2FF'])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- DATA EXPLORER ---
    st.subheader("📑 Event Investigation Log")
    
    # Add a search bar for the table
    search = st.text_input("Search for specific IP or signature...")
    if search:
        display_df = filt_df[filt_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    else:
        display_df = filt_df

    st.dataframe(display_df, use_container_width=True)

        # Dynamic conclusion text based on data
    if len(filt_df) > 0:
        top_threat = filt_df['threat_type'].value_counts().idxmax()
        st.info(f"**Automated Summary:** The primary threat vector currently identified is **{top_threat}**. We recommend immediate audit of logs associated with this activity.")
    else:
        st.warning("No incidents match the selected filters. System appears clear.")


    # --- FOOTER ---
    current_year = datetime.date.today().year
    st.markdown(f"""
        <div style="margin-top: 50px; padding: 20px; border-top: 1px solid #EEE; text-align: center; color: #666;">
            <b>ASHU MARY GLADYS</b> | Masters of Technology | {current_year} <br>
            <small>Confidential Security Report - Authorized Personnel Only</small>
        </div>
        """, unsafe_allow_html=True)

else:

    st.error("⚠️ Dataset not found. Please ensure 'dataset2_threat_detection.csv' is in your project folder.")



