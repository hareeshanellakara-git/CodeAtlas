import streamlit as st


def render_repository_intelligence():

    stats = st.session_state.repo_stats

    if not stats:
        return

    intelligence = (
        stats.repository_intelligence
    )

    if not intelligence:
        return

    summary = intelligence.get(
        "summary",
        {}
    )

    languages = intelligence.get(
        "languages",
        {}
    )

    entry_points = intelligence.get(
        "entry_points",
        []
    )

    largest_files = intelligence.get(
        "largest_files",
        []
    )

    directories = intelligence.get(
        "directory_structure",
        []
    )

    edges = intelligence.get(
        "dependency_edges",
        []
    )

    st.markdown(
        """
        <div class="section-header">
            <h2>🧠 Repository Intelligence</h2>
            <p>
                Automated structural analysis generated
                directly from the repository source code.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    row1 = st.columns(3)

    row1[0].metric(
        "Source Files",
        summary.get(
            "total_source_files",
            0,
        ),
    )

    row1[1].metric(
        "Classes",
        summary.get(
            "total_classes",
            0,
        ),
    )

    row1[2].metric(
        "Functions",
        summary.get(
            "total_functions",
            0,
        ),
    )

    row2 = st.columns(2)

    row2[0].metric(
        "Imports Detected",
        summary.get(
            "total_imports",
            0,
        ),
    )

    row2[1].metric(
        "Internal Dependencies",
        summary.get(
            "internal_dependencies",
            0,
        ),
    )

    if languages:

        st.markdown(
            "### 💻 Languages Detected"
        )

        st.bar_chart(languages)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 🚀 Potential Entry Points"
        )

        if entry_points:

            for entry_point in entry_points:

                st.code(entry_point)

        else:

            st.caption(
                "No common entry point detected."
            )

    with col2:

        st.markdown(
            "### 📁 Repository Structure"
        )

        if directories:

            for directory in directories[:15]:

                st.caption(
                    f"📂 {directory}"
                )

        else:

            st.caption(
                "No directories detected."
            )

    if largest_files:

        st.markdown(
            "### 📦 Largest Files"
        )

        for file_data in largest_files:

            size_kb = (
                file_data["size_bytes"]
                / 1024
            )

            st.markdown(
                f"**{file_data['path']}** "
                f"— {size_kb:.1f} KB"
            )

    if edges:

        st.markdown(
            "### 🔗 Internal Dependencies"
        )

        for edge in edges[:10]:

            st.markdown(
                f"`{edge['source']}` "
                f"→ "
                f"`{edge['target']}`"
            )