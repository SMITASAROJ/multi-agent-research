
import streamlit as st
from pipeline import run_research_pipeline
import html

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
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #7c4dff;
    color: white;
    font-size: 18px;
    border: none;
}
.stButton > button:hover {
    background-color: #651fff;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ---------------- CLEAN RESULT DISPLAY ---------------- #

HIDDEN_KEYS = {
    "extras",
    "signature",
    "usage_metadata",
    "response_metadata",
    "additional_kwargs"
}


def display_content(data):
    """Display readable content without exposing internal metadata."""

    if data is None:
        st.caption("No content available.")
        return

    if isinstance(data, str):
        st.markdown(data)
        return

    if isinstance(data, list):
        for item in data:
            display_content(item)
        return

    if isinstance(data, dict):

        # Extract the actual text from provider response blocks.
        if isinstance(data.get("text"), str):
            st.markdown(data["text"])

            # Show a source link only if a URL is provided.
            url = data.get("url") or data.get("source_url")
            if isinstance(url, str) and url.startswith(("https://", "http://")):
                st.markdown(f"[Open source]({url})")

            return

        # Handle dictionaries containing other readable fields.
        for key, value in data.items():
            if key.lower() in HIDDEN_KEYS:
                continue

            if value is None or value == "":
                continue

            # Avoid displaying opaque binary or token-like metadata.
            if key.lower() in {"id", "token", "token_ids"}:
                continue

            if key.lower() in {"url", "source_url", "link"}:
                if isinstance(value, str) and value.startswith(("https://", "http://")):
                    st.markdown(f"[{html.escape(key.replace('_', ' ').title())}]({value})")
                continue

            if key.lower() in {"title", "name"} and isinstance(value, str):
                st.markdown(f"**{value}**")
                continue

            display_content(value)

        return

    st.write(data)


# ---------------- HEADER ---------------- #

st.title("🔎 Multi-Agent Research System")

st.markdown("""
### AI-Powered Multi-Agent Research Assistant

This system uses:
- 🔍 Search Agent
- 📄 Reader Agent
- ✍️ Writer Chain
- 📊 Critic Chain
- 🌐 Tavily Search
- 🧠 LangChain + LCEL
- ✨ Google Gemini
""")


# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.header("⚙️ System Info")
    st.success("Google Gemini Powered")

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


# ---------------- RESEARCH PIPELINE ---------------- #

if st.button("🚀 Generate Research Report"):

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:
        with st.spinner("Running Multi-Agent Research Pipeline..."):

            try:
                result = run_research_pipeline(topic)

                st.success("Research completed successfully!")

                # SEARCH RESULTS
                with st.expander("🔍 Search Results"):
                    display_content(result.get("search_results"))

                # SCRAPED CONTENT
                with st.expander("📄 Scraped Content"):
                    display_content(result.get("scraped_content"))

                # FINAL REPORT
                st.subheader("📝 Final Research Report")
                display_content(result.get("report"))

                # CRITIC FEEDBACK
                st.subheader("📊 Critic Feedback")
                display_content(result.get("feedback"))

            except Exception as e:
                st.error(f"Research failed: {e}")


# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("Multi-Agent Research System • Streamlit UI")
