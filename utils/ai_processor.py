import streamlit as st
from openai import OpenAI
import json
from typing import List, Dict

@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client with API key from secrets."""
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_feedback(feedback_entries: List[Dict], course_code: str, enrolled_count: int = 30) -> Dict:
    """
    Analyze feedback for a course and return themes, summary, and impact score.
    Returns a dict with: themes, working_well, needs_improvement, individual_voices, impact_score, sentiment
    """
    if not feedback_entries:
        return {
            "themes": [],
            "working_well": [],
            "needs_improvement": [],
            "individual_voices": [],
            "impact_score": 0,
            "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
            "volume": {"responded": 0, "enrolled": enrolled_count},
            "severity": "N/A",
            "raw_count": 0
        }
    
    client = get_openai_client()
    
    # Prepare feedback text for the LLM
    feedback_texts = [f"- {e['feedback']}" for e in feedback_entries]
    feedback_block = "\n".join(feedback_texts)
    
    prompt = f"""You are analyzing anonymous student feedback for course {course_code}.
{len(feedback_entries)} students submitted feedback out of {enrolled_count} enrolled.

FEEDBACK ENTRIES:
{feedback_block}

Analyze this feedback and return a JSON object with EXACTLY this structure:
{{
  "themes": [
    {{"theme": "short theme name", "count": number_of_students, "sentiment": "positive" or "negative" or "neutral", "severity": "high" or "medium" or "low", "sample_quote": "one representative quote"}}
  ],
  "working_well": ["short bullet 1", "short bullet 2"],
  "needs_improvement": ["short bullet 1", "short bullet 2"],
  "individual_voices": ["unique concerns mentioned by only 1 student"],
  "sentiment": {{"positive": count, "neutral": count, "negative": count}},
  "severity_level": "high" or "medium" or "low",
  "overall_summary": "one sentence summary of the class health"
}}

Rules:
- Group similar feedback into themes (a theme has 2+ students)
- Individual voices are single-student concerns kept SEPARATE from themes
- Count sentiment for each individual feedback entry (positive/neutral/negative)
- Severity: "high" if multiple students use strong language ("confused", "lost", "frustrated", "terrible"); "medium" if mild concerns; "low" if mostly positive
- Return ONLY valid JSON, no markdown, no extra text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing student course feedback. You always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Compute impact score
        impact_score = compute_impact_score(
            sentiment=result.get("sentiment", {"positive": 0, "neutral": 0, "negative": 0}),
            volume_responded=len(feedback_entries),
            volume_enrolled=enrolled_count,
            severity=result.get("severity_level", "medium")
        )
        
        return {
            "themes": result.get("themes", []),
            "working_well": result.get("working_well", []),
            "needs_improvement": result.get("needs_improvement", []),
            "individual_voices": result.get("individual_voices", []),
            "sentiment": result.get("sentiment", {"positive": 0, "neutral": 0, "negative": 0}),
            "severity": result.get("severity_level", "medium"),
            "impact_score": impact_score,
            "volume": {"responded": len(feedback_entries), "enrolled": enrolled_count},
            "overall_summary": result.get("overall_summary", ""),
            "raw_count": len(feedback_entries)
        }
    except Exception as e:
        st.error(f"AI processing error: {str(e)}")
        return {
            "themes": [],
            "working_well": [],
            "needs_improvement": [],
            "individual_voices": [],
            "impact_score": 0,
            "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
            "volume": {"responded": len(feedback_entries), "enrolled": enrolled_count},
            "severity": "unknown",
            "raw_count": len(feedback_entries),
            "error": str(e)
        }

def compute_impact_score(sentiment: Dict, volume_responded: int, volume_enrolled: int, severity: str) -> float:
    """
    Compute weighted impact score (0-10):
    - Sentiment ratio (50%)
    - Volume of concerns (30%)
    - Severity (20%)
    """
    total_responses = max(sentiment.get("positive", 0) + sentiment.get("neutral", 0) + sentiment.get("negative", 0), 1)
    positive_ratio = sentiment.get("positive", 0) / total_responses
    negative_ratio = sentiment.get("negative", 0) / total_responses
    
    # Sentiment component (0-10, weighted 50%)
    sentiment_score = (positive_ratio * 10) + (0.5 * (1 - positive_ratio - negative_ratio) * 10)
    
    # Volume of concerns component (inverse — more concerns = lower score, weighted 30%)
    concern_ratio = negative_ratio
    volume_score = 10 * (1 - concern_ratio)
    
    # Severity component (weighted 20%)
    severity_map = {"low": 10, "medium": 6, "high": 3}
    severity_score = severity_map.get(severity, 6)
    
    # Weighted composite
    final = (sentiment_score * 0.5) + (volume_score * 0.3) + (severity_score * 0.2)
    return round(final, 1)

def score_color(score: float) -> str:
    """Return emoji color code for impact score."""
    if score >= 8:
        return "🟢"
    elif score >= 5:
        return "🟡"
    else:
        return "🔴"

def score_label(score: float) -> str:
    """Return text label for impact score."""
    if score >= 8:
        return "Healthy"
    elif score >= 5:
        return "Needs Attention"
    else:
        return "Critical"