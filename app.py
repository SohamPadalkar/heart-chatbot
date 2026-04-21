from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def to_bool(value: str) -> bool:
    """Convert yes/no style form inputs to Python booleans."""
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def safe_int(value: str, default: int = 0) -> int:
    """Safely convert text to an integer and use a default if conversion fails."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def calculate_risk(data: dict) -> dict:
    """
    Rule-based risk calculator.

    Returns a dictionary with:
    - risk_level: Low Risk / Medium Risk / High Risk
    - risk_score: 0 to 100
    - summary: conversational explanation
    - next_steps: practical guidance
    """

    # Symptom flags
    chest_pain = data["chest_pain"]
    short_breath = data["short_breath"]
    sweating = data["sweating"]
    fatigue = data["fatigue"]
    dizziness = data["dizziness"]

    # Health history
    age = data["age"]
    high_bp = data["high_bp"]
    diabetes = data["diabetes"]
    high_cholesterol = data["high_cholesterol"]

    # Weighted points to create a beginner-friendly risk score percentage.
    # The numbers are intentionally simple and easy to understand.
    score = 0
    if chest_pain:
        score += 30
    if short_breath:
        score += 25
    if sweating:
        score += 20
    if dizziness:
        score += 10
    if fatigue:
        score += 5

    if age >= 60:
        score += 10
    elif age >= 45:
        score += 5

    if high_bp:
        score += 8
    if diabetes:
        score += 8
    if high_cholesterol:
        score += 6

    # Keep score in a clean 0-100 range.
    risk_score = min(score, 100)

    major_count = sum([chest_pain, short_breath, sweating])
    mild_count = sum([fatigue, dizziness])
    symptom_count = major_count + mild_count

    symptom_snapshot = []
    symptom_snapshot.append(f"Chest pain: {'Yes' if chest_pain else 'No'}")
    symptom_snapshot.append(f"Shortness of breath: {'Yes' if short_breath else 'No'}")
    symptom_snapshot.append(f"Sweating: {'Yes' if sweating else 'No'}")
    symptom_snapshot.append(f"Fatigue: {'Yes' if fatigue else 'No'}")
    symptom_snapshot.append(f"Dizziness: {'Yes' if dizziness else 'No'}")

    # Rule-based classification from the prompt.
    if chest_pain and short_breath and sweating:
        risk_level = "High Risk"
    elif risk_score >= 65:
        risk_level = "High Risk"
    elif symptom_count == 0:
        risk_level = "Low Risk"
    elif fatigue and not (chest_pain or short_breath or sweating or dizziness):
        risk_level = "Low Risk"
    elif 1 <= mild_count <= 2 and major_count == 0:
        risk_level = "Medium Risk"
    elif major_count >= 1:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    positive_factors = []
    protective_notes = []

    if chest_pain:
        positive_factors.append("You reported chest pain, which can be a key warning sign.")
    if short_breath:
        positive_factors.append("You reported shortness of breath.")
    if sweating:
        positive_factors.append("You reported sweating during this episode.")
    if dizziness:
        positive_factors.append("You reported dizziness.")
    if fatigue:
        positive_factors.append("You reported fatigue.")

    if high_bp:
        positive_factors.append("High blood pressure adds cardiovascular risk.")
    if diabetes:
        positive_factors.append("Diabetes can increase heart-related risk.")
    if high_cholesterol:
        positive_factors.append("High cholesterol can raise long-term artery risk.")
    if age >= 45:
        positive_factors.append("Age is an additional risk factor in this context.")

    if not chest_pain:
        protective_notes.append("No chest pain reported.")
    if not short_breath:
        protective_notes.append("No shortness of breath reported.")
    if major_count == 0:
        protective_notes.append("No major red-flag symptom combination was reported.")

    # Human-like conversational responses.
    if risk_level == "High Risk":
        summary = (
            "Thanks for sharing these symptoms. Because chest discomfort, breathing issues, "
            "and/or sweating can point to serious heart-related conditions such as coronary "
            "artery disease or even an acute cardiac event, this pattern is concerning."
        )
        next_steps = (
            "Please seek immediate medical attention now. Do not delay. If symptoms are active, "
            "call emergency services right away."
        )
        urgency = "Immediate"
        possible_conditions = [
            "Acute coronary syndrome",
            "Coronary artery disease flare",
            "Serious cardiopulmonary event",
        ]
        suggested_tests = [
            "Emergency ECG",
            "Cardiac blood markers (e.g., troponin)",
            "Continuous vital monitoring",
        ]
        action_checklist = [
            "Seek emergency care now.",
            "Do not drive yourself if symptoms are severe.",
            "Keep someone with you while waiting for help.",
        ]
        lifestyle_tips = [
            "Avoid physical strain until assessed by a clinician.",
            "Keep emergency contacts reachable.",
            "Prepare your medication/history list for the care team.",
        ]
        warning_signs = [
            "Worsening chest pain",
            "Increasing breathlessness",
            "New confusion, fainting, or severe weakness",
        ]
        followup_time = "Now"
        score_explainer = "Your score is high due to multiple major warning symptoms and risk factors."
    elif risk_level == "Medium Risk":
        summary = (
            "I appreciate the details. Your symptoms do not strongly match an emergency pattern, "
            "but they still deserve medical evaluation. Some causes may be heart-related, "
            "including early coronary artery disease."
        )
        next_steps = (
            "Please schedule a doctor visit soon and discuss getting an ECG and basic blood tests. "
            "If symptoms worsen suddenly, seek urgent care immediately."
        )
        urgency = "Soon"
        possible_conditions = [
            "Early coronary artery disease",
            "Blood pressure or glucose-related strain",
            "Non-cardiac causes that still need review",
        ]
        suggested_tests = [
            "Outpatient ECG",
            "Basic blood panel (sugars/lipids)",
            "Blood pressure and risk-factor review",
        ]
        action_checklist = [
            "Book a doctor appointment in the next few days.",
            "Track symptom timing and triggers.",
            "Escalate to urgent care if symptoms intensify.",
        ]
        lifestyle_tips = [
            "Reduce heavy exertion until evaluated.",
            "Track blood pressure and blood sugar if possible.",
            "Prioritize sleep, hydration, and lower-salt meals.",
        ]
        warning_signs = [
            "New chest pain episodes",
            "Shortness of breath at rest",
            "Sweating or dizziness that becomes sudden or severe",
        ]
        followup_time = "Within 24-72 hours"
        score_explainer = "Your score suggests moderate concern from symptoms and/or background risk factors."
    else:
        summary = (
            "Thanks for checking in. Based on what you entered, your current pattern looks lower risk. "
            "This may reflect temporary fatigue, stress, or mild non-cardiac causes."
        )
        next_steps = (
            "Get rest, stay hydrated, and monitor symptoms. If new chest pain, shortness of breath, "
            "or sweating appears, contact a doctor promptly."
        )
        urgency = "Monitor"
        possible_conditions = [
            "Temporary fatigue or stress response",
            "Mild non-cardiac discomfort",
            "Early lifestyle-related strain",
        ]
        suggested_tests = [
            "Routine checkup if symptoms continue",
            "Basic blood pressure and glucose screening",
        ]
        action_checklist = [
            "Rest and monitor over the next 24-48 hours.",
            "Hydrate and avoid heavy exertion for now.",
            "Seek care if red-flag symptoms appear.",
        ]
        lifestyle_tips = [
            "Continue light activity and good hydration.",
            "Limit stress and maintain regular sleep.",
            "Plan a routine preventive checkup if symptoms repeat.",
        ]
        warning_signs = [
            "Any new chest pain",
            "New shortness of breath",
            "Cold sweats with weakness or dizziness",
        ]
        followup_time = "Monitor over 24-48 hours"
        score_explainer = "Your score is lower because major warning combinations were not reported."

    if not positive_factors:
        positive_factors.append("No high-risk symptoms were reported in this check.")
    if not protective_notes:
        protective_notes.append("There were no clear reassuring points in this symptom pattern.")

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "summary": summary,
        "next_steps": next_steps,
        "urgency": urgency,
        "possible_conditions": possible_conditions,
        "suggested_tests": suggested_tests,
        "action_checklist": action_checklist,
        "positive_factors": positive_factors,
        "protective_notes": protective_notes,
        "symptom_snapshot": symptom_snapshot,
        "lifestyle_tips": lifestyle_tips,
        "warning_signs": warning_signs,
        "followup_time": followup_time,
        "score_explainer": score_explainer,
        "disclaimer": (
            "This chatbot is educational and cannot diagnose medical conditions. "
            "A licensed clinician should make final decisions."
        ),
    }


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze_api():
    payload = request.get_json(silent=True) or {}

    # Read and normalize user inputs from JSON payload.
    form_data = {
        "age": safe_int(payload.get("age"), default=0),
        "chest_pain": to_bool(payload.get("chest_pain")),
        "short_breath": to_bool(payload.get("short_breath")),
        "sweating": to_bool(payload.get("sweating")),
        "fatigue": to_bool(payload.get("fatigue")),
        "dizziness": to_bool(payload.get("dizziness")),
        "high_bp": to_bool(payload.get("high_bp")),
        "diabetes": to_bool(payload.get("diabetes")),
        "high_cholesterol": to_bool(payload.get("high_cholesterol")),
    }

    result = calculate_risk(form_data)

    return jsonify({
        "age": form_data["age"],
        "result": result,
    })


if __name__ == "__main__":
    # debug=True is useful for learning and local development.
    app.run(debug=True)
