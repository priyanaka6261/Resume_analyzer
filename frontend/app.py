import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")

# ---------- SESSION STATE ----------
if "total_resumes" not in st.session_state:
    st.session_state.total_resumes = 0

if "analyzed_candidates" not in st.session_state:
    st.session_state.analyzed_candidates = 0

if "processing_time" not in st.session_state:
    st.session_state.processing_time = 0

if "match_score" not in st.session_state:
    st.session_state.match_score = 0

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = set()

# ---------- SIDEBAR ----------
st.sidebar.title("🧠 ATS Analyzer")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Resume Analyzer"])

# Reset button
if st.sidebar.button("🔄 Reset Dashboard"):
    st.session_state.total_resumes = 0
    st.session_state.analyzed_candidates = 0
    st.session_state.processing_time = 0
    st.session_state.match_score = 0
    st.session_state.uploaded_files = set()
    st.success("Dashboard reset successfully")

# ---------- HEADER ----------
st.title("🚀 ATS Resume Analyzer")
st.caption("AI-powered recruitment insights and candidate analysis")

# ---------- DASHBOARD ----------
if menu == "Dashboard":

    st.subheader("Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Resumes", st.session_state.total_resumes)

    with col2:
        st.metric("Analyzed Candidates", st.session_state.analyzed_candidates)

    with col3:
        st.metric("Match Score", f"{st.session_state.match_score}%")

    with col4:
        st.metric("Processing Time", f"{st.session_state.processing_time}s")

    st.info("Upload resumes to see analytics")

# ---------- RESUME ANALYZER ----------
if menu == "Resume Analyzer":

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

    if uploaded_file:

        file_name = uploaded_file.name

        # Only count if new file
        if file_name not in st.session_state.uploaded_files:

            start_time = time.time()

            with st.spinner("Analyzing resume..."):
                requests.post(f"{BACKEND_URL}/upload",
                              files={"file": uploaded_file})

            end_time = time.time()

            st.session_state.uploaded_files.add(file_name)
            st.session_state.total_resumes += 1
            st.session_state.analyzed_candidates += 1
            st.session_state.processing_time = round(end_time - start_time, 2)

            # Simple demo score
            st.session_state.match_score = 80

            st.success("Resume uploaded successfully")

        else:
            st.warning("This resume is already uploaded")

    # ---------- ASK QUESTION ----------
    st.subheader("💬 Ask Question")

    question = st.text_input("Ask about resume")

    if st.button("Analyze"):
        if question:
            with st.spinner("Generating insights..."):
                res = requests.get(f"{BACKEND_URL}/query",
                                   params={"question": question})
                answer = res.json().get("answer", "No answer generated")

            st.success(answer)
        else:
            st.warning("Please enter a question")
