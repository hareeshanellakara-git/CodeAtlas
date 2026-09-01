import streamlit as st

from api_client import analyze_impact, APIError


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def _build_dot_graph(
    dependency_edges: list[dict],
    file_structures: dict,
) -> str:

    lines = [
        "digraph RepositoryArchitecture {",

        '    graph [rankdir=LR, '
        'bgcolor="transparent", '
        'pad=0.5, '
        'nodesep=0.6, '
        'ranksep=1.0];',

        '    node [shape=box, '
        'style="rounded,filled", '
        'fontname="Arial", '
        'fontsize=10, '
        'margin="0.2,0.12"];',

        '    edge [color="#00ADB5", '
        'penwidth=2.0, '
        'arrowsize=1.2, '
        'fontname="Arial", '
        'fontsize=9];',
    ]

    
    # 1. Collect ALL analyzed source files as graph nodes
    
    nodes = set()

    for file_path in file_structures.keys():

        nodes.add(
            _normalize_path(file_path)
        )

    
    # 2. Normalize dependency edges
    

    normalized_edges = []

    for edge in dependency_edges:

        source = edge.get("source")
        target = edge.get("target")

        if not source or not target:
            continue

        source = _normalize_path(source)
        target = _normalize_path(target)

        nodes.add(source)
        nodes.add(target)

        normalized_edges.append(
            {
                "source": source,
                "target": target,
            }
        )

    
    # 3. Create safe Graphviz node IDs
   
    node_ids = {}

    for index, node in enumerate(
        sorted(nodes)
    ):

        node_id = f"node_{index}"

        node_ids[node] = node_id

        safe_label = (
            node.replace(
                '"',
                '\\"',
            )
        )

        lines.append(
            f'"{node_id}" '
            f'[label="{safe_label}"];'
        )

    
    # 4. Add dependency arrows
    
    for edge in normalized_edges:

        source = edge["source"]
        target = edge["target"]

        source_id = node_ids[source]
        target_id = node_ids[target]

        lines.append(
            f'"{source_id}" '
            f'-> '
            f'"{target_id}" '
            f'[label="depends on"];'
        )

    lines.append("}")

    return "\n".join(lines)


def render_architecture_view():

    stats = st.session_state.repo_stats

    if not stats:
        return

    intelligence = (
        stats.repository_intelligence
    )

    if not intelligence:
        return

    dependency_edges = intelligence.get(
        "dependency_edges",
        [],
    )

    file_structures = intelligence.get(
        "file_structures",
        {},
    )

    repository = intelligence.get(
        "repository_name",
        stats.repository,
    )

    st.markdown(
        """
        <div class="section-header">
            <h2>🏗️ Architecture & Dependency Analysis</h2>
            <p>
                Explore the automatically reconstructed repository
                structure and analyze the potential impact of file changes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    
    # ARCHITECTURE GRAPH
    
    st.markdown(
        "### 🕸️ Repository Architecture Graph"
    )

    if file_structures:

        dot_graph = _build_dot_graph(
            dependency_edges,
            file_structures,
        )

        st.graphviz_chart(
            dot_graph,
            use_container_width=True,
        )

        st.caption(
            "Nodes represent analyzed source files. "
            "Arrows represent dependencies detected from source-code imports."
        )

    else:

        st.info(
            "No source-code structure was detected."
        )

    
    # DEPENDENCY RELATIONSHIPS
    

    st.markdown(
        "### 🔗 Detected Dependencies"
    )

    if dependency_edges:

        for edge in dependency_edges[:20]:

            source = _normalize_path(
                edge.get("source", "")
            )

            target = _normalize_path(
                edge.get("target", "")
            )

            st.markdown(
                f"`{source}` → `{target}`"
            )

    else:

        st.caption(
            "No internal dependencies were detected."
        )

    
    # CHANGE IMPACT ANALYSIS
    

    st.markdown(
        "### 🔍 Change Impact Analysis"
    )

    candidate_files = sorted(
        {
            _normalize_path(path)
            for path in file_structures.keys()
        }
        |
        {
            _normalize_path(edge.get("source", ""))
            for edge in dependency_edges
            if edge.get("source")
        }
        |
        {
            _normalize_path(edge.get("target", ""))
            for edge in dependency_edges
            if edge.get("target")
        }
    )

    if not candidate_files:

        st.info(
            "No files are available for impact analysis."
        )

        return

    selected_file = st.selectbox(
        "Select a file to analyze",
        candidate_files,
    )

    if st.button(
        "🔎 Analyze Change Impact",
        use_container_width=True,
    ):

        try:

            result = analyze_impact(
                repository,
                selected_file,
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Direct Dependents",
                len(
                    result.direct_dependents
                ),
            )

            col2.metric(
                "Indirect Dependents",
                len(
                    result.indirect_dependents
                ),
            )

            col3.metric(
                "Total Affected",
                result.total_affected_files,
            )

            if result.direct_dependents:

                st.markdown(
                    "#### 🔴 Directly Affected"
                )

                for file in (
                    result.direct_dependents
                ):

                    st.write(
                        f"• `{file}`"
                    )

            elif result.total_affected_files == 0:

                st.success(
                    "No dependent files were detected."
                )

            if result.indirect_dependents:

                st.markdown(
                    "#### 🟠 Indirectly Affected"
                )

                for file in (
                    result.indirect_dependents
                ):

                    st.write(
                        f"• `{file}`"
                    )

        except APIError as error:

            st.error(
                f"❌ {error}"
            )