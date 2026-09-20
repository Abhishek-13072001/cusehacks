import streamlit as st
from utils.storage import load_feedback, get_feedback_for_course, get_all_courses
from utils.ai_processor import analyze_feedback, score_color, score_label
import plotly.graph_objects as go

st.set_page_config(page_title="OrangeVoice - Professor", page_icon="👨‍🏫", layout="wide")

# SU Orange theme
st.markdown("""
<style>
    .main-header {
        color: #F76900;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .score-big {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
    }
    .metric-label {
        font-size: 1rem;
        color: #888;
        text-align: center;
    }
    .theme-box {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #F76900;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">👨‍🏫 Professor Dashboard</p>', unsafe_allow_html=True)

if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# Course selector
available_courses = get_all_courses()

if not available_courses:
    st.warning("📭 No feedback has been submitted yet. Go to the Student page and submit some feedback first.")
    st.stop()

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    selected_course = st.selectbox("Select your course", available_courses)
with col2:
    selected_cycle = st.selectbox("Cycle", options=[1, 2, 3, 4, 5, 6, 7, 8], index=0)
with col3:
    enrolled_count = st.number_input("Students enrolled", min_value=1, value=30, step=1)

# Load feedback for selected course + cycle
feedback = get_feedback_for_course(selected_course, cycle=selected_cycle)

if not feedback:
    st.info(f"No feedback yet for {selected_course} in Cycle {selected_cycle}. Try a different cycle or wait for submissions.")
    st.stop()

st.markdown(f"### {selected_course} — Cycle {selected_cycle}")
st.caption(f"{len(feedback)} of {enrolled_count} students responded ({round(len(feedback)/enrolled_count*100)}%)")

# Analyze feedback with AI
with st.spinner("🤖 AI is analyzing feedback..."):
    analysis = analyze_feedback(feedback, selected_course, enrolled_count)

if analysis.get("error"):
    st.error("AI analysis failed. Check your OpenAI API key and try again.")
    st.stop()

st.markdown("---")

# TOP ROW: Impact score + Sentiment chart
col1, col2 = st.columns([1, 2])

with col1:
    score = analysis["impact_score"]
    color = score_color(score)
    label = score_label(score)
    st.markdown(f"### Impact Score")
    st.markdown(f'<p class="score-big">{color} {score}/10</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-label">{label}</p>', unsafe_allow_html=True)
    st.caption(f"Severity: {analysis['severity'].capitalize()}")

with col2:
    st.markdown("### Sentiment Breakdown")
    sentiment = analysis["sentiment"]
    fig = go.Figure(data=[go.Bar(
        x=["Positive", "Neutral", "Negative"],
        y=[sentiment.get("positive", 0), sentiment.get("neutral", 0), sentiment.get("negative", 0)],
        marker_color=["#2ecc71", "#95a5a6", "#e74c3c"]
    )])
    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )
    st.plotly_chart(fig, use_container_width=True)

# AI Summary
if analysis.get("overall_summary"):
    st.info(f"🤖 **AI Summary:** {analysis['overall_summary']}")

st.markdown("---")

# TWO COLUMNS: What's Working + What Needs Improvement
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ What's Working Well")
    if analysis["working_well"]:
        for item in analysis["working_well"]:
            st.markdown(f"- {item}")
    else:
        st.caption("No clear positive themes identified.")

with col2:
    st.markdown("### ⚠️ What Needs Improvement")
    if analysis["needs_improvement"]:
        for item in analysis["needs_improvement"]:
            st.markdown(f"- {item}")
    else:
        st.caption("No major concerns identified.")

st.markdown("---")

# Detailed themes
st.markdown("### 📌 Detailed Themes (grouped by student count)")

themes = sorted(analysis["themes"], key=lambda x: x.get("count", 0), reverse=True)

if themes:
    for theme in themes:
        sentiment_icon = {"positive": "✅", "negative": "🔴", "neutral": "🟡"}.get(theme.get("sentiment", "neutral"), "🟡")
        severity_badge = f"[{theme.get('severity', 'medium').upper()}]"
        with st.container():
            st.markdown(f"""
<div class="theme-box">
<b>{sentiment_icon} {theme.get('theme', 'Untitled')}</b> — {theme.get('count', 0)} students {severity_badge}<br>
<i>Sample: "{theme.get('sample_quote', '')}"</i>
</div>
""", unsafe_allow_html=True)
else:
    st.caption("No themes detected yet.")

# Individual voices
if analysis["individual_voices"]:
    st.markdown("### 💬 Individual Voices (unique concerns from single students)")
    st.caption("These are single-student concerns — they may be edge cases OR early signals of a broader issue.")
    for voice in analysis["individual_voices"]:
        st.markdown(f"- {voice}")

st.markdown("---")

# Action button
col1, col2 = st.columns([3, 1])
with col1:
    st.info("💡 After discussing this feedback with your class, click below to mark it as addressed. Students can then submit new feedback for the next cycle.")
with col2:
    if st.button("Mark Cycle as Addressed", use_container_width=True):
        st.success("✅ Marked as addressed. Awaiting next cycle's feedback.")

# Raw feedback expander (for professor reference)
with st.expander("📄 View raw anonymous feedback (for your reference)"):
    for i, entry in enumerate(feedback, 1):
        st.markdown(f"**{i}.** {entry['feedback']}")