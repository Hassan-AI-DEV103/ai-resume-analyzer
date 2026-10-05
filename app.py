
import re

import streamlit as st
from pypdf import PdfReader


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume & Job Match Analyzer",
    page_icon="📄",
    layout="wide",
)

# -----------------------------
# Custom styling
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .score-card {
        padding: 25px;
        border-radius: 15px;
        background: #f5f7fa;
        text-align: center;
        margin-bottom: 20px;
    }

    .score-number {
        font-size: 52px;
        font-weight: 700;
    }

    .skill-card {
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-weight: 500;
    }

    .matched {
        background: #e8f5e9;
        border-left: 5px solid #2e7d32;
    }

    .missing {
        background: #ffebee;
        border-left: 5px solid #c62828;
    }

    .info-box {
        padding: 18px;
        border-radius: 12px;
        background: #eef4ff;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">📄 AI Resume & Job Match Analyzer</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Compare your resume with a job description and discover your skill gaps.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("📌 How it works")

    st.write("1. Upload your resume PDF")
    st.write("2. Paste a job description")
    st.write("3. Click **Analyze Resume**")
    st.write("4. Review your match score and skill gaps")

    st.divider()

    st.info(
        "💡 Tip: Use a job description that matches the type of role you want."
    )

# -----------------------------
# Skill database
# -----------------------------
SKILLS = [
    "Python",
    "SQL",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "OpenCV",
    "Git",
    "GitHub",
    "Streamlit",
    "FastAPI",
    "Flask",
    "Docker",
    "AWS",
    "Azure",
    "Power BI",
    "Tableau",
    "Excel",
    "Generative AI",
    "LLM",
    "LangChain",
]


# -----------------------------
# Functions
# -----------------------------
def extract_pdf_text(uploaded_file):
    """Extract text from an uploaded PDF."""
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def find_skills(text):
    """Find predefined skills in text."""
    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


# -----------------------------
# Main input section
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload your resume in PDF format.",
    )

with col2:
    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder="Example: We are looking for a Python Developer with experience in Python, SQL, Pandas, Machine Learning and Git...",
    )

st.write("")

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True,
)

# -----------------------------
# Analysis
# -----------------------------
if analyze_button:

    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume PDF first.")

    elif not job_description.strip():
        st.warning("⚠️ Please paste a job description first.")

    else:

        with st.spinner("Analyzing your resume..."):

            try:
                resume_text = extract_pdf_text(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "❌ Could not extract readable text from this PDF."
                    )
                    st.stop()

                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)

                if not job_skills:
                    st.warning(
                        "⚠️ No supported technical skills were detected in the job description."
                    )
                    st.stop()

                matched_skills = [
                    skill for skill in job_skills
                    if skill in resume_skills
                ]

                missing_skills = [
                    skill for skill in job_skills
                    if skill not in resume_skills
                ]

                match_percentage = round(
                    (len(matched_skills) / len(job_skills)) * 100
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
                st.stop()

        # -----------------------------
        # Results
        # -----------------------------
        st.divider()

        st.subheader("📊 Resume Analysis Results")

        score_col, stats_col = st.columns([1, 2])

        with score_col:

            st.markdown(
                f"""
                <div class="score-card">
                    <div>Resume Match Score</div>
                    <div class="score-number">{match_percentage}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with stats_col:

            metric1, metric2, metric3 = st.columns(3)

            with metric1:
                st.metric(
                    "Job Skills",
                    len(job_skills),
                )

            with metric2:
                st.metric(
                    "Matched",
                    len(matched_skills),
                )

            with metric3:
                st.metric(
                    "Missing",
                    len(missing_skills),
                )

        # -----------------------------
        # Progress bar
        # -----------------------------
        st.progress(
            match_percentage / 100,
            text=f"Job Match: {match_percentage}%",
        )

        st.write("")

        # -----------------------------
        # Skills sections
        # -----------------------------
        matched_col, missing_col = st.columns(2)

        with matched_col:

            st.subheader("✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:

                    st.markdown(
                        f"""
                        <div class="skill-card matched">
                            ✅ {skill}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:
                st.info("No matching skills were detected.")

        with missing_col:

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.markdown(
                        f"""
                        <div class="skill-card missing">
                            ❌ {skill}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:
                st.success("🎉 Great! No missing skills detected.")

        # -----------------------------
        # Suggestions
        # -----------------------------
        st.divider()

        st.subheader("💡 Improvement Suggestions")

        if missing_skills:

            st.markdown(
                '<div class="info-box">',
                unsafe_allow_html=True,
            )

            st.write(
                "Consider adding relevant experience, projects, or "
                "learning evidence for these skills:"
            )

            for skill in missing_skills:
                st.write(f"• **{skill}**")

            st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.success(
                "Your resume contains all the detected skills from this job description!"
            )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Built with Python, Streamlit and PyPDF • AI Resume & Job Match Analyzer"
)

