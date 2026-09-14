from backend.repository_intelligence.srs.evidence_mapper import (
    EvidenceMapper,
)


class RequirementBuilder:

    def __init__(self):

        self.evidence_mapper = (
            EvidenceMapper()
        )

    def build(
        self,
        capability_result: dict,
        analysis: dict,
    ) -> list[dict]:

        requirements = []

        capabilities = capability_result.get(
            "capabilities",
            {},
        )

        builders = {
            "web_api": self._build_api,
            "user_interface": self._build_ui,
            "database": self._build_database,
            "authentication": self._build_authentication,
            "machine_learning": self._build_machine_learning,
            "data_processing": self._build_data_processing,
            "testing": self._build_testing,
            "cli": self._build_cli,
            "hardware": self._build_hardware,
            "deployment": self._build_deployment,
            "configuration": self._build_configuration,
        }

        for capability_key, builder in (
            builders.items()
        ):

            capability = capabilities.get(
                capability_key
            )

            if capability:

                requirements.extend(
                    builder(
                        capability_key,
                        capability,
                        analysis,
                    )
                )

        return requirements

    def _build_api(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "API",
                capability_key,
                "API Services",
                "The system shall provide the web or API services implemented by the repository components associated with this capability.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_ui(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "UI",
                capability_key,
                "User Interface",
                "The system shall provide the user-interface functionality implemented by the repository components associated with this capability.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_database(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "DB",
                capability_key,
                "Data Persistence",
                "The system shall provide the data-persistence functionality implemented by the repository components associated with this capability.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_authentication(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "AUTH",
                capability_key,
                "Authentication and Authorization",
                "The system shall provide the authentication or authorization functionality implemented by the repository components associated with this capability.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_machine_learning(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "ML",
                capability_key,
                "Machine Learning",
                "The system shall provide the machine-learning or prediction functionality implemented by the repository components associated with this capability.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_data_processing(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "DATA",
                capability_key,
                "Data Processing",
                "The system shall process or transform the data represented by the repository components associated with this capability.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_testing(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "TEST",
                capability_key,
                "Automated Testing",
                "The project shall maintain the automated testing functionality implemented by the repository components associated with this capability.",
                "Medium",
                capability,
                analysis,
            )
        ]

    def _build_cli(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "CLI",
                capability_key,
                "Command-Line Interface",
                "The system shall provide the command-line functionality implemented by the repository components associated with this capability.",
                "Medium",
                capability,
                analysis,
            )
        ]

    def _build_hardware(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "HW",
                capability_key,
                "Hardware Integration",
                "The system shall interact with the hardware components represented by the repository implementation.",
                "High",
                capability,
                analysis,
            )
        ]

    def _build_deployment(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "DEP",
                capability_key,
                "Deployment Configuration",
                "The project shall support the deployment configuration represented by the repository.",
                "Medium",
                capability,
                analysis,
            )
        ]

    def _build_configuration(
        self,
        capability_key,
        capability,
        analysis,
    ) -> list[dict]:

        return [
            self._requirement(
                "CONFIG",
                capability_key,
                "Configuration Management",
                "The system shall use the configuration components represented by the repository.",
                "Medium",
                capability,
                analysis,
            )
        ]

    def _requirement(
        self,
        prefix,
        capability_key,
        title,
        description,
        priority,
        capability,
        analysis,
    ) -> dict:

        evidence = (
            self.evidence_mapper.build(
                capability_key,
                capability,
                analysis,
            )
        )

        number = (
            self._get_requirement_number(
                prefix,
                capability_key,
            )
        )

        return {
            "id": f"REQ-{prefix}-{number:03d}",
            "capability": capability_key,
            "title": title,
            "description": description,
            "priority": priority,
            "evidence": evidence.get(
                "files",
                [],
            ),
            "functions": evidence.get(
                "functions",
                [],
            ),
            "classes": evidence.get(
                "classes",
                [],
            ),
            "dependency_links": evidence.get(
                "dependency_links",
                [],
            ),
            "evidence_basis": evidence.get(
                "evidence_basis",
                [],
            ),
            "evidence_strength": evidence.get(
                "evidence_strength",
                "Structural",
            ),
        }

    def _get_requirement_number(
        self,
        prefix,
        capability_key,
    ) -> int:

        ordering = {
            "web_api": 1,
            "user_interface": 1,
            "database": 1,
            "authentication": 1,
            "machine_learning": 1,
            "data_processing": 1,
            "testing": 1,
            "cli": 1,
            "hardware": 1,
            "deployment": 1,
            "configuration": 1,
        }

        return ordering.get(
            capability_key,
            1,
        )

    