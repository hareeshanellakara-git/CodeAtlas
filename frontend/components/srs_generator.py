import streamlit as st

from api_client import (
    generate_srs,
    APIError,
)


def render_srs_generator(
    repository: str,
):

    st.markdown(
        """
        <div class="section-header">
            <h2>📄 Software Requirements Specification</h2>
            <p>
                Generate an SRS from the repository structure,
                detected capabilities, dependencies and source evidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not repository:

        st.info(
            "Analyze a repository before generating its SRS."
        )

        return

    if st.button(
        "📄 Generate SRS",
        use_container_width=True,
    ):

        with st.spinner(
            "Building SRS from repository analysis..."
        ):

            try:

                result = generate_srs(
                    repository
                )

                st.session_state.srs_document = (
                    result.document
                )

            except APIError as exc:

                st.error(
                    f"❌ {exc}"
                )

                return

    document = st.session_state.get(
        "srs_document",
        "",
    )

    if not document:

        return

    st.success(
        "SRS generated successfully."
    )

    st.download_button(
        label="⬇️ Download SRS",
        data=document,
        file_name=f"{repository}_SRS.md",
        mime="text/markdown",
        use_container_width=True,
    )

    with st.expander(
        "👁️ Preview SRS",
        expanded=True,
    ):

        st.markdown(
            document
        )