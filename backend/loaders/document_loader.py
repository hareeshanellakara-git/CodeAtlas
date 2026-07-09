from pathlib import Path

from langchain_core.documents import Document

from backend.config import settings


class DocumentLoader:
   

    def load_repository(self, repo_path: str) -> list[Document]:

        documents = []

        repo_path = Path(repo_path)

        for file_path in repo_path.rglob("*"):

            if not file_path.is_file():
                continue

            if any(
                excluded in file_path.parts
                for excluded in settings.EXCLUDED_DIRECTORIES
            ):
                continue

            if file_path.suffix.lower() not in settings.ALLOWED_EXTENSIONS:
                continue

            try:

                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).strip()

                if not content:
                    continue

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(file_path.relative_to(repo_path)),
                            "extension": file_path.suffix.lower(),
                        },
                    )
                )

            except Exception:
                continue

        return documents