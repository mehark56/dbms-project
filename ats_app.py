import nltk
import streamlit as st
import pdfplumber
import openai
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image

# Download NLTK dependencies
nltk.download('punkt')  # Punkt tokenizer
nltk.download('stopwords')  # Stopwords for preprocessing

# Ensure the NLTK path is set correctly
nltk.data.path.append('/usr/share/nltk_data')

# Streamlit App Title with Styling
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📄 ATS Resume Scorer</h1>
""", unsafe_allow_html=True)

# Function to extract text from a PDF resume
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

# Function to calculate ATS score based on job description
def calculate_ats_score(resume_text, job_description):
    resume_tokens = word_tokenize(resume_text.lower())
    job_description_tokens = word_tokenize(job_description.lower())

    stop_words = set(stopwords.words('english'))
    resume_tokens = [word for word in resume_tokens if word not in stop_words and word.isalnum()]
    job_description_tokens = [word for word in job_description_tokens if word not in stop_words and word.isalnum()]

    common_tokens = set(resume_tokens) & set(job_description_tokens)
    ats_score = len(common_tokens) / len(set(job_description_tokens)) * 100 if len(job_description_tokens) > 0 else 0
    return round(ats_score, 2)

# Upload resume file (PDF)
st.sidebar.header("📂 Upload Resume")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.sidebar.success("✅ Resume uploaded successfully!")
    
    st.markdown("""
        <h3 style='color: #2196F3;'>📄 Resume Text Preview</h3>
    """, unsafe_allow_html=True)
    st.text_area("", resume_text[:1000], height=200)

    # Input job description
    job_description = st.text_area("📝 Enter the Job Description")

    # Calculate ATS Score
    if st.button('⚡ Calculate ATS Score'):
        if resume_text and job_description:
            ats_score = calculate_ats_score(resume_text, job_description)
            st.markdown(f"""
                <h2 style='text-align: center; color: #FF9800;'>🎯 ATS Score: {ats_score}%</h2>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please upload a resume and enter a job description.")

# Footer with Heart and RVCE branding
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>Made with ❤️ in RVCE</p>
""", unsafe_allow_html=True)
