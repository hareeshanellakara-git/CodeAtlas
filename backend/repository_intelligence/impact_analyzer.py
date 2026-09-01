from collections import defaultdict, deque


class ImpactAnalyzer:
    """
    Performs dependency-based change impact analysis.

    An edge:

        source -> target

    means that source depends on target.

    Therefore, when target changes, source may be affected.
    """

    def build_reverse_graph(
        self,
        dependency_edges: list[dict],
    ) -> dict[str, set[str]]:

        reverse_graph = defaultdict(set)

        for edge in dependency_edges:

            source = edge.get("source")
            target = edge.get("target")

            if not source or not target:
                continue

            source = source.replace("\\", "/")
            target = target.replace("\\", "/")

            reverse_graph[target].add(source)

        return dict(reverse_graph)

    def analyze(
        self,
        dependency_edges: list[dict],
        changed_file: str,
    ) -> dict:

        changed_file = changed_file.replace(
            "\\",
            "/",
        )

        reverse_graph = self.build_reverse_graph(
            dependency_edges
        )

        direct_dependents = sorted(
            reverse_graph.get(
                changed_file,
                set(),
            )
        )

        affected_files = set()

        queue = deque(
            direct_dependents
        )

        while queue:

            current = queue.popleft()

            if current in affected_files:
                continue

            affected_files.add(current)

            for dependent in reverse_graph.get(
                current,
                set(),
            ):

                if dependent not in affected_files:
                    queue.append(dependent)

        indirect_dependents = sorted(
            affected_files.difference(
                direct_dependents
            )
        )

        return {
            "changed_file": changed_file,
            "direct_dependents": direct_dependents,
            "indirect_dependents": indirect_dependents,
            "total_affected_files": len(
                affected_files
            ),
            "all_affected_files": sorted(
                affected_files
            ),
        }