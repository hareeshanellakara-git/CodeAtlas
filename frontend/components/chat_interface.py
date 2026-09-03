import streamlit as st

from api_client import ask_question, APIError
from session_state import add_chat_message


def render_chat_interface():

    st.markdown(
        """
        <div class="section-header">
            <h2>💬 Chat with Repository</h2>
            <p>
                Ask anything about the repository's architecture, files,
                technologies, functions or implementation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.repo_indexed:

        st.info(
            "Analyze a repository above to start chatting."
        )

        return

    _render_history()

    _render_input()


def _render_history():

    for message in (
        st.session_state.chat_history
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("evidence")
            ):

                _render_evidence(
                    message["evidence"]
                )

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                _render_sources(
                    message["sources"]
                )


def _render_sources(
    sources,
):

    with st.expander(
        f"📄 Sources ({len(sources)})"
    ):

        for source in sources:

            st.markdown(
                f"✓ `{source}`"
            )


def _render_evidence(
    evidence,
):

    with st.expander(
        f"🔍 Retrieved Evidence ({len(evidence)})"
    ):

        st.caption(
            "These are the repository chunks retrieved by "
            "FAISS and provided to the AI as context."
        )

        for item in evidence:

            st.markdown(
                f"### #{item['rank']} — `{item['source']}`"
            )

            score = float(
                item["score"]
            )

            display_score = score * 100
            

            st.markdown(
                f"**Retrieval Relevance: {display_score:.1f}%**"
            )

            st.progress(
                min(max(score, 0.0), 1.0)
            )

            if item.get("preview"):

                st.code(
                    item["preview"],
                    language="text",
                )

            if item != evidence[-1]:

                st.divider()


def _render_input():

    question = st.chat_input(
        "Ask CodeAtlas about this repository..."
    )

    if not question:

        return

    add_chat_message(
        "user",
        question,
    )

    with st.chat_message("user"):

        st.markdown(
            question
        )

    with st.chat_message("assistant"):

        with st.spinner(
            "🔍 Searching the codebase and asking the LLM..."
        ):

            try:

                result = ask_question(
                    question
                )

                st.markdown(
                    """
                    <div class="answer-card">
                        <div class="answer-title">
                            🤖 AI Answer
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    result.answer
                )

                evidence = [
                    {
                        "rank": item.rank,
                        "source": item.source,
                        "score": item.score,
                        "preview": item.preview,
                    }
                    for item in result.evidence
                ]

                if evidence:

                    _render_evidence(
                        evidence
                    )

                if result.sources:

                    _render_sources(
                        result.sources
                    )

                add_chat_message(
                    "assistant",
                    result.answer,
                    result.sources,
                    evidence,
                )

            except APIError as exc:

                error_message = (
                    f"❌ {exc}"
                )

                st.error(
                    error_message
                )

                add_chat_message(
                    "assistant",
                    error_message,
                )