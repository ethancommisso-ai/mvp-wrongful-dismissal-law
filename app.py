import streamlit as st


st.set_page_config(
    page_title="Definitely-Not-Evil-Corp Inc. – Dismissal Risk",
    page_icon="⚖️",
    layout="centered",
)


def compute_risk(
    age: int,
    years_service: float,
    job_level: str,
    reason: str,
    misconduct_documented: str,
    discipline_history: str,
    protected_leave: str,
    severance_weeks_offered: float,
    documentation_quality: str,
):
    """Return (risk_level, risk_factors, suggested_min_weeks, suggested_max_weeks)."""
    risk_score = 0
    risk_factors: list[str] = []

    # Simple suggested notice rule
    suggested_notice_weeks = max(0.0, years_service * 2.0)

    # Protected leave is automatically high risk
    if protected_leave != "No protected leave":
        risk_factors.append("Employee on protected (medical/parental/disability) leave")
        return "High", risk_factors, suggested_notice_weeks, suggested_notice_weeks + 4

    # Misconduct without documentation is automatically high risk
    if reason == "Misconduct" and misconduct_documented == "No":
        risk_factors.append("Misconduct termination without supporting documentation")
        return "High", risk_factors, suggested_notice_weeks, suggested_notice_weeks + 4

    # Years of service
    if years_service > 5:
        risk_score += 1
        risk_factors.append("More than 5 years of service")

    # Age
    if age > 50:
        risk_score += 1
        risk_factors.append("Employee over age 50")

    # Job level
    if job_level == "Executive":
        risk_score += 1
        risk_factors.append("Executive-level role")

    # Progressive discipline for performance terminations
    if reason == "Performance" and discipline_history == "None":
        risk_score += 1
        risk_factors.append("Performance termination without progressive discipline")

    # Documentation quality
    if documentation_quality == "Partial documentation":
        risk_score += 1
        risk_factors.append("Partial termination documentation")
    elif documentation_quality == "No documentation":
        risk_score += 2
        risk_factors.append("No termination documentation")

    # Severance/notice vs suggested amount
    if suggested_notice_weeks > 0 and severance_weeks_offered < suggested_notice_weeks:
        risk_score += 1
        risk_factors.append("Severance/notice below suggested minimum based on service")

    # Map score to buckets
    if risk_score >= 4:
        risk_level = "High"
    elif risk_score >= 2:
        risk_level = "Medium"
    elif risk_score == 1:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return risk_level, risk_factors, suggested_notice_weeks, suggested_notice_weeks + 4


def recommendation_for_risk(risk_level: str) -> str:
    if risk_level == "High":
        return "High risk of wrongful dismissal. Provide severance or seek legal advice."
    if risk_level == "Medium":
        return "Provide statutory notice or severance."
    return "Termination likely compliant but ensure notice requirements are met."


# Lightweight dark-mode theming / branding
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #0e1117 !important;
        color: #f5f5f5 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .app-header {
        text-align: center;
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #30363d;
    }
    .app-header h1 {
        margin-bottom: 0.25rem;
        color: #f5f5f5;
    }
    .app-header h3 {
        margin-top: 0;
        color: #c2c2c2;
        font-weight: 400;
        font-size: 0.95rem;
    }
    .card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
        border: 1px solid #30363d;
    }
    label, .stRadio, .stSelectbox, .stNumberInput {
        color: #f5f5f5 !important;
    }
    .risk-pill {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 1.1rem;
        color: #ffffff;
    }
    .risk-low {
        background-color: #0f9d58;
    }
    .risk-medium {
        background-color: #f4b400;
    }
    .risk-high {
        background-color: #db4437;
    }
    /* Form submit button: visible label and clear background */
    .stFormSubmitButton button,
    .stFormSubmitButton button span,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stFormSubmitButton"] button span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stFormSubmitButton button {
        background-color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
    }
    .stFormSubmitButton button:hover {
        background-color: #ff6b6b !important;
        border-color: #ff6b6b !important;
    }
    .stFormSubmitButton button:hover span {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-header">
        <h1>Definitely-Not-Evil-Corp Inc.</h1>
        <h3>Wrongful Dismissal Risk Evaluator</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Internal legal and compliance tool for evaluating wrongful dismissal risk before finalizing "
    "a termination decision. **Ontario only.**"
)

with st.form("termination_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Employee age", min_value=16, max_value=80, value=35, step=1)
        years_service = st.number_input("Years of service", min_value=0.0, max_value=40.0, value=3.0, step=0.5)
        protected_leave = st.selectbox(
            "Protected leave status",
            ["No protected leave", "Medical leave", "Parental leave", "Disability leave"],
        )
        severance_weeks_offered = st.number_input(
            "Weeks of severance / notice offered",
            min_value=0.0,
            max_value=156.0,
            value=0.0,
            step=0.5,
        )

    with col2:
        job_level = st.selectbox("Job level", ["Entry", "Manager", "Executive"])
        reason = st.selectbox("Reason for termination", ["Performance", "Misconduct", "Layoff"])
        misconduct_documented = st.radio(
            "Is misconduct documented?",
            ["Yes", "No"],
            index=0,
            help="E.g. written warnings, investigation report, signed acknowledgements.",
        )
        discipline_history = st.selectbox(
            "Progressive discipline history",
            ["None", "Verbal warning", "Written warning", "Performance Improvement Plan (PIP)"],
        )
        documentation_quality = st.selectbox(
            "Termination documentation quality",
            ["Complete documentation", "Partial documentation", "No documentation"],
        )

    evaluate = st.form_submit_button("Evaluate Termination")

if evaluate:
    risk_level, risk_factors, suggested_min_weeks, suggested_max_weeks = compute_risk(
        age=int(age),
        years_service=float(years_service),
        job_level=job_level,
        reason=reason,
        misconduct_documented=misconduct_documented,
        discipline_history=discipline_history,
        protected_leave=protected_leave,
        severance_weeks_offered=float(severance_weeks_offered),
        documentation_quality=documentation_quality,
    )

    recommendation = recommendation_for_risk(risk_level)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Termination Compliance Report – Definitely-Not-Evil-Corp Inc")

    if risk_level == "High":
        pill_class = "risk-pill risk-high"
    elif risk_level == "Medium":
        pill_class = "risk-pill risk-medium"
    else:
        pill_class = "risk-pill risk-low"

    st.markdown(
        f"**Risk Level:** <span class='{pill_class}'>{risk_level}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("**Key risk factors detected:**")
    if risk_factors:
        st.markdown("\n".join(f"- {factor}" for factor in risk_factors))
    else:
        st.markdown("- No major risk factors detected based on the inputs provided.")

    st.markdown(
        f"**Suggested severance / notice range:** "
        f"{suggested_min_weeks:.1f} – {suggested_max_weeks:.1f} weeks"
    )

    st.markdown(f"**Recommended compliance action:** {recommendation}")

    # --- Potential Legal Damages and Liability ---
    st.markdown("---")
    st.subheader("Potential Legal Damages and Liability")

    st.markdown("**1. Common Law Damages**")
    st.markdown(
        "Employees may be entitled to reasonable notice damages. The period is typically based on "
        "age, position, length of service, and job marketability."
    )

    st.markdown("**2. Damages for Wrongful Dismissal**")
    st.markdown(
        "If the employer terminates without proper notice or just cause, damages may include "
        "compensation equal to the salary and benefits the employee would have earned during "
        "the reasonable notice period."
    )

    st.markdown("**3. Legislative Requirements**")
    st.markdown(
        "The Ontario Employment Standards Act requires minimum statutory notice or termination pay "
        "depending on years of service. Failure to provide this can result in orders to pay."
    )

    punitive_applicable = (
        risk_level == "High"
        and (
            documentation_quality in ["Partial documentation", "No documentation"]
            or (reason == "Misconduct" and misconduct_documented == "No")
        )
    )
    st.markdown("**4. Punitive Damages (if applicable)**")
    if punitive_applicable:
        st.markdown(
            "⚠️ **Warning:** Punitive damages may apply if the employer acted in bad faith or "
            "unfairly (e.g., missing documentation or undocumented misconduct in a high-risk case). "
            "Consider legal review."
        )
    else:
        st.markdown(
            "Punitive damages may apply in cases of bad faith or unfair treatment. Not indicated "
            "as a primary concern for this assessment based on the inputs provided."
        )

    # --- Dismissal Liability Timeline ---
    st.markdown("---")
    st.subheader("Dismissal Liability Timeline")

    today = datetime.now().date()
    # Ontario ESA: 1 week per year of service, minimum 0, max 8 weeks
    statutory_weeks = min(8.0, max(0.0, int(years_service)))
    end_statutory = today + timedelta(weeks=statutory_weeks)
    end_reasonable = today + timedelta(weeks=suggested_min_weeks)

    st.markdown(f"- **Date of Dismissal:** {today.strftime('%B %d, %Y')}")
    st.markdown(f"- **End of Statutory Notice Period:** {end_statutory.strftime('%B %d, %Y')} ({statutory_weeks:.0f} weeks)")
    st.markdown(f"- **End of Reasonable Notice Period:** {end_reasonable.strftime('%B %d, %Y')} ({suggested_min_weeks:.1f} weeks)")
    if punitive_applicable:
        st.markdown("- **Potential Punitive Damages Exposure:** ⚠️ Applicable — consider legal advice.")
    else:
        st.markdown("- **Potential Punitive Damages Exposure:** Not highlighted for this scenario.")

    st.caption(
        "This assessment is a simplified heuristic and does not replace professional legal advice. "
        "Always consult counsel for complex or high‑risk terminations."
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    

