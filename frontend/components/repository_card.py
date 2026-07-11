

import time

import streamlit as st

from api_client import ingest_repository, APIError
from session_state import set_repo_indexed

PROGRESS_STEPS = [
    "📥 Cloning repository...",
    "📄 Reading files...",
    "✂️ Splitting into chunks...",
    "🧠 Creating embeddings...",
    "🗄️ Building FAISS index...",
]


def render_repository_card():
    st.markdown(
        """
        <div class="section-header">
            <h2>📂 Analyze Repository</h2>
            <p>
                Enter any public GitHub repository URL and let CodeAtlas
                build an intelligent knowledge base for it.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        col_input, col_button = st.columns([4, 1], vertical_alignment="bottom")
        with col_input:
            repo_url = st.text_input(
                "GitHub repository URL",
                placeholder="https://github.com/username/repo",
                label_visibility="collapsed",
                key="repo_url_input",
            )
        with col_button:
            analyze_clicked = st.button("🚀 Analyze Repository", use_container_width=True)

        if analyze_clicked:
            _handle_analyze(repo_url)


def _handle_analyze(repo_url: str):
    if not repo_url.strip():
        st.warning("Please paste a GitHub repository URL first.")
        return

    progress_bar = st.progress(0)

    status = st.empty()
    try:
        for i, step in enumerate(PROGRESS_STEPS):

            status.info(step)

            progress_bar.progress(
                (i + 1) / len(PROGRESS_STEPS)
            )

            time.sleep(0.4)

        stats = ingest_repository(repo_url.strip())
        status.success(f"✅ {stats.message}")

        progress_bar.empty()
        set_repo_indexed(repo_url.strip(), stats)
        st.rerun()

    except APIError as exc:
        progress_bar.empty()

        status.error(f"❌ {exc}")