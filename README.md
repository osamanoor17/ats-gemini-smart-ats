# 🤖 AI Recruiter: Smart ATS using Google Gemini 1.5 Flash

AI Recruiter is an advanced, intelligent Application Tracking System (ATS) built with Google Gemini 1.5 Flash LIM Model. This tool helps recruiters analyze resumes, match them with job descriptions, and suggest relevant jobs—all in one place.

---

## 🚀 Features

- 🔍 **Resume Evaluation** — Gemini analyzes uploaded resumes against job descriptions and provides feedback on strengths, weaknesses, and fit.
- 📊 **Percentage Match** — Get an approximate match score between a resume and job description.
- 💼 **Job Suggestions** — Suggests job openings from LinkedIn, Indeed, and Glassdoor based on required skills from the JD.
- 📎 **PDF Resume Parsing** — Parses the uploaded PDF resume's content for evaluation.
- 💡 **Dynamic Skill Extraction** — Automatically extracts relevant skills using Gemini based on the provided JD.

---

## 🛠️ Tech Stack

- **Google Gemini 1.5 Flash** — Core NLP model for evaluation and reasoning.
- **Python** — Main programming language.
- **Streamlit** — For building a clean and interactive UI.
- **pdfminer** — For extracting text from resumes.
- **pdf2image** — Converts PDF to image (used in Gemini input format).
- **dotenv** — For managing API keys securely.

---

## 📂 Directory Structure

```

📁 ats-gemini-smart-ats/
│
├── app.py                 # Main Streamlit App
├── requirements.txt       # All required packages
├── README.md              # You’re reading it!
└── .env                   # Environment variables (add your Google API Key)

````

---

## ⚙️ Installation Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ats-gemini-smart-ats.git
   cd ats-gemini-smart-ats

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # for Windows
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API key in `.env` file:**

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the app:**

   ```bash
   streamlit run app.py
   ```

---

## 🧪 How to Use

1. Paste a **Job Description** in the text area.
2. Upload your **Resume (PDF format)**.
3. Click on:

   * 🔍 "Analyze Resume" — to get a summary of fit.
   * 📊 "Percentage Match" — to get a numerical fit score.
4. Get **job suggestions** from top job platforms based on JD.

---

## 🙌 Contributing

Want to contribute?

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

Made with 💻 by **Muhammad Osama Noor**
📧 [mosamanoor17@gmail.com](mailto:mosamanoor17@gmail.com)

```
