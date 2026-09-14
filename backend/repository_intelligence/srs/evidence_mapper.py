class EvidenceMapper:

    def build(
        self,
        capability_key,
        capability,
        analysis,
    ) -> dict:

        evidence_files = [
            self._normalize_path(item)
            for item in capability.get(
                "evidence",
                [],
            )
        ]

        file_structures = analysis.get(
            "file_structures",
            {},
        )

        normalized_structures = {
            self._normalize_path(path): structure
            for path, structure in file_structures.items()
        }

        functions = []
        classes = []

        keywords = self._get_function_keywords(
            capability_key
        )

        for path in evidence_files:

            structure = normalized_structures.get(
                path,
                {},
            )

            if not isinstance(
                structure,
                dict,
            ):
                continue

            detected_functions = structure.get(
                "functions",
                [],
            )

            for function in detected_functions:

                name = str(function)

                if (
                    not keywords
                    or self._matches_keyword(
                        name,
                        keywords,
                    )
                ):
                    functions.append(
                        name
                    )

            detected_classes = structure.get(
                "classes",
                [],
            )

            classes.extend(
                str(item)
                for item in detected_classes
            )

        functions = list(
            dict.fromkeys(functions)
        )

        classes = list(
            dict.fromkeys(classes)
        )

        dependency_links = (
            self._get_dependency_links(
                evidence_files,
                analysis.get(
                    "dependency_edges",
                    [],
                ),
            )
        )

        evidence_basis = [
            "source-file evidence",
        ]

        if functions:
            evidence_basis.append(
                "capability-matched functions"
            )

        if classes:
            evidence_basis.append(
                "detected classes"
            )

        if dependency_links:
            evidence_basis.append(
                "dependency relationships"
            )

        if functions or classes:
            evidence_strength = "Strong"
        else:
            evidence_strength = "Structural"

        return {
            "files": evidence_files,
            "functions": functions,
            "classes": classes,
            "dependency_links": dependency_links,
            "evidence_basis": evidence_basis,
            "evidence_strength": evidence_strength,
        }

    def build_architecture(
        self,
        capabilities,
    ) -> list[dict]:

        layers = []

        layer_map = [
            (
                "Presentation Layer",
                [
                    "user_interface",
                ],
            ),
            (
                "API / Service Layer",
                [
                    "web_api",
                ],
            ),
            (
                "Computation / Intelligence Layer",
                [
                    "machine_learning",
                    "data_processing",
                ],
            ),
            (
                "Persistence Layer",
                [
                    "database",
                ],
            ),
            (
                "Integration Layer",
                [
                    "hardware",
                ],
            ),
            (
                "Cross-Cutting Layer",
                [
                    "authentication",
                    "configuration",
                ],
            ),
            (
                "Quality Layer",
                [
                    "testing",
                ],
            ),
            (
                "Deployment Layer",
                [
                    "deployment",
                ],
            ),
            (
                "Command Layer",
                [
                    "cli",
                ],
            ),
        ]

        for layer_name, capability_keys in layer_map:

            detected = [
                capabilities[key].get(
                    "name",
                    key,
                )
                for key in capability_keys
                if key in capabilities
            ]

            if detected:
                layers.append(
                    {
                        "name": layer_name,
                        "components": detected,
                    }
                )

        return layers

    def build_execution_flow(
        self,
        analysis,
    ) -> list[str]:

        entry_points = [
            self._normalize_path(item)
            for item in analysis.get(
                "entry_points",
                [],
            )
        ]

        edges = self._normalize_edges(
            analysis.get(
                "dependency_edges",
                [],
            )
        )

        flows = []

        for entry_point in entry_points:

            current = entry_point
            chain = [current]
            visited = {current}

            while True:

                next_nodes = [
                    target
                    for source, target in edges
                    if source == current
                    and target not in visited
                ]

                if not next_nodes:
                    break

                current = next_nodes[0]
                chain.append(current)
                visited.add(current)

            if len(chain) > 1:
                flows.append(
                    " → ".join(chain)
                )

        return list(
            dict.fromkeys(flows)
        )

    def build_change_hotspots(
        self,
        analysis,
    ) -> list[dict]:

        edges = self._normalize_edges(
            analysis.get(
                "dependency_edges",
                [],
            )
        )

        reverse_dependencies = {}

        for source, target in edges:

            reverse_dependencies.setdefault(
                target,
                set(),
            )

            reverse_dependencies[target].add(
                source
            )

        hotspots = []

        for target, dependents in (
            reverse_dependencies.items()
        ):

            hotspots.append(
                {
                    "file": target,
                    "dependent_count": len(
                        dependents
                    ),
                    "dependents": sorted(
                        dependents
                    ),
                }
            )

        hotspots.sort(
            key=lambda item: item[
                "dependent_count"
            ],
            reverse=True,
        )

        return hotspots[:5]

    def _get_function_keywords(
        self,
        capability_key,
    ) -> list[str]:

        return {
            "user_interface": [
                "render",
                "display",
                "dashboard",
                "page",
                "ui",
                "view",
            ],
            "web_api": [
                "api",
                "route",
                "endpoint",
                "request",
                "response",
                "server",
            ],
            "database": [
                "db",
                "database",
                "query",
                "insert",
                "update",
                "delete",
                "save",
                "load",
                "fetch",
            ],
            "authentication": [
                "auth",
                "login",
                "logout",
                "token",
                "permission",
                "authorize",
            ],
            "machine_learning": [
                "train",
                "predict",
                "model",
                "inference",
                "classif",
                "regress",
                "forecast",
            ],
            "data_processing": [
                "data",
                "dataset",
                "generate",
                "process",
                "transform",
                "simulate",
                "preprocess",
            ],
            "testing": [
                "test",
                "assert",
                "verify",
                "check",
            ],
            "cli": [
                "cli",
                "command",
                "run",
                "execute",
            ],
            "hardware": [
                "sensor",
                "serial",
                "gpio",
                "read",
                "write",
                "connect",
            ],
            "deployment": [
                "deploy",
                "build",
                "start",
                "run",
            ],
            "configuration": [
                "config",
                "setting",
                "load",
                "initialize",
            ],
        }.get(
            capability_key,
            [],
        )

    def _matches_keyword(
        self,
        function_name,
        keywords,
    ) -> bool:

        normalized = (
            str(function_name)
            .lower()
        )

        return any(
            keyword in normalized
            for keyword in keywords
        )

    def _get_dependency_links(
        self,
        evidence_files,
        dependency_edges,
    ) -> list[str]:

        evidence_set = set(
            evidence_files
        )

        links = []

        for source, target in (
            self._normalize_edges(
                dependency_edges
            )
        ):

            if (
                source in evidence_set
                or target in evidence_set
            ):

                links.append(
                    f"{source} → {target}"
                )

        return list(
            dict.fromkeys(
                links
            )
        )

    def _normalize_edges(
        self,
        dependency_edges,
    ) -> list[tuple[str, str]]:

        normalized = []

        for edge in dependency_edges:

            source = None
            target = None

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

            elif isinstance(
                edge,
                (list, tuple),
            ) and len(edge) >= 2:

                source = edge[0]
                target = edge[1]

            elif isinstance(
                edge,
                str,
            ) and "→" in edge:

                source, target = (
                    edge.split(
                        "→",
                        1,
                    )
                )

            if source is None or target is None:
                continue

            normalized.append(
                (
                    self._normalize_path(
                        source
                    ),
                    self._normalize_path(
                        target
                    ),
                )
            )

        return normalized

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