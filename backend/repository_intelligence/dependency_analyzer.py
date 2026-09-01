import ast
import re
from pathlib import Path


class DependencyAnalyzer:

    def analyze_repository(
        self,
        repo_path: str,
        excluded_directories: set[str] | None = None,
    ) -> dict:

        repo = Path(repo_path)

        excluded_directories = (
            excluded_directories or set()
        )

        repository_files = self._get_repository_files(
            repo,
            excluded_directories,
        )

        dependencies = {}
        total_imports = 0

        for file_path in repository_files:

            relative_path = str(
                file_path.relative_to(repo)
            )

            try:

                imports = self._extract_imports(
                    file_path
                )

                total_imports += len(imports)

                internal_dependencies = (
                    self._resolve_internal_dependencies(
                        imports,
                        file_path,
                        repo,
                        repository_files,
                    )
                )

                dependencies[relative_path] = {
                    "imports": sorted(
                        set(imports)
                    ),
                    "internal_dependencies": sorted(
                        set(internal_dependencies)
                    ),
                }

            except Exception:

                dependencies[relative_path] = {
                    "imports": [],
                    "internal_dependencies": [],
                }

        edges = []

        for source, data in dependencies.items():

            for target in data[
                "internal_dependencies"
            ]:

                edges.append(
                    {
                        "source": source,
                        "target": target,
                    }
                )

        return {
            "total_imports": total_imports,
            "dependencies": dependencies,
            "dependency_edges": edges,
            "internal_dependency_count": len(edges),
        }

    def _get_repository_files(
        self,
        repo: Path,
        excluded_directories: set[str],
    ) -> list[Path]:

        supported_extensions = {
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".java",
            ".cpp",
            ".c",
            ".cs",
            ".go",
            ".rs",
            ".php",
        }

        files = []

        for file_path in repo.rglob("*"):

            if not file_path.is_file():
                continue

            if any(
                directory in file_path.parts
                for directory in excluded_directories
            ):
                continue

            if (
                file_path.suffix.lower()
                not in supported_extensions
            ):
                continue

            files.append(file_path)

        return files

    def _extract_imports(
        self,
        file_path: Path,
    ) -> list[str]:

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        suffix = file_path.suffix.lower()

        if suffix == ".py":
            return self._extract_python_imports(
                content
            )

        return self._extract_generic_imports(
            content
        )

    def _extract_python_imports(
        self,
        content: str,
    ) -> list[str]:

        try:

            tree = ast.parse(content)

        except SyntaxError:

            return []

        imports = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Import,
            ):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                if node.module:
                    imports.append(node.module)

        return imports

    def _extract_generic_imports(
        self,
        content: str,
    ) -> list[str]:

        imports = []

        patterns = [
            (
                r'import\s+.*?from\s+'
                r'[\'"]([^\'"]+)[\'"]'
            ),
            (
                r'import\s+'
                r'[\'"]([^\'"]+)[\'"]'
            ),
            (
                r'require\(\s*[\'"]'
                r'([^\'"]+)[\'"]\s*\)'
            ),
            (
                r'#include\s*[<"]'
                r'([^>"]+)[>"]'
            ),
        ]

        for pattern in patterns:

            matches = re.findall(
                pattern,
                content,
            )

            imports.extend(matches)

        return imports

    def _resolve_internal_dependencies(
        self,
        imports: list[str],
        current_file: Path,
        repo: Path,
        repository_files: list[Path],
    ) -> list[str]:

        internal_dependencies = []

        relative_files = {
            str(
                file_path.relative_to(repo)
            ).replace("\\", "/"): file_path
            for file_path in repository_files
        }

        for imported_module in imports:

            normalized = (
                imported_module
                .replace("\\", "/")
                .lstrip("./")
            )

            possible_paths = self._get_possible_paths(
                normalized
            )

            for possible_path in possible_paths:

                if possible_path in relative_files:

                    internal_dependencies.append(
                        possible_path
                    )
                    break

        return internal_dependencies

    def _get_possible_paths(
        self,
        module: str,
    ) -> list[str]:

        extensions = [
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".java",
            ".cpp",
            ".c",
            ".cs",
            ".go",
            ".rs",
            ".php",
        ]

        paths = []

        dotted_path = module.replace(
            ".",
            "/",
        )

        paths.append(module)
        paths.append(dotted_path)

        for extension in extensions:

            paths.append(
                dotted_path + extension
            )

            paths.append(
                dotted_path
                + "/index"
                + extension
            )

        return paths