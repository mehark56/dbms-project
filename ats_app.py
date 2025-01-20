

#pip install PyPDF2 python-dotenv google-generativeai
##pip install openai

import nltk
nltk.download('punkt')
nltk.data.path.append('/usr/share/nltk_data')


# Install required libraries
#pip install openai pdfplumber nltk -q

# Import required libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pdfplumber
import openai
import re
import streamlit as st
import PyPDF2


# Download NLTK dependencies
nltk.download('punkt_tab')  # Punkt tokenizer
nltk.download('stopwords')  # Stopwords for preprocessing

# Ensure the NLTK path is set correctly
nltk.data.path.append('/usr/share/nltk_data')

# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual API key

# Function to extract text from a PDF resume
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to calculate ATS score based on job description
def calculate_ats_score(resume_text, job_description):
    # Preprocess the text
    resume_tokens = word_tokenize(resume_text.lower())
    job_description_tokens = word_tokenize(job_description.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    resume_tokens = [word for word in resume_tokens if word not in stop_words and word.isalnum()]
    job_description_tokens = [word for word in job_description_tokens if word not in stop_words and word.isalnum()]

    # Calculate match score
    common_tokens = set(resume_tokens) & set(job_description_tokens)
    ats_score = len(common_tokens) / len(set(job_description_tokens)) * 100 if len(job_description_tokens) > 0 else 0
    return round(ats_score, 2)

# Streamlit interface
st.title('ATS Resume Scorer')

# Upload the resume (PDF) and input the job description
#from google.colab import files

# Upload resume file (PDF)
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)

    st.write("### Resume Text Preview")
    st.write(resume_text[:1000])  # Display a preview of the first 1000 characters of the resume text

    # Input job description
    job_description = st.text_area("Enter the job description:")

    if st.button('Calculate ATS Score'):
        if resume_text and job_description:
            ats_score = calculate_ats_score(resume_text, job_description)
            st.write(f"**ATS Score**: {ats_score}%")
        else:
            st.warning("Please upload a resume and enter a job description.")
