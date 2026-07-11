

import streamlit as st

from config import (
    APP_TAGLINE,
    LOGO_PATH,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_LLM,
    DEFAULT_VECTOR_DB,
    POWERED_BY,
)


def render_sidebar():
    with st.sidebar:
        _render_brand()
        st.markdown("---")
        _render_repository_status()
        st.markdown("---")
        _render_model_info()
        st.markdown("---")
        _render_credits()


def _render_brand():
    try:
        st.markdown(
            '<div class="sidebar-logo">',
            unsafe_allow_html=True,
        )       
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image(
                LOGO_PATH,
                width=180,
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )
    except Exception:
        st.markdown("### 🤖 CodeAtlas")
    st.markdown(
        f"<div class='sidebar-tagline'>{APP_TAGLINE}</div>",
        unsafe_allow_html=True,
    )


def _render_repository_status():

    st.markdown("### 🟢 Status")

    if st.session_state.repo_indexed:

        st.success("Repository Indexed")

        st.markdown("### 📂 Current Repository")

        repo_name = (
            st.session_state.repo_stats.repository
            or st.session_state.repo_url
        )

        st.code(repo_name)

    else:

        st.warning("No Repository Indexed")

        st.caption("Analyze a GitHub repository to begin.")






def _render_model_info():

    st.markdown("### 🧠 AI Stack")

    stats = st.session_state.repo_stats

    embedding = (
        stats.embedding_model
        if stats and stats.embedding_model
        else DEFAULT_EMBEDDING_MODEL
    )

    llm = (
        stats.llm
        if stats and stats.llm
        else DEFAULT_LLM
    )

    vector_db = (
        stats.vector_database
        if stats and stats.vector_database
        else DEFAULT_VECTOR_DB
    )

    st.markdown(f"**LLM**")
    st.caption(llm)

    st.markdown(f"**Embeddings**")
    st.caption(embedding)

    st.markdown(f"**Vector DB**")
    st.caption(vector_db)


def _render_credits():
    st.markdown("#### 🔗 Powered by")
    st.caption(" • ".join(POWERED_BY))