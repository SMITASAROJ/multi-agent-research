# app.py

import streamlit as st
from pipeline import run_research_pipeline

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Multi Agent Research System",
    page_icon="🔎",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: white;
}

.stTextInput > div > div > input {
    background-color: #262730;
    color: white;
    border-radius: 10px;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #7c4dff;
    color: white;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background-color: #651fff;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.report-box {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 12px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.title("🔎 Multi Agent Research System")

st.markdown("""
### AI Powered Multi-Agent Research Assistant

This system uses:
- 🔍 Search Agent
- 📄 Reader Agent
- ✍ Writer Chain
- 📊 Critic Chain
- 🌐 Tavily Search
- 🧠 LangChain + LCEL
""")

# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.header("⚙ System Info")

    st.success("Groq / OpenAI Powered")

    st.markdown("""
    ### Features
    - Real-time web research
    - URL scraping
    - AI report generation
    - Research critic feedback
    - Multi-agent architecture
    """)

    st.markdown("---")

    st.info("Built using Streamlit + LangChain")

# ---------------- INPUT ---------------- #

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Impact of AI on Healthcare"
)

# ---------------- BUTTON ---------------- #

if st.button("🚀 Generate Research Report"):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
    
    else:

        with st.spinner("Running Multi-Agent Research Pipeline..."):

            try:

                result = run_research_pipeline(topic)

                st.success("Research Completed Successfully!")

                # ---------------- SEARCH RESULTS ---------------- #

                with st.expander("🔍 Search Results", expanded=False):
                    st.write(result["search_results"])

                # ---------------- SCRAPED CONTENT ---------------- #

                with st.expander("📄 Scraped Content", expanded=False):
                    st.write(result["scraped_content"])

                # ---------------- FINAL REPORT ---------------- #

                st.subheader("📝 Final Research Report")

                st.markdown(
                    f"""
                    <div class="report-box">
                    {result["report"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ---------------- FEEDBACK ---------------- #

                st.subheader("📊 Critic Feedback")

                st.markdown(
                    f"""
                    <div class="report-box">
                    {result["feedback"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(f"Error: {str(e)}")

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption("Multi Agent Research System • Streamlit UI")