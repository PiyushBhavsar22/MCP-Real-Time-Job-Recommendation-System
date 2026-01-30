import streamlit as st
from src.helper import ask_openai, extract_text_from_pdf
from src.job_api import fetch_linkedin_jobs, fetch_indeed_jobs

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("AI Job Recommender")
st.markdown("Upload the resume and get job recommendation based on the skills and experience from LinkedIN and Indeed")

uploaded_file = st.file_uploader("Upload the resume PDF", type=["PDF"])

if uploaded_file:
    with st.spinner("Extracting thext from Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing the Resume..."):
        summary = ask_openai(f"Summarize the Resume highlighting the skills, education, and experience: \n\n{resume_text}", max_tokens=500)

    with st.spinner("Finding Skill gaps..."):
        gaps = ask_openai(f"Analyze this resume and highlight missing skills, certification, and experience needed for better job opportunities: \n\n{resume_text}", max_tokens=500)

    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_openai(f"Based on the resume suggest a future roadmap to improve industry exposure: \n\n{resume_text}", max_tokens=500)

    # Diplay the Result
    st.markdown("---")
    st.header(" Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header(" Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header(" Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success(" Analysis Completed Successfully!")

    if st.button("Get Job Recommendation"):
        with st.spinner("Fetching job recommendation..."):
            keywords = ask_openai(
                f"Based on the Resume summary, suggest the best job titles and keywords for searching job. Give a comma-separated list only, no explanation. \n\nSummary: {summary}",
                max_tokens=200
            )

            search_keywords_clean = keywords.replace("\n", "").strip()

        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=80)
            indeed_jobs = fetch_indeed_jobs(search_keywords_clean, rows=80)

        st.markdown("---")
        st.header("Top LinkedIn Jobs")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f"- [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")

        st.markdown("---")
        st.header("Top Naukri Jobs (India)")

        if indeed_jobs:
            for job in indeed_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- {job.get('location')}")
                st.markdown(f"- [View Job]({job.get('url')})")
                st.markdown("---")
        else:
            st.warning("No Naukri jobs found.")