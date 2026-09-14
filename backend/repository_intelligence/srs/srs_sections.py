class SRSSections:

    def build_introduction(
        self,
        repository_name: str,
        languages: str,
    ) -> dict:

        return {
            "title": "1. Introduction",
            "content": [
                (
                    "### 1.1 Purpose",
                    f"This document describes the software system implemented in **{repository_name}** based on source-code structure, detected capabilities, dependencies, and implementation evidence analyzed by CodeAtlas.",
                ),
                (
                    "### 1.2 Document Conventions",
                    "This document uses a numbered SRS structure. Functional requirements are assigned unique identifiers and are traceable to repository evidence.",
                ),
                (
                    "### 1.3 Intended Audience and Reading Suggestions",
                    "This document is intended for developers, testers, maintainers, and technical stakeholders who need to understand the observable software capabilities represented by the repository.",
                ),
                (
                    "### 1.4 Product Scope",
                    f"The software analyzed is **{repository_name}**. The repository uses {languages}. The SRS describes capabilities and requirements that can be conservatively reconstructed from repository evidence.",
                ),
                (
                    "### 1.5 References",
                    "The repository source files, project documentation, configuration artifacts, and statically reconstructed analysis models form the primary references for this document.",
                ),
            ],
        }

    def build_overall_description(
        self,
        modules: str,
        capabilities: str,
        environment: str,
        dependencies: str,
        entry_points: str,
        architecture: str,
        execution_flow: str,
    ) -> dict:

        return {
            "title": "2. Overall Description",
            "content": [
                (
                    "### 2.1 Product Perspective",
                    "The product consists of the software modules, capabilities, and implementation relationships reconstructed from the repository.",
                ),
                (
                    "### 2.2 Product Functions",
                    capabilities,
                ),
                (
                    "### 2.3 Operating Environment",
                    environment,
                ),
                (
                    "### 2.4 Design and Implementation Constraints",
                    "The implementation is constrained by the programming languages, frameworks, libraries, configuration artifacts, repository organization, and implementation patterns detected during analysis.",
                ),
                (
                    "### 2.5 Repository Modules",
                    modules,
                ),
                (
                    "### 2.6 Potential Entry Points",
                    entry_points,
                ),
                (
                    "### 2.7 Dependencies",
                    dependencies,
                ),
                (
                    "### 2.8 Reconstructed Architecture",
                    architecture,
                ),
                (
                    "### 2.9 Reconstructed Execution Flow",
                    execution_flow,
                ),
            ],
        }

    def build_interfaces(
        self,
        capabilities: dict,
    ) -> dict:

        content = []

        if "user_interface" in capabilities:
            content.append(
                (
                    "### 3.1 User Interfaces",
                    "User-interface components were detected from repository source files, framework indicators, and structural evidence.",
                )
            )

        if "hardware" in capabilities:
            content.append(
                (
                    "### 3.2 Hardware Interfaces",
                    "Hardware-related implementation components were detected in the repository.",
                )
            )

        if "web_api" in capabilities:
            content.append(
                (
                    "### 3.3 Software Interfaces",
                    "Web or API interface components were detected in the repository.",
                )
            )

        if "deployment" in capabilities:
            content.append(
                (
                    "### 3.4 Deployment Interfaces",
                    "Deployment-related configuration was detected in the repository.",
                )
            )

        if not content:
            return {}

        return {
            "title": "3. External Interface Requirements",
            "content": content,
        }

    def build_system_features(
        self,
        requirements: list[dict],
        capabilities: dict,
    ) -> dict:

        content = []
        feature_number = 1

        for capability_key, capability in (
            capabilities.items()
        ):

            feature_requirements = [
                requirement
                for requirement in requirements
                if requirement.get(
                    "capability"
                ) == capability_key
            ]

            if not feature_requirements:
                continue

            feature_name = capability.get(
                "name",
                capability_key.replace(
                    "_",
                    " ",
                ).title(),
            )

            evidence = capability.get(
                "evidence",
                [],
            )

            description = (
                f"The repository contains implementation associated with **{feature_name}**."
            )

            if evidence:
                description += (
                    " Primary source evidence includes "
                    + ", ".join(
                        f"`{self._normalize_path(item)}`"
                        for item in evidence
                    )
                    + "."
                )

            content.append(
                (
                    f"### 4.{feature_number} {feature_name}",
                    "",
                )
            )

            content.append(
                (
                    f"#### 4.{feature_number}.1 Description and Priority",
                    description,
                )
            )

            content.append(
                (
                    f"#### 4.{feature_number}.2 Implementation Evidence",
                    self._format_implementation_details(
                        feature_requirements
                    ),
                )
            )

            flow = self._format_feature_flow(
                feature_requirements
            )

            if flow:
                content.append(
                    (
                        f"#### 4.{feature_number}.3 Implementation Flow",
                        flow,
                    )
                )
                functional_number = 4
            else:
                functional_number = 3

            content.append(
                (
                    f"#### 4.{feature_number}.{functional_number} Functional Requirements",
                    self._format_requirements(
                        feature_requirements
                    ),
                )
            )

            feature_number += 1

        if not content:
            return {}

        return {
            "title": "4. System Features",
            "content": content,
        }

    def build_nonfunctional_requirements(
        self,
        capabilities: dict,
    ) -> dict:

        content = []

        if "testing" in capabilities:
            content.append(
                (
                    "### 5.1 Reliability and Testability",
                    "Automated testing components were detected in the repository and are therefore represented as part of the project's testability characteristics.",
                )
            )

        if "authentication" in capabilities:
            content.append(
                (
                    "### 5.2 Security",
                    "Authentication or authorization-related implementation components were detected in the repository.",
                )
            )

        if "deployment" in capabilities:
            content.append(
                (
                    "### 5.3 Deployment Characteristics",
                    "Deployment or containerization configuration was detected in the repository.",
                )
            )

        if "configuration" in capabilities:
            content.append(
                (
                    "### 5.4 Configuration",
                    "Application configuration components were detected in the repository.",
                )
            )

        if not content:
            return {}

        return {
            "title": "5. Other Nonfunctional Requirements",
            "content": content,
        }

    def build_other_requirements(
        self,
        capabilities: dict,
    ) -> dict:

        content = []

        if "data_processing" in capabilities:
            content.append(
                (
                    "### 6.1 Data Requirements",
                    "The repository contains implementation components for processing or transforming structured data.",
                )
            )

        if "machine_learning" in capabilities:
            content.append(
                (
                    "### 6.2 Machine Learning Requirements",
                    "The repository contains machine-learning, prediction, training, or inference-related implementation components.",
                )
            )

        if not content:
            return {}

        return {
            "title": "6. Other Requirements",
            "content": content,
        }

    def build_appendices(
        self,
        glossary: str,
        analysis_models: str,
        requirements: list[dict],
        hotspots: list[dict],
    ) -> list[dict]:

        result = []

        if glossary:
            result.append(
                {
                    "title": "Appendix A: Glossary",
                    "content": [
                        glossary
                    ],
                }
            )

        if analysis_models:
            result.append(
                {
                    "title": "Appendix B: Analysis Models",
                    "content": [
                        analysis_models
                    ],
                }
            )

        traceability = (
            self._format_traceability_matrix(
                requirements
            )
        )

        if traceability:
            result.append(
                {
                    "title": "Appendix C: Evidence Traceability Matrix",
                    "content": [
                        traceability
                    ],
                }
            )

        change_snapshot = (
            self._format_change_hotspots(
                hotspots
            )
        )

        if change_snapshot:
            result.append(
                {
                    "title": "Appendix D: Change-Sensitivity Snapshot",
                    "content": [
                        change_snapshot
                    ],
                }
            )

        return result

    def _format_implementation_details(
        self,
        requirements,
    ) -> str:

        lines = []

        for requirement in requirements:

            lines.append(
                f"**{requirement.get('id', 'REQ-UNKNOWN')}**"
            )

            functions = requirement.get(
                "functions",
                [],
            )

            classes = requirement.get(
                "classes",
                [],
            )

            evidence_strength = requirement.get(
                "evidence_strength",
                "Structural",
            )

            basis = requirement.get(
                "evidence_basis",
                [],
            )

            if functions:
                lines.append(
                    "- Functions: "
                    + ", ".join(
                        f"`{item}`"
                        for item in functions
                    )
                )

            if classes:
                lines.append(
                    "- Classes: "
                    + ", ".join(
                        f"`{item}`"
                        for item in classes
                    )
                )

            if not functions and not classes:
                lines.append(
                    "- Implementation units: source-file evidence was detected, but no capability-matched function or class names were extracted."
                )

            lines.append(
                f"- Evidence strength: **{evidence_strength}**"
            )

            if basis:
                lines.append(
                    "- Evidence basis: "
                    + ", ".join(
                        basis
                    )
                )

            lines.append("")

        return "\n".join(
            lines
        ).strip()

    def _format_feature_flow(
        self,
        requirements,
    ) -> str:

        flows = []

        for requirement in requirements:

            links = requirement.get(
                "dependency_links",
                [],
            )

            for link in links:
                flows.append(
                    f"- `{link}`"
                )

        if not flows:
            return ""

        return (
            "The detected implementation relationships associated with this feature are:\n\n"
            + "\n".join(
                list(
                    dict.fromkeys(
                        flows
                    )
                )
            )
        )

    def _format_requirements(
        self,
        requirements,
    ) -> str:

        lines = []

        for requirement in requirements:

            lines.append(
                f"**{requirement.get('id', 'REQ-UNKNOWN')}: {requirement.get('title', 'Requirement')}**"
            )

            lines.append(
                f"- Priority: {requirement.get('priority', 'Medium')}"
            )

            lines.append(
                f"- {requirement.get('description', '')}"
            )

            evidence = requirement.get(
                "evidence",
                [],
            )

            if evidence:
                lines.append(
                    "- Evidence: "
                    + ", ".join(
                        f"`{self._normalize_path(item)}`"
                        for item in evidence
                    )
                )

            lines.append("")

        return "\n".join(
            lines
        ).strip()

    def _format_traceability_matrix(
        self,
        requirements,
    ) -> str:

        lines = []

        for requirement in requirements:

            requirement_id = requirement.get(
                "id",
                "REQ-UNKNOWN",
            )

            capability = requirement.get(
                "title",
                "Capability",
            )

            evidence = requirement.get(
                "evidence",
                [],
            )

            functions = requirement.get(
                "functions",
                [],
            )

            classes = requirement.get(
                "classes",
                [],
            )

            strength = requirement.get(
                "evidence_strength",
                "Structural",
            )

            lines.append(
                f"### {requirement_id}"
            )

            lines.append(
                f"- Capability: **{capability}**"
            )

            if evidence:
                lines.append(
                    "- Source Evidence: "
                    + ", ".join(
                        f"`{self._normalize_path(item)}`"
                        for item in evidence
                    )
                )
            else:
                lines.append(
                    "- Source Evidence: Repository structure"
                )

            units = []

            units.extend(
                f"`{item}`"
                for item in functions
            )

            units.extend(
                f"`{item}`"
                for item in classes
            )

            if units:
                lines.append(
                    "- Implementation Units: "
                    + ", ".join(
                        units
                    )
                )
            else:
                lines.append(
                    "- Implementation Units: Source structure"
                )

            lines.append(
                f"- Evidence Strength: **{strength}**"
            )

            lines.append("")

        return "\n".join(
            lines
        ).strip()

    def _format_change_hotspots(
        self,
        hotspots,
    ) -> str:

        if not hotspots:
            return ""

        lines = [
            "The following files have the highest number of detected incoming dependency relationships and therefore represent repository-level change-sensitivity hotspots.",
            "",
        ]

        for index, hotspot in enumerate(
            hotspots,
            start=1,
        ):

            file_name = self._normalize_path(
                hotspot.get(
                    "file",
                    "",
                )
            )

            dependent_count = hotspot.get(
                "dependent_count",
                0,
            )

            dependents = hotspot.get(
                "dependents",
                [],
            )

            lines.append(
                f"### Hotspot {index}: `{file_name}`"
            )

            lines.append(
                f"- Direct Dependents: **{dependent_count}**"
            )

            if dependents:
                lines.append(
                    "- Affected Components: "
                    + ", ".join(
                        f"`{self._normalize_path(item)}`"
                        for item in dependents
                    )
                )
            else:
                lines.append(
                    "- Affected Components: None"
                )

            lines.append("")

        return "\n".join(
            lines
        ).strip()

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