
import streamlit as st

def render_stats_dashboard():

    stats = st.session_state.repo_stats

    if not stats:
        return

    st.markdown("### 📊 Repository Statistics")

    row1 = st.columns(3)

    row1[0].metric(
        "Repository",
        stats.repository,
    )

    row1[1].metric(
        "Files Indexed",
        stats.documents_processed,
    )

    row1[2].metric(
        "Chunks",
        stats.chunks_created,
    )

    row2 = st.columns(3)

    row2[0].metric(
        "LLM",
        stats.llm,
    )

    row2[1].metric(
        "Embeddings",
        stats.embedding_model,
    )

    row2[2].metric(
        "Vector DB",
        stats.vector_database,
    )


    