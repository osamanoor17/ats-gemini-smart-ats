# --- Required Libraries ---
import base64
import io
import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
from docx import Document

# --- Load API Key ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Gemini API Call Function ---
def get_gemini_response(input_text, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, prompt])
        return response.text
    except Exception as e:
        return f"Error fetching response from Gemini API: {e}"

# --- Extract Skills from JD ---
def extract_dynamic_skills_from_jd(job_description):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        skill_prompt = f"""
        You are a professional recruiter. From the following job description, extract the top 5 core skills required for the job.
        Only return a comma-separated list of 5 skills. No explanation needed.

        Job Description:
        {job_description}
        """
        response = model.generate_content(skill_prompt)
        skills = response.text.strip().split(",")
        return [skill.strip() for skill in skills][:5]
    except:
        return []

# --- Generate Job Links ---
def get_job_search_links(skills):
    platforms = {
        "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords=",
        "Indeed": "https://www.indeed.com/jobs?q=",
        "Glassdoor": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword="
    }

    links = []
    for idx, (platform, base_url) in enumerate(platforms.items()):
        if idx < len(skills):
            skill = skills[idx]
            encoded = skill.replace(" ", "+")
            full_url = f"{base_url}{encoded}"
            links.append((platform, skill, full_url))
    return links

# --- Resume Text Extractor (PDF, DOCX, TXT) ---
def extract_text_from_file(uploaded_file):
    try:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            pdf_bytes = uploaded_file.read()
            return extract_text(io.BytesIO(pdf_bytes))

        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_file.name.endswith(".docx"):
            docx_bytes = uploaded_file.read()
            doc = Document(io.BytesIO(docx_bytes))
            full_text = [para.text for para in doc.paragraphs]
            return "\n".join(full_text)

        elif file_type == "text/plain" or uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
            return text

        else:
            st.error("Unsupported file format. Please upload PDF, DOCX, or TXT.")
            return None

    except Exception as e:
        st.error(f"\u274c Error processing file: {e}")
        return None

# --- UI Config ---
st.set_page_config(page_title="AI Recruiter", page_icon="🤖", layout="centered")

# --- Background Style ---
def set_background():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #d4fc79, #96e6a1, #a1c4fd, #c2e9fb);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 30px 25px;
        border-radius: 20px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    .main-title {
        text-align: center;
        color: #003049;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 20px;
        margin-top: 0;
    }
    .stTextArea label, .stFileUploader label {
        font-weight: bold;
        color: #003049;
    }
    textarea, input[type="text"] {
        border: 1px solid rgba(0, 0, 0, 0.2) !important;
        border-radius: 8px !important;
    }
    textarea:focus, input[type="text"]:focus {
        border: 1.5px solid #118ab2 !important;
        outline: none;
    }
    button[kind="primary"] {
        background-color: #118ab2;
        color: white;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
    }
    button[kind="primary"]:hover {
        background-color: #073b4c;
    }
    section[data-testid="stFileUploader"] > div {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

set_background()

# --- Header ---
st.markdown('<div class="main-title">🤖 AI Recruiter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Smart ATS powered by Google Gemini 1.5 Flash</div><br>', unsafe_allow_html=True)

# --- JD Input ---
st.markdown("### 📝 Add Job Description")
input_text = st.text_area("Paste your job description below:", height=150)


# --- Resume Upload ---

st.markdown("### 📎 Upload Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
if uploaded_file:
    st.toast("Resume uploaded successfully!", icon="📄")

# --- Buttons ---

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("🧐 Analyze Resume")
with col2:
    submit3 = st.button("📊 Match Percentage")


# --- Prompts ---
prompt_eval = """
You are an experienced HR expert. Evaluate the candidate's resume for the given job. 
Mention strengths, weaknesses, and whether the candidate is a fit. Be clear and concise.
"""
prompt_match = """
Evaluate the resume against the job description and give a percentage match, missing keywords, 
and an overall summary of alignment.
"""

# --- Button Logic ---
if submit1:
    if not input_text.strip():
        st.warning("⚠️ Please paste the Job Description before analyzing.")
    elif not uploaded_file:
        st.warning("⚠️ Please upload your resume before analyzing.")
    else:
        resume_text = extract_text_from_file(uploaded_file)
        if resume_text:
            combined_input = f"Job Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.info("⏳ Evaluating resume using Gemini...")
            response = get_gemini_response(combined_input, prompt_eval)
            st.markdown("---")
            st.subheader("📋 Resume Evaluation")
            st.write(response)

            skills = extract_dynamic_skills_from_jd(input_text)
            job_links = get_job_search_links(skills)
            if job_links:
                st.subheader("🔗 Job Suggestions Based on JD")
                for platform, skill, url in job_links:
                    st.markdown(f"- **{platform} – {skill}** → [View Jobs]({url})")
            else:
                st.warning("⚠️ No skills extracted from the job description.")
        else:
            st.error("❌ Could not process resume.")

if submit3:
    if not input_text.strip():
        st.warning("⚠️ Please paste the Job Description before matching.")
    elif not uploaded_file:
        st.warning("⚠️ Please upload your resume before matching.")
    else:
        resume_text = extract_text_from_file(uploaded_file)
        if resume_text:
            combined_input = f"Job Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.info("⏳ Calculating match percentage...")
            response = get_gemini_response(combined_input, prompt_match)
            st.markdown("---")
            st.subheader("📊 Match Result")
            st.write(response)
        else:
            st.error("❌ Could not process resume.")
