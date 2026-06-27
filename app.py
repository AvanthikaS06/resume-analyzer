import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import load_skills, extract_skills
from utils.scorer import calculate_match_score
from utils.ats_checker import check_ats_score

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and paste a job description to get an instant match report.")

# ── Input Section ─────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

with col2:
    st.subheader("📋 Paste Job Description")
    jd_text = st.text_area("Job Description", height=250,
                            placeholder="Paste the full job description here...")


analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True, type="primary")

# ── Analysis ──────────────────────────────────────────────
if analyze_btn:
    if not uploaded_file:
        st.error("Please upload a resume PDF.")
    elif not jd_text.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text   = extract_text_from_pdf(uploaded_file)
            skills_db     = load_skills()
            resume_skills = extract_skills(resume_text, skills_db)
            jd_skills     = extract_skills(jd_text, skills_db)
            score, matched, missing = calculate_match_score(resume_skills, jd_skills)
            ats_score, ats_checks   = check_ats_score(resume_text)

        st.divider()

        # ── Metrics ───────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🎯 Match Score",    f"{score}%")
        m2.metric("✅ Skills Matched", len(matched))
        m3.metric("❌ Skills Missing", len(missing))
        m4.metric("🏢 ATS Score",      f"{ats_score}/100")

        st.divider()

        # ── Charts Row ────────────────────────────────────
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Skill Match Breakdown")
            fig = go.Figure(go.Pie(
                values=[len(matched), len(missing)],
                labels=["Matched", "Missing"],
                hole=0.5,
                marker_colors=["#4CAF50", "#F44336"]
            ))
            fig.update_layout(margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("☁️ Resume Keyword Cloud")
            if resume_text:
                wc = WordCloud(width=600, height=300,
                               background_color="white",
                               colormap="Blues").generate(resume_text)
                fig2, ax = plt.subplots(figsize=(6, 3))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig2)

        st.divider()

        # ── Skills Detail ─────────────────────────────────
        s1, s2 = st.columns(2)
        with s1:
            st.subheader("✅ Matched Skills")
            if matched:
                for skill in sorted(matched):
                    st.success(f"  {skill}")
            else:
                st.info("No matching skills found.")

        with s2:
            st.subheader("❌ Missing Skills")
            if missing:
                for skill in sorted(missing):
                    st.error(f"  {skill}")
            else:
                st.info("No missing skills — great match!")

        st.divider()

        # ── ATS Checklist ─────────────────────────────────
        st.subheader("🏢 ATS Checklist")
        ats_cols = st.columns(2)
        for i, item in enumerate(ats_checks):
            icon = "✅" if item["passed"] else "❌"
            ats_cols[i % 2].write(f"{icon} {item['check']}")

        st.divider()



        # ── Raw Resume Text ───────────────────────────────
        with st.expander("📃 View Extracted Resume Text"):
            st.text(resume_text)