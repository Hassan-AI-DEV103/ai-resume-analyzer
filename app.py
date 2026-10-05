import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume & Job Match Analyzer")
st.write("Upload your resume and compare it with a job description.")

# Skills our analyzer can detect
SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "computer vision",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "flask",
    "fastapi",
    "streamlit",
    "html",
    "css",
    "javascript",
    "react",
    "power bi",
    "tableau",
    "excel",
    "data analysis",
    "data science",
    "generative ai",
    "llm",
    "chatbot",
]

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def find_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill)

    return found_skills


# Sidebar
st.sidebar.header("How it works")
st.sidebar.write("1. Upload your resume PDF")
st.sidebar.write("2. Paste the job description")
st.sidebar.write("3. Click Analyze")
st.sidebar.write("4. See matched and missing skills")


# Resume upload
uploaded_resume = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# Job description
job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)

# Analyze button
if st.button("🔍 Analyze Resume", type="primary"):

    if uploaded_resume is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please paste a job description.")

    else:
        with st.spinner("Analyzing your resume..."):

            resume_text = extract_pdf_text(uploaded_resume)

            resume_skills = find_skills(resume_text)
            job_skills = find_skills(job_description)

            matched_skills = [
                skill for skill in job_skills
                if skill in resume_skills
            ]

            missing_skills = [
                skill for skill in job_skills
                if skill not in resume_skills
            ]

            if job_skills:
                match_percentage = (
                    len(matched_skills) / len(job_skills)
                ) * 100
            else:
                match_percentage = 0

        st.success("Analysis complete! 🎉")

        # Match score
        st.subheader("📊 Resume Match Score")
        st.progress(int(match_percentage))

        st.metric(
            "Job Match",
            f"{match_percentage:.0f}%"
        )

        # Results columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.write(f"✅ {skill.title()}")
            else:
                st.write("No matching skills found.")

        with col2:
            st.subheader("❌ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"❌ {skill.title()}")
            else:
                st.write("Great! No missing skills detected. 🎯")

        # Suggestions
        st.subheader("💡 Suggestions")

        if missing_skills:
            st.write(
                "Consider learning or highlighting these skills "
                "in your resume if you genuinely have them:"
            )

            for skill in missing_skills:
                st.write(f"• {skill.title()}")
        else:
            st.write(
                "Your detected skills match the job description well. "
                "Make sure your resume clearly demonstrates them."
            )