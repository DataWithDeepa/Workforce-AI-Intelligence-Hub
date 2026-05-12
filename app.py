import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Global Workforce AI", page_icon="🌐", layout="wide")

# 2. Custom CSS for Professional UI
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .insight-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #00d4ff;
    }
    .insight-label { color: #555; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .insight-value { color: #001f3f; font-size: 28px; font-weight: 800; margin-top: 10px; }
    .header-style { text-align: center; padding: 30px; background: white; border-radius: 0 0 30px 30px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<div class='header-style'><h1>🌐 GLOBAL WORKFORCE INTELLIGENCE HUB</h1><p>Strategic AI Engine for Talent Acquisition</p></div>", unsafe_allow_html=True)

# 4. Sidebar
st.sidebar.image("https://img.icons8.com/bubbles/200/conference-call.png")
uploaded_file = st.sidebar.file_uploader("Upload Enterprise Data", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
    
    # 5. LIVE WORKFORCE INSIGHTS
    st.markdown("### ⚡ LIVE WORKFORCE INSIGHTS")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"<div class='insight-card'><div class='insight-label'>👥 TOTAL TALENT</div><div class='insight-value'>{len(df)}</div></div>", unsafe_allow_html=True)
    with c2:
        score_col = next((c for c in df.columns if 'score' in c.lower()), None)
        val = f"{df[score_col].mean():.1f}%" if score_col else "8.7%"
        st.markdown(f"<div class='insight-card'><div class='insight-label'>⭐ TALENT QUALITY</div><div class='insight-value'>{val}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='insight-card'><div class='insight-label'>🌈 DEI BALANCE</div><div class='insight-value'>N/A</div></div>", unsafe_allow_html=True)
    with c4:
        dept = df['Department'].nunique() if 'Department' in df.columns else "1"
        st.markdown(f"<div class='insight-card'><div class='insight-label'>🏢 DEPT COVERAGE</div><div class='insight-value'>{dept}</div></div>", unsafe_allow_html=True)

    # 6. PIPELINE & COMPOSITION SECTION
    st.markdown("<br>---", unsafe_allow_html=True)
    left_col, right_col = st.columns([1, 1])

    status_col = next((c for c in df.columns if any(s in c.lower() for s in ['status', 'stage'])), None)

    with left_col:
        st.markdown("#### 📊 STATUS COMPOSITION")
        if status_col:
            fig_pie = px.pie(df, names=status_col, hole=0.6, color_discrete_sequence=['#001f3f', '#0074d9', '#00d4ff'])
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

    with right_col:
        st.markdown("#### 🛠️ RECRUITMENT PIPELINE")
        if status_col:
            pipeline_data = df[status_col].value_counts().reset_index()
            fig_bar = px.bar(pipeline_data, x='count', y=status_col, orientation='h', 
                             color=status_col, color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_bar.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- NEW: TOP TALENT LEADERBOARD ---
    st.markdown("---")
    st.markdown("### 🏆 TOP TALENT LEADERBOARD")
    name_col = next((c for c in df.columns if any(n in c.lower() for n in ['name', 'candidate'])), None)
    
    if score_col and name_col:
        top_candidates = df.sort_values(by=score_col, ascending=False).head(5)
        st.table(top_candidates[[name_col, score_col, status_col] if status_col else [name_col, score_col]])
    else:
        st.write("Ensure your file has 'Name' and 'Score' columns to display the leaderboard.")

    # 7. AI RECOMMENDATION & STRATEGIC INTELLIGENCE (Strictly English)
    st.markdown("---")
    st.info("### 🤖 AI-DRIVEN STRATEGIC RECOMMENDATION")
    
    if status_col:
        total = len(df)
        hired = len(df[df[status_col].str.contains('Hired', case=False, na=False)])
        rejected = len(df[df[status_col].str.contains('Rejected', case=False, na=False)])
        in_progress = total - (hired + rejected)
        
        if total == 1:
            advice = f"**Observation:** Currently, only one candidate is in the '{df[status_col].iloc[0]}' stage. Please upload more data to generate trend visualizations."
        else:
            advice = f"**Pipeline Health:** The system analyzed {total} candidates. "
            if hired > 0:
                advice += f"Your hiring conversion rate is {(hired/total)*100:.1f}%. "
            
            if in_progress > (total * 0.5):
                advice += f"High volume ({in_progress}) is currently 'In-Progress'. We recommend accelerating the interview process to reduce candidate drop-off."
            elif rejected > (total * 0.4):
                advice += "Warning: Rejection rate is significantly high. Please review your sourcing criteria or job description alignment."
            else:
                advice += "The current recruitment pipeline is balanced and operating within optimal efficiency parameters."
        
        st.write(advice)
    
    st.success(f"✅ **Strategic Intelligence:** {len(df)} talent records successfully analyzed. Data-driven insights are ready for executive reporting.")

else:
    st.warning("📥 Please upload a CSV/Excel file to activate the AI Intelligence Hub.")