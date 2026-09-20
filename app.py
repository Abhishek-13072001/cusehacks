import streamlit as st

st.set_page_config(
    page_title="OrangeVoice",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SU Orange theme
st.markdown("""
<style>
    .main-header {
        color: #F76900;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0;
    }
    .tagline {
        color: #666;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #F76900;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #D55A00;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🍊 OrangeVoice</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Anonymous mid-semester feedback that closes the loop</p>', unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Choose your role")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🎓 Student")
    st.write("Share anonymous feedback about your courses")
    if st.button("Enter as Student", key="student_btn", use_container_width=True):
        st.switch_page("pages/1_Student.py")

with col2:
    st.markdown("#### 👨‍🏫 Professor")
    st.write("View AI-clustered feedback for your courses")
    if st.button("Enter as Professor", key="prof_btn", use_container_width=True):
        st.switch_page("pages/2_Professor.py")

with col3:
    st.markdown("#### 🏛️ Dean")
    st.write("Monitor course health across departments")
    if st.button("Enter as Dean", key="dean_btn", use_container_width=True):
        st.switch_page("pages/3_Dean.py")

st.markdown("---")
st.caption("🔒 100% anonymous — no student login, no identity stored. Ever.")