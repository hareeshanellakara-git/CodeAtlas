from pathlib import Path

from backend.config import settings

from backend.repository_intelligence.language_detector import (
    LanguageDetector,
)

from backend.repository_intelligence.code_structure_analyzer import (
    CodeStructureAnalyzer,
)

from backend.repository_intelligence.dependency_analyzer import (
    DependencyAnalyzer,
)


class RepositoryAnalyzer:

    def __init__(self):

        self.language_detector = (
            LanguageDetector()
        )

        self.code_structure_analyzer = (
            CodeStructureAnalyzer()
        )

        self.dependency_analyzer = (
            DependencyAnalyzer()
        )

    def analyze_repository(
        self,
        repo_path: str,
    ) -> dict:

        repo = Path(repo_path)

        if not repo.exists():
            raise FileNotFoundError(
                "Repository path does not exist."
            )

        language_data = (
            self.language_detector
            .detect_languages(
                repo_path
            )
        )

        structure_data = (
            self.code_structure_analyzer
            .analyze_repository(
                repo_path,
                settings.EXCLUDED_DIRECTORIES,
            )
        )

        dependency_data = (
            self.dependency_analyzer
            .analyze_repository(
                repo_path,
                settings.EXCLUDED_DIRECTORIES,
            )
        )

        entry_points = (
            self._detect_entry_points(
                repo
            )
        )

        largest_files = (
            self._get_largest_files(
                repo
            )
        )

        directory_structure = (
            self._get_directory_structure(
                repo
            )
        )

        return {
            "repository_name": repo.name,

            "summary": {
                "total_source_files": (
                    language_data[
                        "total_source_files"
                    ]
                ),

                "total_classes": (
                    structure_data[
                        "total_classes"
                    ]
                ),

                "total_functions": (
                    structure_data[
                        "total_functions"
                    ]
                ),

                "total_imports": (
                    dependency_data[
                        "total_imports"
                    ]
                ),

                "internal_dependencies": (
                    dependency_data[
                        "internal_dependency_count"
                    ]
                ),
            },

            "languages": (
                language_data["languages"]
            ),

            "entry_points": entry_points,

            "largest_files": largest_files,

            "directory_structure": (
                directory_structure
            ),

            "dependency_edges": (
                dependency_data[
                    "dependency_edges"
                ]
            ),

            "file_structures": (
                structure_data["files"]
            ),

            "dependencies": (
                dependency_data[
                    "dependencies"
                ]
            ),
        }

    def _detect_entry_points(
        self,
        repo: Path,
    ) -> list[str]:

        common_entry_points = {
            "main.py",
            "app.py",
            "server.py",
            "manage.py",
            "index.js",
            "index.ts",
            "server.js",
            "server.ts",
            "main.js",
            "main.ts",
            "Program.java",
        }

        entry_points = []

        for file_path in repo.rglob("*"):

            if not file_path.is_file():
                continue

            if any(
                directory in file_path.parts
                for directory in settings.EXCLUDED_DIRECTORIES
            ):
                continue

            if file_path.name in common_entry_points:

                entry_points.append(
                    str(
                        file_path.relative_to(repo)
                    )
                )

        return sorted(entry_points)

    def _get_largest_files(
        self,
        repo: Path,
        limit: int = 5,
    ) -> list[dict]:

        files = []

        for file_path in repo.rglob("*"):

            if not file_path.is_file():
                continue

            if any(
                directory in file_path.parts
                for directory in settings.EXCLUDED_DIRECTORIES
            ):
                continue

            try:

                files.append(
                    {
                        "path": str(
                            file_path.relative_to(repo)
                        ),
                        "size_bytes": (
                            file_path.stat().st_size
                        ),
                    }
                )

            except OSError:
                continue

        files.sort(
            key=lambda item: (
                item["size_bytes"]
            ),
            reverse=True,
        )

        return files[:limit]

    def _get_directory_structure(
        self,
        repo: Path,
        max_depth: int = 2,
    ) -> list[str]:

        directories = set()

        for path in repo.rglob("*"):

            if not path.is_dir():
                continue

            if any(
                directory in path.parts
                for directory in settings.EXCLUDED_DIRECTORIES
            ):
                continue

            try:

                relative = path.relative_to(repo)

                if len(relative.parts) <= max_depth:
                    directories.add(
                        str(relative)
                    )

            except ValueError:
                continue

        return sorted(directories)