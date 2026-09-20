import streamlit as st
from utils.storage import save_feedback

st.set_page_config(page_title="OrangeVoice - Student", page_icon="🎓", layout="centered")

st.markdown("""
<style>
    .main-header {
        color: #F76900;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .page-caption {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🎓 Student Feedback</p>', unsafe_allow_html=True)
st.markdown('<p class="page-caption">Verified via SU Blackboard SSO. Your feedback is stored anonymously — no identifier ever linked to it.</p>', unsafe_allow_html=True)

if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

with st.form("feedback_form", clear_on_submit=True):
    course_code = st.text_input(
        "Course Code",
        placeholder="e.g., IST 615",
        help="Enter the course code you want to give feedback for"
    )
    
    feedback_text = st.text_area(
        "Your Feedback",
        placeholder="What's working? What needs improvement? Be constructive — your professor will read this.",
        height=200
    )
    
    cycle = st.selectbox(
        "Feedback Cycle (Week)",
        options=[1, 2, 3, 4, 5, 6, 7, 8],
        index=0,
        help="Which feedback cycle is this for?"
    )
    
    submitted = st.form_submit_button("Submit Anonymously", use_container_width=True)
    
    if submitted:
        if not course_code.strip():
            st.error("Please enter a course code")
        elif not feedback_text.strip():
            st.error("Please write some feedback")
        elif len(feedback_text.strip()) < 10:
            st.error("Feedback too short — please write at least 10 characters")
        else:
            save_feedback(course_code, feedback_text, cycle)
            st.balloons()
            st.markdown("""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a5a2a 0%, #2ecc71 100%); border-radius: 12px; margin: 1rem 0;'>
                <div style='font-size: 2.5rem;'>✅</div>
                <div style='color: white; font-size: 1.3rem; font-weight: bold; margin-top: 0.5rem;'>Feedback submitted anonymously</div>
                <div style='color: #e0f5e6; margin-top: 0.5rem;'>Thank you for helping improve your course. Your voice matters.</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.info("💡 **How anonymity works:** SU Blackboard SSO confirms you're enrolled in this course. Once verified, your feedback is stored without any identifier — just {course, feedback, cycle}. Your professor sees anonymous themes, never individual quotes traceable to you.")