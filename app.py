# # --- Required Libraries ---
# import base64
# import io
# import os
# import platform
# import google.generativeai as genai
# import pdf2image
# import streamlit as st
# from dotenv import load_dotenv
# from pdfminer.high_level import extract_text

# # --- Load API Key from .env file ---
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # --- Gemini API Call Function ---
# def get_gemini_response(input_text, pdf_content, prompt):
#     try:
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         response = model.generate_content([input_text, pdf_content[0], prompt])
#         return response.text
#     except Exception as e:
#         return f"Error fetching response from Gemini API: {e}"

# # --- Extract Skills from Job Description using Gemini ---
# def extract_dynamic_skills_from_jd(job_description):
#     """
#     Ask Gemini to pull out top 5 skills from the job description.
#     We'll use these to show job suggestions later.
#     """
#     try:
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         skill_prompt = f"""
#         You are a professional recruiter. From the following job description, extract the top 5 core skills required for the job.
#         Only return a comma-separated list of 5 skills. No explanation needed.

#         Job Description:
#         {job_description}
#         """
#         response = model.generate_content(skill_prompt)
#         skills = response.text.strip().split(",")
#         return [skill.strip() for skill in skills][:5]
#     except:
#         return []

# # --- Generate Job Search URLs ---
# def get_job_search_links(skills):
#     """
#     Take the top skills and generate job search links
#     for LinkedIn, Indeed, and Glassdoor.
#     """
#     platforms = {
#         "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords=",
#         "Indeed": "https://www.indeed.com/jobs?q=",
#         "Glassdoor": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword="
#     }

#     links = []
#     for idx, (platform, base_url) in enumerate(platforms.items()):
#         if idx < len(skills):
#             skill = skills[idx]
#             encoded = skill.replace(" ", "+")  # Make it URL-friendly
#             full_url = f"{base_url}{encoded}"
#             links.append((platform, skill, full_url))
#     return links

# # --- Handle PDF Upload: Convert First Page to Image + Extract Text ---
# def input_pdf_setup(uploaded_file):
#     try:
#         pdf_bytes = uploaded_file.read()

#         # Detect OS
#         system_platform = platform.system()

#         if system_platform == "Windows":
#             poppler_path = r"C:\Program Files (x86)\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin"
#             images = pdf2image.convert_from_bytes(pdf_bytes, poppler_path=poppler_path)
#         else:
#             images = pdf2image.convert_from_bytes(pdf_bytes)

#         # Convert first page to JPEG
#         first_page = images[0]
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         # Extract text from PDF
#         resume_text = extract_text(io.BytesIO(pdf_bytes))

#         # Prepare image part for Gemini input
#         pdf_parts = [{
#             "mime_type": "image/jpeg",
#             "data": base64.b64encode(img_byte_arr).decode()
#         }]
#         return pdf_parts, resume_text
#     except Exception as e:
#         st.error(f"Error processing PDF: {e}")
#         return None, None


# # --- Streamlit UI Setup ---
# st.set_page_config(page_title="AI Recruiter")
# st.header("📄 AI Recruiter: Smart ATS with Google Gemini 1.5")

# # --- Input Fields ---
# input_text = st.text_area("📝 Paste Job Description Here")
# uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF)", type=["pdf"])

# # Let the user know resume was received
# if uploaded_file:
#     st.success("✅ Resume uploaded successfully!")

# # --- Action Buttons ---
# submit1 = st.button("🧐 Analyze Resume")
# submit3 = st.button("📊 Percentage Match")

# # --- Prompts Sent to Gemini ---
# prompt_eval = """
# You are an experienced HR expert. Evaluate the candidate's resume for the given job. 
# Mention strengths, weaknesses, and whether the candidate is a fit. Be clear and concise.
# """

# prompt_match = """
# Evaluate the resume against the job description and give a percentage match, missing keywords, 
# and an overall summary of alignment.
# """

# # --- If "Analyze Resume" Button is Pressed ---
# if submit1:
#     if uploaded_file:
#         pdf_content, resume_text = input_pdf_setup(uploaded_file)
#         if pdf_content:
#             combined_input = f"Job Description:\n{input_text}\n\nResume:\n{resume_text}"
#             st.info("⏳ Evaluating resume using Gemini...")
#             response = get_gemini_response(combined_input, pdf_content, prompt_eval)
#             st.subheader("📋 Resume Evaluation:")
#             st.write(response)

#             # Generate and Show Job Links based on Skills from JD
#             skills = extract_dynamic_skills_from_jd(input_text)
#             job_links = get_job_search_links(skills)
#             if job_links:
#                 st.subheader("🔗 Job Suggestions (Based on Job Description):")
#                 for platform, skill, url in job_links:
#                     st.markdown(f"- **{platform} – {skill}** → [View Jobs]({url})")
#             else:
#                 st.warning("⚠️ No skills extracted from the job description.")
#         else:
#             st.error("❌ Could not process resume.")

# # --- If "Percentage Match" Button is Pressed ---
# if submit3:
#     if uploaded_file:
#         pdf_content, resume_text = input_pdf_setup(uploaded_file)
#         if pdf_content:
#             combined_input = f"Job Description:\n{input_text}\n\nResume:\n{resume_text}"
#             st.info("⏳ Matching Resume with Job Description...")
#             response = get_gemini_response(combined_input, pdf_content, prompt_match)
#             st.subheader("📊 Match Percentage:")
#             st.write(response)
#         else:
#             st.error("❌ Could not process resume.")


# --- Required Libraries ---
import base64
import io
import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from pdfminer.high_level import extract_text

# --- Load API Key from .env file ---
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

# --- Extract Skills from Job Description using Gemini ---
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

# --- Generate Job Search URLs ---
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

# --- Handle PDF Upload: Extract Text Only ---
def input_pdf_setup(uploaded_file):
    try:
        pdf_bytes = uploaded_file.read()
        resume_text = extract_text(io.BytesIO(pdf_bytes))
        return resume_text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# --- Streamlit UI Setup ---
st.set_page_config(page_title="AI Recruiter")
st.header("📄 AI Recruiter: Smart ATS with Google Gemini 1.5")

# --- Input Fields ---
input_text = st.text_area("📝 Paste Job Description Here")
uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

# --- Action Buttons ---
submit1 = st.button("🧐 Analyze Resume")
submit3 = st.button("📊 Percentage Match")

# --- Prompts Sent to Gemini ---
prompt_eval = """
You are an experienced HR expert. Evaluate the candidate's resume for the given job. 
Mention strengths, weaknesses, and whether the candidate is a fit. Be clear and concise.
"""

prompt_match = """
Evaluate the resume against the job description and give a percentage match, missing keywords, 
and an overall summary of alignment.
"""

# --- Analyze Resume Button ---
if submit1:
    if uploaded_file:
        resume_text = input_pdf_setup(uploaded_file)
        if resume_text:
            combined_input = f"Job Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.info("⏳ Evaluating resume using Gemini...")
            response = get_gemini_response(combined_input, prompt_eval)
            st.subheader("📋 Resume Evaluation:")
            st.write(response)

            skills = extract_dynamic_skills_from_jd(input_text)
            job_links = get_job_search_links(skills)
            if job_links:
                st.subheader("🔗 Job Suggestions (Based on Job Description):")
                for platform, skill, url in job_links:
                    st.markdown(f"- **{platform} – {skill}** → [View Jobs]({url})")
            else:
                st.warning("⚠️ No skills extracted from the job description.")
        else:
            st.error("❌ Could not process resume.")

# --- Percentage Match Button ---
if submit3:
    if uploaded_file:
        resume_text = input_pdf_setup(uploaded_file)
        if resume_text:
            combined_input = f"Job Description:\n{input_text}\n\nResume:\n{resume_text}"
            st.info("⏳ Matching Resume with Job Description...")
            response = get_gemini_response(combined_input, prompt_match)
            st.subheader("📊 Match Percentage:")
            st.write(response)
        else:
            st.error("❌ Could not process resume.")
