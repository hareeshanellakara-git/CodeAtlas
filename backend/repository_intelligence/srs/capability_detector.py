class CapabilityDetector:

    def detect(
        self,
        analysis: dict,
    ) -> dict:

        file_structures = analysis.get(
            "file_structures",
            {},
        )

        directory_structure = analysis.get(
            "directory_structure",
            [],
        )

        languages = analysis.get(
            "languages",
            {},
        )

        entry_points = analysis.get(
            "entry_points",
            [],
        )

        filenames = self._get_filenames(
            file_structures
        )

        imports = self._get_imports(
            file_structures
        )

        directories = self._get_directories(
            directory_structure
        )

        capabilities = {}

        self._detect_web_api(
            capabilities,
            filenames,
            imports,
        )

        self._detect_ui(
            capabilities,
            filenames,
            imports,
            directories,
        )

        self._detect_database(
            capabilities,
            filenames,
            imports,
        )

        self._detect_authentication(
            capabilities,
            filenames,
            imports,
        )

        self._detect_machine_learning(
            capabilities,
            filenames,
            imports,
        )

        self._detect_data_processing(
            capabilities,
            filenames,
            imports,
        )

        self._detect_testing(
            capabilities,
            filenames,
            imports,
            directories,
        )

        self._detect_cli(
            capabilities,
            filenames,
            imports,
        )

        self._detect_hardware(
            capabilities,
            filenames,
            imports,
            directories,
        )

        self._detect_deployment(
            capabilities,
            filenames,
            directories,
        )

        self._detect_configuration(
            capabilities,
            filenames,
        )

        self._detect_documentation(
            capabilities,
            filenames,
            directories,
        )

        return {
            "capabilities": capabilities,
            "metadata": {
                "languages_detected": languages,
                "potential_entry_points": entry_points,
            },
        }

    def _detect_web_api(
        self,
        capabilities,
        filenames,
        imports,
    ):

        frameworks = [
            "fastapi",
            "flask",
            "django",
            "express",
            "koa",
            "spring",
            "springframework",
            "gin",
            "fiber",
        ]

        file_patterns = [
            "routes",
            "route",
            "api",
            "server",
            "controller",
            "endpoint",
            "urls.py",
        ]

        if (
            self._contains_any(
                imports,
                frameworks,
            )
            or self._contains_any(
                filenames,
                file_patterns,
            )
        ):

            capabilities["web_api"] = {
                "name": "Web / API Services",
                "evidence": self._collect_matching_files(
                    filenames,
                    file_patterns,
                ),
            }

    def _detect_ui(
        self,
        capabilities,
        filenames,
        imports,
        directories,
    ):

        ui_frameworks = [
            "streamlit",
            "react",
            "react-dom",
            "vue",
            "angular",
            "svelte",
            "tkinter",
            "pyqt",
            "electron",
        ]

        ui_patterns = [
            ".html",
            ".jsx",
            ".tsx",
            ".vue",
            ".svelte",
        ]

        ui_directories = [
            "frontend",
            "ui",
            "views",
            "templates",
            "components",
            "dashboard",
        ]

        if (
            self._contains_any(
                imports,
                ui_frameworks,
            )
            or self._contains_any(
                filenames,
                ui_patterns,
            )
            or self._contains_any(
                directories,
                ui_directories,
            )
        ):

            capabilities["user_interface"] = {
                "name": "User Interface",
                "evidence": self._collect_matching_files(
                    filenames,
                    ui_patterns
                    + ui_directories,
                ),
            }

    def _detect_database(
        self,
        capabilities,
        filenames,
        imports,
    ):

        database_libraries = [
            "sqlalchemy",
            "pymongo",
            "mongoose",
            "prisma",
            "psycopg",
            "mysql",
            "sqlite",
            "mongodb",
            "redis",
            "django.db",
            "hibernate",
            "sequelize",
            "typeorm",
            "peewee",
        ]

        database_patterns = [
            "models.py",
            "database",
            "db.py",
            "schema",
        ]

        if (
            self._contains_any(
                imports,
                database_libraries,
            )
            or self._contains_any(
                filenames,
                database_patterns,
            )
        ):

            capabilities["database"] = {
                "name": "Data Persistence",
                "evidence": self._collect_matching_files(
                    filenames,
                    database_patterns,
                ),
            }

    def _detect_authentication(
        self,
        capabilities,
        filenames,
        imports,
    ):

        auth_libraries = [
            "jwt",
            "oauth",
            "oauth2",
            "bcrypt",
            "passlib",
            "authlib",
            "passport",
        ]

        auth_patterns = [
            "auth",
            "authentication",
            "authorization",
            "login",
            "security",
            "permission",
        ]

        if (
            self._contains_any(
                imports,
                auth_libraries,
            )
            or self._contains_any(
                filenames,
                auth_patterns,
            )
        ):

            capabilities["authentication"] = {
                "name": "Authentication / Authorization",
                "evidence": self._collect_matching_files(
                    filenames,
                    auth_patterns,
                ),
            }

    def _detect_machine_learning(
        self,
        capabilities,
        filenames,
        imports,
    ):

        ml_libraries = [
            "sklearn",
            "scikit-learn",
            "torch",
            "tensorflow",
            "keras",
            "xgboost",
            "lightgbm",
            "catboost",
            "transformers",
            "pytorch",
        ]

        ml_patterns = [
            "model",
            "train",
            "training",
            "predict",
            "prediction",
            "inference",
            "classifier",
            "regressor",
        ]

        if (
            self._contains_any(
                imports,
                ml_libraries,
            )
            or self._contains_any(
                filenames,
                ml_patterns,
            )
        ):

            capabilities["machine_learning"] = {
                "name": "Machine Learning",
                "evidence": self._collect_matching_files(
                    filenames,
                    ml_patterns,
                ),
            }

    def _detect_data_processing(
        self,
        capabilities,
        filenames,
        imports,
    ):

        data_libraries = [
            "pandas",
            "polars",
            "numpy",
        ]

        data_patterns = [
            "dataset",
            "data",
            ".csv",
            ".json",
            "etl",
            "preprocess",
        ]

        if (
            self._contains_any(
                imports,
                data_libraries,
            )
            or self._contains_any(
                filenames,
                data_patterns,
            )
        ):

            capabilities["data_processing"] = {
                "name": "Data Processing",
                "evidence": self._collect_matching_files(
                    filenames,
                    data_patterns,
                ),
            }

    def _detect_testing(
        self,
        capabilities,
        filenames,
        imports,
        directories,
    ):

        testing_libraries = [
            "pytest",
            "unittest",
            "jest",
            "mocha",
            "junit",
            "vitest",
            "nose",
        ]

        testing_patterns = [
            "test_",
            "_test",
            ".test.",
            ".spec.",
            "tests",
        ]

        if (
            self._contains_any(
                imports,
                testing_libraries,
            )
            or self._contains_any(
                filenames,
                testing_patterns,
            )
            or self._contains_any(
                directories,
                [
                    "test",
                    "tests",
                ],
            )
        ):

            capabilities["testing"] = {
                "name": "Automated Testing",
                "evidence": self._collect_matching_files(
                    filenames,
                    testing_patterns,
                ),
            }

    def _detect_cli(
        self,
        capabilities,
        filenames,
        imports,
    ):

        cli_libraries = [
            "argparse",
            "click",
            "typer",
            "fire",
            "commander",
            "yargs",
        ]

        cli_patterns = [
            "cli",
            "command",
            "commands",
        ]

        if (
            self._contains_any(
                imports,
                cli_libraries,
            )
            or self._contains_any(
                filenames,
                cli_patterns,
            )
        ):

            capabilities["cli"] = {
                "name": "Command-Line Interface",
                "evidence": self._collect_matching_files(
                    filenames,
                    cli_patterns,
                ),
            }

    def _detect_hardware(
        self,
        capabilities,
        filenames,
        imports,
        directories,
    ):

        hardware_patterns = [
            "arduino",
            "esp32",
            "raspberry",
            "gpio",
            "serial",
            "sensor",
            "embedded",
            "hardware",
            "microcontroller",
        ]

        if (
            self._contains_any(
                imports,
                hardware_patterns,
            )
            or self._contains_any(
                filenames,
                hardware_patterns,
            )
            or self._contains_any(
                directories,
                hardware_patterns,
            )
        ):

            capabilities["hardware"] = {
                "name": "Hardware Integration",
                "evidence": self._collect_matching_files(
                    filenames,
                    hardware_patterns,
                ),
            }

    def _detect_deployment(
        self,
        capabilities,
        filenames,
        directories,
    ):

        deployment_patterns = [
            "dockerfile",
            "docker-compose",
            "compose.yml",
            "compose.yaml",
            "kubernetes",
            "helm",
        ]

        if (
            self._contains_any(
                filenames,
                deployment_patterns,
            )
            or self._contains_any(
                directories,
                [
                    "k8s",
                    "kubernetes",
                    "helm",
                ],
            )
        ):

            capabilities["deployment"] = {
                "name": "Deployment Configuration",
                "evidence": self._collect_matching_files(
                    filenames,
                    deployment_patterns,
                ),
            }

    def _detect_configuration(
        self,
        capabilities,
        filenames,
    ):

        configuration_patterns = [
            "config",
            "settings",
            ".env",
            "application.yml",
            "application.yaml",
            "application.properties",
        ]

        if self._contains_any(
            filenames,
            configuration_patterns,
        ):

            capabilities["configuration"] = {
                "name": "Configuration Management",
                "evidence": self._collect_matching_files(
                    filenames,
                    configuration_patterns,
                ),
            }

    def _detect_documentation(
        self,
        capabilities,
        filenames,
        directories,
    ):

        documentation_patterns = [
            "readme",
            "documentation",
            "docs",
            ".md",
        ]

        if (
            self._contains_any(
                filenames,
                documentation_patterns,
            )
            or self._contains_any(
                directories,
                [
                    "docs",
                    "documentation",
                ],
            )
        ):

            capabilities["documentation"] = {
                "name": "Project Documentation",
                "evidence": self._collect_matching_files(
                    filenames,
                    documentation_patterns,
                ),
            }

    def _get_filenames(
        self,
        file_structures,
    ) -> list[str]:

        if isinstance(
            file_structures,
            dict,
        ):

            return [
                str(item)
                for item in file_structures.keys()
            ]

        if isinstance(
            file_structures,
            list,
        ):

            return [
                str(item)
                for item in file_structures
            ]

        return []

    def _get_directories(
        self,
        directory_structure,
    ) -> list[str]:

        if isinstance(
            directory_structure,
            dict,
        ):

            return [
                str(item)
                for item in directory_structure.keys()
            ]

        if isinstance(
            directory_structure,
            list,
        ):

            return [
                str(item)
                for item in directory_structure
            ]

        return []

    def _get_imports(
        self,
        file_structures,
    ) -> list[str]:

        imports = []

        if not isinstance(
            file_structures,
            dict,
        ):

            return imports

        for structure in (
            file_structures.values()
        ):

            if not isinstance(
                structure,
                dict,
            ):

                continue

            detected = structure.get(
                "imports",
                [],
            )

            if isinstance(
                detected,
                list,
            ):

                imports.extend(
                    str(item).lower()
                    for item in detected
                )

        return imports

    def _contains_any(
        self,
        values,
        patterns,
    ) -> bool:

        normalized_values = [
            str(value).lower()
            for value in values
        ]

        normalized_patterns = [
            str(pattern).lower()
            for pattern in patterns
        ]

        return any(
            pattern in value
            for value in normalized_values
            for pattern in normalized_patterns
        )

    def _collect_matching_files(
        self,
        filenames,
        patterns,
    ) -> list[str]:

        matches = []

        for filename in filenames:

            normalized = str(
                filename
            ).lower()

            for pattern in patterns:

                if str(pattern).lower() in normalized:

                    matches.append(
                        filename
                    )

                    break

        return list(
            dict.fromkeys(matches)
        )