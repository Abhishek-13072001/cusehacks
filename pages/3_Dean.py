import streamlit as st
from utils.storage import load_feedback, get_feedback_for_course, get_all_courses
from utils.ai_processor import analyze_feedback, score_color, score_label
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="OrangeVoice - Dean", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
    .main-header {
        color: #F76900;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .alert-red {
        background-color: #7a1a1a;
        color: #ffffff !important;
        border-left: 5px solid #e74c3c;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .alert-red h4, .alert-red b, .alert-red p {
        color: #ffffff !important;
    }
    .alert-yellow {
        background-color: #7a5a1a;
        color: #ffffff !important;
        border-left: 5px solid #f39c12;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .alert-yellow h4, .alert-yellow b, .alert-yellow p {
        color: #ffffff !important;
    }
    .alert-green {
        background-color: #1a5a2a;
        color: #ffffff !important;
        border-left: 5px solid #2ecc71;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .alert-green h4, .alert-green b, .alert-green p {
        color: #ffffff !important;
    }
    .course-card {
        background-color: #2a2a2a;
        color: #ffffff !important;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .course-card h4, .course-card b, .course-card p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏛️ Dean Dashboard</p>', unsafe_allow_html=True)
st.caption("Cross-course visibility across your department. Alerts trigger only after 2-cycle escalation.")

if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# ============ SIDEBAR (Demo Controls + Filters) ============
with st.sidebar:
    # Demo reset safety net
    st.markdown("### 🛠️ Demo Controls")
    if st.button("🔄 Reset Demo Data", help="Restore seed data if something breaks", use_container_width=True):
        try:
            import subprocess
            import sys
            result = subprocess.run(
                [sys.executable, "seed_data.py"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd="."
            )
            if result.returncode == 0:
                st.success("✅ Demo data reset!")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(f"Reset failed: {result.stderr[:200]}")
        except Exception as e:
            st.error(f"Error: {str(e)[:200]}")
    st.caption("💡 Restores seed data if needed during demo")
    st.markdown("---")

    # Filters
    st.markdown("### Filters")
    min_sample = st.number_input("Minimum sample size for alerts", value=5, min_value=1)
    st.markdown("### Alert Thresholds (% negative)")
    yellow_pct = st.slider("Yellow", 5, 30, 10)
    orange_pct = st.slider("Orange", 15, 40, 20)
    red_pct = st.slider("Red", 25, 50, 30)
    enrolled_default = st.number_input("Default enrollment per course", value=30, min_value=1)

# ============ MAIN CONTENT ============
# Load all courses
courses = get_all_courses()

if not courses:
    st.warning("📭 No feedback data yet across any course.")
    st.stop()

# Analyze each course across cycles
st.markdown("### 📊 Department Overview")
st.caption("Analyzing all courses and cycles...")

course_data = []

for course in courses:
    all_feedback = get_feedback_for_course(course)
    cycles = sorted(list(set(e.get("cycle", 1) for e in all_feedback)))
    
    cycle_scores = []
    latest_analysis = None
    
    for cycle in cycles:
        cycle_feedback = get_feedback_for_course(course, cycle=cycle)
        if not cycle_feedback:
            continue
        with st.spinner(f"Analyzing {course} Cycle {cycle}..."):
            analysis = analyze_feedback(cycle_feedback, course, enrolled_default)
        cycle_scores.append({
            "cycle": cycle,
            "score": analysis["impact_score"],
            "responded": analysis["volume"]["responded"],
            "sentiment": analysis["sentiment"],
            "severity": analysis["severity"]
        })
        latest_analysis = analysis
    
    if cycle_scores:
        course_data.append({
            "course": course,
            "cycles": cycle_scores,
            "latest": cycle_scores[-1],
            "num_cycles": len(cycle_scores),
            "latest_analysis": latest_analysis
        })

# Compute alerts
def get_alert_level(course_info):
    """Determine alert level based on 2-cycle escalation logic."""
    cycles = course_info["cycles"]
    latest = cycles[-1]
    
    # Not enough sample size
    if latest["responded"] < min_sample:
        return "insufficient", "Insufficient sample size for alert"
    
    total_responses = latest["sentiment"]["positive"] + latest["sentiment"]["neutral"] + latest["sentiment"]["negative"]
    if total_responses == 0:
        return "no_data", "No feedback data"
    
    negative_pct = (latest["sentiment"]["negative"] / total_responses) * 100
    
    # Single cycle — passive visibility only, no alert
    if len(cycles) < 2:
        if negative_pct >= red_pct:
            return "watching", f"Cycle 1 signal: {negative_pct:.0f}% negative. Awaiting Cycle 2 for escalation decision."
        return "monitoring", "First cycle — professor has opportunity to address"
    
    # 2+ cycles — check trend
    prev = cycles[-2]
    prev_total = prev["sentiment"]["positive"] + prev["sentiment"]["neutral"] + prev["sentiment"]["negative"]
    prev_negative_pct = (prev["sentiment"]["negative"] / prev_total * 100) if prev_total > 0 else 0
    
    score_trend = latest["score"] - prev["score"]
    
    # RED alert: 2 consecutive cycles above red threshold OR declining
    if negative_pct >= red_pct and prev_negative_pct >= red_pct:
        return "red", f"🚨 CRITICAL: 2 consecutive cycles above {red_pct}% negative. Supportive intervention recommended."
    if negative_pct >= red_pct and score_trend < 0:
        return "red", f"🚨 CRITICAL: {negative_pct:.0f}% negative + declining trend ({score_trend:+.1f})"
    
    # ORANGE alert: 20%+ negative + no improvement
    if negative_pct >= orange_pct and score_trend <= 0:
        return "orange", f"⚠️ WARNING: {negative_pct:.0f}% negative, score not improving ({score_trend:+.1f})"
    
    # YELLOW: sustained 10%+
    if negative_pct >= yellow_pct and prev_negative_pct >= yellow_pct:
        return "yellow", f"⚡ CAUTION: Sustained {negative_pct:.0f}% negative across 2 cycles"
    
    # Improvement recognized
    if score_trend >= 2:
        return "improved", f"✅ Positive signal: Score improved by +{score_trend:.1f}. Professor successfully addressed feedback."
    
    return "healthy", "Healthy course, no intervention needed"

# Sort courses by alert priority
alert_priority = {"red": 0, "orange": 1, "yellow": 2, "watching": 3, "monitoring": 4, "improved": 5, "healthy": 6, "insufficient": 7, "no_data": 8}

for ci in course_data:
    alert, message = get_alert_level(ci)
    ci["alert"] = alert
    ci["alert_message"] = message

course_data.sort(key=lambda x: alert_priority.get(x["alert"], 9))

# Display summary metrics at top
col1, col2, col3, col4 = st.columns(4)
with col1:
    red_count = sum(1 for c in course_data if c["alert"] == "red")
    st.metric("🔴 Critical Alerts", red_count)
with col2:
    orange_count = sum(1 for c in course_data if c["alert"] == "orange")
    st.metric("🟠 Warnings", orange_count)
with col3:
    improved_count = sum(1 for c in course_data if c["alert"] == "improved")
    st.metric("✅ Improved Courses", improved_count)
with col4:
    total_courses = len(course_data)
    st.metric("📚 Total Courses Tracked", total_courses)

st.markdown("---")

# Display each course with alert
st.markdown("### Course Details (sorted by alert priority)")

for ci in course_data:
    course = ci["course"]
    latest = ci["latest"]
    alert = ci["alert"]
    message = ci["alert_message"]
    
    # Alert styling
    if alert == "red":
        alert_class = "alert-red"
        alert_emoji = "🚨"
    elif alert == "orange":
        alert_class = "alert-yellow"
        alert_emoji = "⚠️"
    elif alert == "yellow":
        alert_class = "alert-yellow"
        alert_emoji = "⚡"
    elif alert == "improved":
        alert_class = "alert-green"
        alert_emoji = "✅"
    elif alert == "watching":
        alert_class = "alert-yellow"
        alert_emoji = "👁️"
    else:
        alert_class = "course-card"
        alert_emoji = "📖"
    
    score = latest["score"]
    color = score_color(score)
    
    with st.container():
        st.markdown(f"""
<div class="{alert_class}">
<h4>{alert_emoji} {course} — Latest Score: {color} {score}/10</h4>
<b>Status:</b> {message}<br>
<b>Cycles tracked:</b> {ci['num_cycles']} | <b>Latest cycle responses:</b> {latest['responded']} students
</div>
""", unsafe_allow_html=True)
        
        # Cycle trend
        if len(ci["cycles"]) > 1:
            cycles_list = ci["cycles"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[f"Cycle {c['cycle']}" for c in cycles_list],
                y=[c["score"] for c in cycles_list],
                mode='lines+markers',
                line=dict(color='#F76900', width=3),
                marker=dict(size=12)
            ))
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=20, b=0),
                yaxis=dict(range=[0, 10], showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                title=dict(text=f"Score trend across cycles", font=dict(size=12))
            )
            st.plotly_chart(fig, use_container_width=True, key=f"trend_{course}")
        
        st.markdown("")  # spacing

st.markdown("---")
st.info("💡 **Dean workflow:** Passive visibility on all courses. Active intervention only after 2-cycle escalation (professor gets first chance to improve). All thresholds configurable in sidebar.")