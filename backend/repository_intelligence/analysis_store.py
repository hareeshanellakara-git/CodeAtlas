import json
import re
from pathlib import Path


class AnalysisStore:
    """
    Persists the latest repository intelligence analysis
    as a JSON artifact.
    """

    def __init__(
        self,
        base_path: str = "data/repository_analysis",
    ):

        self.base_path = Path(base_path)

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _safe_repository_name(
        self,
        repository_name: str,
    ) -> str:

        return re.sub(
            r"[^a-zA-Z0-9_.-]",
            "_",
            repository_name,
        )

    def save(
        self,
        repository_name: str,
        analysis: dict,
    ) -> str:

        safe_name = self._safe_repository_name(
            repository_name
        )

        analysis_path = (
            self.base_path
            / f"{safe_name}.json"
        )

        with analysis_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                analysis,
                file,
                indent=2,
            )

        return str(analysis_path)

    def load(
        self,
        repository_name: str,
    ) -> dict:

        safe_name = self._safe_repository_name(
            repository_name
        )

        analysis_path = (
            self.base_path
            / f"{safe_name}.json"
        )

        if not analysis_path.exists():

            raise FileNotFoundError(
                "Repository analysis has not been generated yet."
            )

        with analysis_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)