import hashlib

import streamlit as st

from jd_parser import extract_requirements
from matcher import (
    calculate_similarity,
    calculate_match_score,
    calculate_targeted_scores,
)
from pdf_reader import extract_text_from_pdf
from recommendations import generate_recommendations
from resume_parser import parse_resume
from skills import compare_skills, extract_skills


st.set_page_config(
    page_title="AI Resume–Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background: #f4f7fb;
        color: #172033;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 1200px;
        padding: 2.5rem 2rem 4rem;
    }

    .hero {
        background: linear-gradient(135deg, #102a43, #1f5f8b);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 12px 30px rgba(16, 42, 67, 0.18);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,.15);
        border: 1px solid rgba(255,255,255,.25);
        border-radius: 999px;
        padding: .35rem .8rem;
        font-size: .78rem;
        font-weight: 600;
        letter-spacing: .04em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero h1 {
        color: white;
        font-size: 2.35rem;
        margin: 0 0 .65rem;
        font-weight: 700;
    }

    .hero p {
        color: #dbeafe;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 760px;
        margin: 0;
    }

    h2, h3, h4 {
        color: #172033 !important;
        font-weight: 700 !important;
    }

    [data-testid="stFileUploader"],
    [data-testid="stTextArea"] {
        background: white;
        border: 1px solid #dbe3ee;
        border-radius: 14px;
        padding: 1rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, .04);
    }

    [data-testid="stFileUploader"]:hover,
    [data-testid="stTextArea"]:focus-within {
        border-color: #2383c4;
        box-shadow: 0 0 0 3px rgba(35, 131, 196, .12);
    }

    .stButton > button {
        background: #1769aa;
        color: white;
        border: none;
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 600;
        transition: all .2s ease;
    }

    .stButton > button:hover {
        background: #0f568d;
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(23, 105, 170, .25);
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e1e8f0;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 5px 16px rgba(15, 23, 42, .05);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #1769aa;
        font-weight: 700;
    }

    .skill-tag,
    .missing-tag {
        display: inline-block;
        border-radius: 999px;
        padding: .42rem .8rem;
        margin: .22rem;
        font-size: .84rem;
        font-weight: 500;
    }

    .skill-tag {
        background: #e0f2fe;
        color: #075985;
        border: 1px solid #bae6fd;
    }

    .missing-tag {
        background: #fff7ed;
        color: #9a3412;
        border: 1px solid #fed7aa;
    }

    [data-testid="stExpander"] {
        background: white;
        border: 1px solid #e1e8f0;
        border-radius: 12px;
        margin-bottom: .7rem;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1769aa, #38a3a5);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border: none;
        border-top: 1px solid #dce5ef;
        margin: 2rem 0;
    }

    /* Light gray controls and panels */
    [data-testid="stFileUploader"],
    [data-testid="stTextArea"],
    [data-testid="stTextInput"],
    [data-testid="stExpander"],
    [data-testid="stMetric"],
    .stTextArea textarea,
    textarea {
        background-color: #f1f3f5 !important;
        color: #172033 !important;
        border-color: #d1d5db !important;
    }

    /* File uploader inner area */
    [data-testid="stFileUploader"] section {
        background-color: #f1f3f5 !important;
        border-color: #d1d5db !important;
    }

    /* File uploader browse button */
    [data-testid="stFileUploader"] button {
        background-color: #e2e5e9 !important;
        color: #172033 !important;
        border: 1px solid #c7ccd1 !important;
    }

    /* Expandable recommendation panels */
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {
        background-color: #f1f3f5 !important;
        color: #172033 !important;
    }

    /* Technical error/code boxes */
    .stCodeBlock,
    [data-testid="stCode"] {
        background-color: #e5e7eb !important;
        color: #172033 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_skill_tags(skills, css_class):
    if not skills:
        st.caption("None detected.")

    tags = "".join(
        f'<span class="{css_class}">{skill}</span>'
        for skill in skills
    )
    st.markdown(tags, unsafe_allow_html=True)


def render_recommendations(result):
    st.subheader("AI-Powered Recommendations")

    if result.get("error"):
        st.info(result["error"])
        return

    items = result.get("items", [])

    if not items:
        st.success("No additional recommendations are required.")
        return

    for item in items:
        skill = item.get("skill", "Missing requirement")

        with st.expander(skill.title(), expanded=True):
            st.markdown("**Why it matters**")
            st.write(item.get("why_it_matters", "Not provided."))

            st.markdown("**What to learn**")
            topics = item.get("what_to_learn", [])

            if isinstance(topics, list):
                for topic in topics:
                    st.markdown(f"- {topic}")
            else:
                st.write(topics)

            st.markdown("**Practical exercise or project**")
            st.write(item.get("practical_exercise", "Not provided."))

            st.markdown("**Resume evidence after learning it**")
            st.write(item.get("resume_evidence", "Not provided."))


st.markdown(
    """
    <section class="hero">
        <div class="hero-badge">AI Career Intelligence</div>
        <h1>AI Resume–Job Matcher</h1>
        <p>
            Understand how closely your resume aligns with a job description
            through semantic matching, skill-gap analysis, and actionable
            AI-powered recommendations.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.divider()

left, right = st.columns([1, 1.35], gap="large")

with left:
    st.subheader("Resume")
    resume_file = st.file_uploader(
        "Upload a PDF resume",
        type=["pdf"],
        help="Upload a text-based PDF resume.",
    )

with right:
    st.subheader("Job description")
    job_description = st.text_area(
        "Paste the job description",
        height=245,
        placeholder="Paste the complete job description here...",
        label_visibility="collapsed",
    )

analyze = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True,
)

if analyze:
    if resume_file is None:
        st.warning("Please upload a PDF resume.")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            with st.spinner("Extracting resume content and running analysis..."):
                resume_text = extract_text_from_pdf(resume_file)

                if not resume_text or not resume_text.strip():
                    raise ValueError(
                        "No readable text was found in the uploaded PDF."
                    )

                resume_sections = parse_resume(resume_text)
                requirements = extract_requirements(job_description)

                resume_skills = extract_skills(resume_text)
                job_skills = extract_skills(job_description)

                matching_skills, missing_skills = compare_skills(
                    resume_skills,
                    job_skills,
                )

                similarity = calculate_similarity(
                    resume_text,
                    job_description,
                )
                score = calculate_match_score(similarity)

                section_scores = calculate_targeted_scores(
                    resume_text,
                    resume_sections,
                    requirements,
                    job_description,
                )

                analysis_key = hashlib.sha256(
                    (
                        resume_text
                        + "\n"
                        + job_description
                    ).encode("utf-8")
                ).hexdigest()

                st.session_state.analysis = {
                    "score": score,
                    "matching_skills": matching_skills,
                    "missing_skills": missing_skills,
                    "section_scores": section_scores,
                    "analysis_key": analysis_key,
                }

                # The LLM is called only once for a new analysis.
                if missing_skills:
                    with st.spinner("Generating recommendations..."):
                        try:
                            st.session_state.recommendations = (
                                generate_recommendations(
                                    missing_skills,
                                    job_description,
                                )
                            )
                        except Exception as error:
                            st.session_state.recommendations = {
                                "items": [],
                                "error": (
                                    "The resume analysis completed, but "
                                    f"recommendations failed: {error}"
                                ),
                            }
                else:
                    st.session_state.recommendations = {
                        "items": [],
                        "error": None,
                    }

            st.success("Analysis completed.")

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                "Analysis failed while processing the uploaded resume."
            )
            st.info(
                "The PDF may be readable, but another analysis component "
                "failed. Check the technical message below."
            )
            st.code(f"{type(error).__name__}: {error}")


analysis = st.session_state.get("analysis")

if analysis:
    st.divider()
    st.subheader("Match Overview")
    st.caption(
        "A semantic similarity indicator between the resume and job description. "
        "It is not a hiring probability."
    )

    score_column, progress_column = st.columns([1, 3])

    with score_column:
        st.metric(
            "Resume–job similarity score",
            f"{analysis['score']}%",
        )

    with progress_column:
        st.caption(
            "Semantic similarity indicator. This is not a hiring probability "
            "or guarantee of job suitability."
        )
        st.progress(
            min(max(float(analysis["score"]) / 100, 0.0), 1.0)
        )

    st.divider()
    st.subheader("Skill-Gap Analysis")
    st.caption(
        "Skills detected in both documents and relevant requirements not found "
        "in the resume."
    )

    matching_column, missing_column = st.columns(2, gap="large")

    with matching_column:
        st.markdown("#### Matching Skills")
        render_skill_tags(
            analysis["matching_skills"],
            "skill-tag",
        )

    with missing_column:
        st.markdown("#### Missing Skills")
        render_skill_tags(
            analysis["missing_skills"],
            "missing-tag",
        )

    st.divider()
    st.subheader("Section-Wise Matching")
    st.caption(
        "Scores are calculated only for resume sections that were successfully "
        "detected."
    )

    section_scores = analysis["section_scores"]

    if section_scores:
        score_columns = st.columns(len(section_scores))

        for column, (section, section_score) in zip(
            score_columns,
            section_scores.items(),
        ):
            with column:
                st.metric(section.title(), f"{section_score}%")
                st.progress(
                    min(max(float(section_score) / 100, 0.0), 1.0)
                )
    else:
        st.info(
            "Section scores are unavailable because the required resume "
            "sections or job requirements could not be parsed."
        )

    st.divider()

    if analysis["missing_skills"]:
        render_recommendations(
            st.session_state.get(
                "recommendations",
                {
                    "items": [],
                    "error": "Recommendations are unavailable.",
                },
            )
        )
    else:
        st.subheader("AI-Powered Recommendations")
        st.success(
            "No missing skills were detected, so no LLM request was made."
        )

        st.subheader("AI-Powered Recommendations")
        st.caption(
            "Personalized learning priorities and practical project ideas based on "
            "the requirements missing from your resume."
        )