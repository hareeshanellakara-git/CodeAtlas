from collections import Counter
from pathlib import Path


LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".html": "HTML",
    ".css": "CSS",
}


class LanguageDetector:

    def detect_languages(self, repo_path: str) -> dict:
        """
        Detect programming languages based on file extensions.
        """

        repo = Path(repo_path)

        language_counts = Counter()
        total_files = 0

        for file_path in repo.rglob("*"):

            if not file_path.is_file():
                continue

            language = LANGUAGE_MAP.get(
                file_path.suffix.lower()
            )

            if language:
                language_counts[language] += 1
                total_files += 1

        return {
            "total_source_files": total_files,
            "languages": dict(
                sorted(
                    language_counts.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ),
        }