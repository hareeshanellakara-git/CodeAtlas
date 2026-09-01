import ast
import re
from pathlib import Path


class CodeStructureAnalyzer:

    def analyze_repository(
        self,
        repo_path: str,
        excluded_directories: set[str] | None = None,
    ) -> dict:

        repo = Path(repo_path)

        excluded_directories = (
            excluded_directories or set()
        )

        total_classes = 0
        total_functions = 0

        file_structures = {}

        for file_path in repo.rglob("*"):

            if not file_path.is_file():
                continue

            if any(
                directory in file_path.parts
                for directory in excluded_directories
            ):
                continue

            suffix = file_path.suffix.lower()

            if suffix not in {
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
            }:
                continue

            relative_path = str(
                file_path.relative_to(repo)
            )

            try:

                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                if suffix == ".py":
                    result = self._analyze_python(
                        content
                    )
                else:
                    result = self._analyze_generic(
                        content
                    )

                total_classes += len(
                    result["classes"]
                )

                total_functions += len(
                    result["functions"]
                )

                file_structures[relative_path] = result

            except Exception:
                continue

        return {
            "total_classes": total_classes,
            "total_functions": total_functions,
            "files": file_structures,
        }

    def _analyze_python(
        self,
        content: str,
    ) -> dict:

        try:

            tree = ast.parse(content)

        except SyntaxError:

            return {
                "classes": [],
                "functions": [],
            }

        classes = []
        functions = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ClassDef,
            ):
                classes.append(node.name)

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                functions.append(node.name)

        return {
            "classes": sorted(
                set(classes)
            ),
            "functions": sorted(
                set(functions)
            ),
        }

    def _analyze_generic(
        self,
        content: str,
    ) -> dict:

        class_pattern = (
            r"\bclass\s+"
            r"([A-Za-z_]\w*)"
        )

        function_patterns = [
            r"\bfunction\s+([A-Za-z_]\w*)",
            (
                r"\b(?:public|private|protected|"
                r"static|async)?\s*"
                r"(?:[A-Za-z_][\w<>\[\]]*\s+)+"
                r"([A-Za-z_]\w*)\s*\("
            ),
        ]

        classes = re.findall(
            class_pattern,
            content,
        )

        functions = []

        for pattern in function_patterns:

            matches = re.findall(
                pattern,
                content,
            )

            functions.extend(matches)

        return {
            "classes": sorted(
                set(classes)
            ),
            "functions": sorted(
                set(functions)
            ),
        }