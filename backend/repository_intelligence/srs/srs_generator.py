from datetime import datetime

from backend.repository_intelligence.srs.capability_detector import (
    CapabilityDetector,
)
from backend.repository_intelligence.srs.requirement_builder import (
    RequirementBuilder,
)
from backend.repository_intelligence.srs.srs_sections import (
    SRSSections,
)
from backend.repository_intelligence.srs.srs_formatter import (
    SRSFormatter,
)
from backend.repository_intelligence.srs.evidence_mapper import (
    EvidenceMapper,
)


class SRSGenerator:

    def __init__(self):

        self.capability_detector = (
            CapabilityDetector()
        )

        self.requirement_builder = (
            RequirementBuilder()
        )

        self.sections_builder = (
            SRSSections()
        )

        self.formatter = (
            SRSFormatter()
        )

        self.evidence_mapper = (
            EvidenceMapper()
        )

    def generate(
        self,
        analysis: dict,
    ) -> str:

        repository_name = str(
            analysis.get(
                "repository_name",
                "Repository",
            )
        )

        languages = self._format_languages(
            analysis.get(
                "languages",
                {},
            )
        )

        modules = self._format_modules(
            analysis.get(
                "directory_structure",
                [],
            )
        )

        entry_points = self._format_entries(
            analysis.get(
                "entry_points",
                [],
            )
        )

        dependencies = (
            self._format_dependencies(
                analysis.get(
                    "dependency_edges",
                    [],
                )
            )
        )

        capability_result = (
            self.capability_detector.detect(
                analysis
            )
        )

        capabilities = capability_result.get(
            "capabilities",
            {},
        )

        requirements = (
            self.requirement_builder.build(
                capability_result,
                analysis,
            )
        )

        architecture = (
            self._format_architecture(
                self.evidence_mapper.build_architecture(
                    capabilities
                )
            )
        )

        execution_flow = (
            self._format_execution_flow(
                self.evidence_mapper.build_execution_flow(
                    analysis
                )
            )
        )

        environment = (
            self._build_environment(
                languages,
                capabilities,
            )
        )

        capability_text = (
            self._format_capabilities(
                capabilities
            )
        )

        feature_section = (
            self.sections_builder.build_system_features(
                requirements,
                capabilities,
            )
        )

        nonfunctional_section = (
            self.sections_builder.build_nonfunctional_requirements(
                capabilities
            )
        )

        other_section = (
            self.sections_builder.build_other_requirements(
                capabilities
            )
        )

        source_file_count = (
            self._get_source_file_count(
                analysis
            )
        )

        functions = (
            self._count_structures(
                analysis,
                "functions",
            )
        )

        classes = (
            self._count_structures(
                analysis,
                "classes",
            )
        )

        glossary = (
            self._build_glossary(
                capabilities
            )
        )

        analysis_models = (
            self._build_analysis_models(
                analysis,
                source_file_count,
                functions,
                classes,
            )
        )

        hotspots = (
            self.evidence_mapper.build_change_hotspots(
                analysis
            )
        )

        sections = []

        sections.append(
            self.sections_builder.build_introduction(
                repository_name,
                languages,
            )
        )

        sections.append(
            self.sections_builder.build_overall_description(
                modules,
                capability_text,
                environment,
                dependencies,
                entry_points,
                architecture,
                execution_flow,
            )
        )

        interface_section = (
            self.sections_builder.build_interfaces(
                capabilities
            )
        )

        if interface_section:
            sections.append(
                interface_section
            )

        if feature_section:
            sections.append(
                feature_section
            )

        if nonfunctional_section:
            sections.append(
                nonfunctional_section
            )

        if other_section:
            sections.append(
                other_section
            )

        sections.extend(
            self.sections_builder.build_appendices(
                glossary,
                analysis_models,
                requirements,
                hotspots,
            )
        )

        document = (
            self.formatter.format_document(
                sections
            )
        )

        generated_at = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        header = (
            "# SOFTWARE REQUIREMENTS SPECIFICATION\n\n"
            f"**Project:** {repository_name}\n\n"
            f"**Generated by CodeAtlas:** {generated_at}\n\n"
            "**Generation Method:** Evidence-based static reconstruction\n\n"
            "---"
        )

        return (
            header
            + "\n\n"
            + document
        )

    def _format_languages(
        self,
        languages,
    ) -> str:

        if not languages:
            return "No programming languages were detected"

        total = sum(
            languages.values()
        )

        items = [
            f"{name} ({count})"
            for name, count in (
                languages.items()
            )
        ]

        return (
            ", ".join(items)
            + f", with {total} source files analyzed"
        )

    def _format_modules(
        self,
        directories,
    ) -> str:

        if isinstance(
            directories,
            dict,
        ):

            directories = (
                directories.keys()
            )

        normalized = [
            self._normalize_path(
                item
            )
            for item in directories
        ]

        normalized = sorted(
            set(normalized)
        )

        if not normalized:
            return "No repository modules were structurally identified."

        return "\n".join(
            f"- `{item}`"
            for item in normalized
        )

    def _format_entries(
        self,
        entry_points,
    ) -> str:

        normalized = [
            self._normalize_path(
                item
            )
            for item in entry_points
        ]

        if not normalized:
            return "No conventional entry points were detected."

        return "\n".join(
            f"- `{item}`"
            for item in normalized
        )

    def _format_dependencies(
        self,
        dependency_edges,
    ) -> str:

        if not dependency_edges:
            return "No internal dependency relationships were detected."

        lines = []

        for edge in dependency_edges:

            if isinstance(
                edge,
                dict,
            ):

                source = (
                    edge.get("source")
                    or edge.get("from")
                )

                target = (
                    edge.get("target")
                    or edge.get("to")
                )

                if source and target:

                    lines.append(
                        f"- `{self._normalize_path(source)}` → `{self._normalize_path(target)}`"
                    )

            elif isinstance(
                edge,
                (list, tuple),
            ) and len(edge) >= 2:

                lines.append(
                    f"- `{self._normalize_path(edge[0])}` → `{self._normalize_path(edge[1])}`"
                )

            elif isinstance(
                edge,
                str,
            ):

                lines.append(
                    f"- `{edge.replace(chr(92), '/')}`"
                )

        return (
            "\n".join(
                dict.fromkeys(
                    lines
                )
            )
            or "No internal dependency relationships were detected."
        )

    def _format_capabilities(
        self,
        capabilities,
    ) -> str:

        if not capabilities:
            return "No implementation capabilities were confidently detected."

        lines = []

        for capability in (
            capabilities.values()
        ):

            name = capability.get(
                "name",
                "Capability",
            )

            evidence = capability.get(
                "evidence",
                [],
            )

            lines.append(
                f"- **{name}**"
            )

            if evidence:

                lines.append(
                    "  - Evidence: "
                    + ", ".join(
                        f"`{self._normalize_path(item)}`"
                        for item in evidence
                    )
                )

        return "\n".join(
            lines
        )

    def _format_architecture(
        self,
        layers,
    ) -> str:

        if not layers:
            return "No layered architecture could be reconstructed from the detected capabilities."

        lines = []

        for layer in layers:

            lines.append(
                f"- **{layer['name']}**: "
                + ", ".join(
                    layer["components"]
                )
            )

        return "\n".join(
            lines
        )

    def _format_execution_flow(
        self,
        flows,
    ) -> str:

        if not flows:

            return (
                "No dependency-based execution flow could be reconstructed. "
                "Potential execution entry points are documented separately."
            )

        return (
            "The following dependency-based execution paths were reconstructed "
            "from detected entry points and internal relationships:\n\n"
            + "\n".join(
                f"- `{flow}`"
                for flow in flows
            )
        )

    def _build_environment(
        self,
        languages,
        capabilities,
    ) -> str:

        lines = []

        lines.append(
            f"- Programming environment: {languages}."
        )

        if "user_interface" in capabilities:
            lines.append(
                "- User-interface components were detected."
            )

        if "web_api" in capabilities:
            lines.append(
                "- Web or API service components were detected."
            )

        if "machine_learning" in capabilities:
            lines.append(
                "- Machine-learning components were detected."
            )

        if "hardware" in capabilities:
            lines.append(
                "- Hardware integration components were detected."
            )

        if "database" in capabilities:
            lines.append(
                "- Data-persistence components were detected."
            )

        return "\n".join(
            lines
        )

    def _get_source_file_count(
        self,
        analysis,
    ) -> int:

        summary = analysis.get(
            "summary",
            {},
        )

        return int(
            summary.get(
                "total_source_files",
                len(
                    analysis.get(
                        "file_structures",
                        {},
                    )
                ),
            )
        )

    def _count_structures(
        self,
        analysis,
        structure_type,
    ) -> int:

        total = 0

        for structure in (
            analysis.get(
                "file_structures",
                {},
            ).values()
        ):

            if not isinstance(
                structure,
                dict,
            ):
                continue

            total += len(
                structure.get(
                    structure_type,
                    [],
                )
            )

        return total

    def _build_glossary(
        self,
        capabilities,
    ) -> str:

        terms = {
            "SRS": "Software Requirements Specification",
            "REQ": "Requirement identifier",
            "UI": "User Interface",
            "API": "Application Programming Interface",
            "ML": "Machine Learning",
            "Traceability": "A mapping between generated requirements and repository evidence",
        }

        detected_terms = []

        if "user_interface" in capabilities:
            detected_terms.append(
                "UI"
            )

        if "web_api" in capabilities:
            detected_terms.append(
                "API"
            )

        if "machine_learning" in capabilities:
            detected_terms.append(
                "ML"
            )

        detected_terms.extend(
            [
                "SRS",
                "REQ",
                "Traceability",
            ]
        )

        lines = []

        for term in dict.fromkeys(
            detected_terms
        ):

            lines.append(
                f"- **{term}** — {terms[term]}"
            )

        return "\n".join(
            lines
        )

    def _build_analysis_models(
        self,
        analysis,
        source_file_count,
        functions,
        classes,
    ) -> str:

        summary = analysis.get(
            "summary",
            {},
        )

        internal_dependencies = int(
            summary.get(
                "internal_dependencies",
                len(
                    analysis.get(
                        "dependency_edges",
                        [],
                    )
                ),
            )
        )

        lines = [
            f"- Source files analyzed: **{source_file_count}**",
            f"- Detected functions: **{functions}**",
            f"- Detected classes: **{classes}**",
            f"- Internal dependency relationships: **{internal_dependencies}**",
        ]

        edges = analysis.get(
            "dependency_edges",
            [],
        )

        if edges:

            lines.append(
                ""
            )

            lines.append(
                "### Repository Dependency Model"
            )

            for edge in edges:

                if isinstance(
                    edge,
                    dict,
                ):

                    source = (
                        edge.get("source")
                        or edge.get("from")
                    )

                    target = (
                        edge.get("target")
                        or edge.get("to")
                    )

                    if source and target:

                        lines.append(
                            f"- `{self._normalize_path(source)}` → `{self._normalize_path(target)}`"
                        )

                elif isinstance(
                    edge,
                    (list, tuple),
                ) and len(edge) >= 2:

                    lines.append(
                        f"- `{self._normalize_path(edge[0])}` → `{self._normalize_path(edge[1])}`"
                    )

        return "\n".join(
            lines
        )

    def _normalize_path(
        self,
        value,
    ) -> str:

        return str(
            value
        ).replace(
            "\\",
            "/",
        )