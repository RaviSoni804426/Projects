import streamlit as st
import fitz  # PyMuPDF
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os

# Set page config
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")

st.title("📄 AI Resume Screener")
st.markdown("Upload a resume (PDF) and provide a job description to get an AI-powered screening report.")

# Load Model (Cached for performance)
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, low_cpu_mem_usage=True)
    model.to("cpu")
    return tokenizer, model

tokenizer, model = load_model()

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def rule_based_score(resume_text, required_skills, nice_to_have):
    resume_text_lower = resume_text.lower()
    score = 0
    found_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text_lower:
            score += 10
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    for skill in nice_to_have:
        if skill.lower() in resume_text_lower:
            score += 5
            found_skills.append(skill)

    final_score = min(score, 100)
    recommendation = "Interview" if final_score >= 60 else "Reject"
    return {
        "score": final_score,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }

def generate_reasoning(resume_text, job_description, rule_result):
    prompt = f"""
    You are a technical recruiter.
    Job Description: {job_description}
    Resume Summary: {resume_text[:1000]}
    Score: {rule_result['score']}
    Found Skills: {rule_result['found_skills']}
    Recommendation: {rule_result['recommendation']}
    
    In 2 sentences, explain why the candidate should be {rule_result['recommendation']}.
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model.generate(**inputs, max_new_tokens=120, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# UI Layout
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description Here", height=200)

req_skills_input = st.text_input("Required Skills (comma separated)", "Python, SQL, Machine Learning")
nice_skills_input = st.text_input("Nice to Have Skills (comma separated)", "AWS, NLP, Cloud")

if st.button("Screen Resume"):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
            req_skills = [s.strip() for s in req_skills_input.split(",")]
            nice_skills = [s.strip() for s in nice_skills_input.split(",")]
            
            rule_result = rule_based_score(resume_text, req_skills, nice_skills)
            reasoning = generate_reasoning(resume_text, job_desc, rule_result)
            
            # Display Results
            st.divider()
            st.header("Screening Report")
            
            col1, col2 = st.columns(2)
            col1.metric("Score", f"{rule_result['score']}/100")
            col2.success(f"Recommendation: {rule_result['recommendation']}") if rule_result['recommendation'] == "Interview" else col2.error(f"Recommendation: {rule_result['recommendation']}")
            
            st.subheader("Skills Analysis")
            st.write(f"✅ **Found Skills:** {', '.join(rule_result['found_skills'])}")
            st.write(f"❌ **Missing Skills:** {', '.join(rule_result['missing_skills'])}")
            
            st.subheader("AI Reasoning")
            st.info(reasoning)
    else:
        st.warning("Please upload a resume and provide a job description.")
