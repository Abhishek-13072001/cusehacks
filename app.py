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
        font-size: 5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    .tagline {
        color: #ccc;
        text-align: center;
        font-size: 1.3rem;
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
st.markdown('<p class="tagline">Anonymous mid-semester feedback that closes the loop between students, professors, and deans.</p>', unsafe_allow_html=True)

# Trust indicators row
col1, col2, col3, col4 = st.columns(4)
with col1:
   st.markdown("<div style='text-align: center; color: #F76900; font-size: 1.5rem; font-weight: bold;'>🔒</div><div style='text-align: center; color: #888; font-size: 0.85rem;'>SSO verified,<br>zero stored identity</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align: center; color: #F76900; font-size: 1.5rem; font-weight: bold;'>🤖</div><div style='text-align: center; color: #888; font-size: 0.85rem;'>AI-powered</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='text-align: center; color: #F76900; font-size: 1.5rem; font-weight: bold;'>🔄</div><div style='text-align: center; color: #888; font-size: 0.85rem;'>2-cycle fair</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div style='text-align: center; color: #F76900; font-size: 1.5rem; font-weight: bold;'>📊</div><div style='text-align: center; color: #888; font-size: 0.85rem;'>3-role dashboard</div>", unsafe_allow_html=True)

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
st.caption("🔒 Verified via SU Blackboard SSO · No student identity stored with feedback · Enrollment checked, anonymity preserved")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.75rem; padding-top: 1rem;'>
    Built with 🍊 for Syracuse University · CuseHacks 2026<br>
    <a href='https://github.com/Abhishek-13072001/cusehacks' style='color: #F76900; text-decoration: none;'>View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)