class SRSFormatter:

    def format_document(
        self,
        sections: list[dict],
    ) -> str:

        parts = []

        for section in sections:

            if not section:

                continue

            title = section.get(
                "title",
                "",
            )

            content = section.get(
                "content",
                [],
            )

            if title:

                parts.append(
                    f"# {title}"
                )

            for item in content:

                if isinstance(
                    item,
                    tuple,
                ):

                    heading = item[0]
                    body = item[1]

                    if heading:

                        parts.append(
                            heading
                        )

                    if body:

                        parts.append(
                            body
                        )

                elif item:

                    parts.append(
                        str(item)
                    )

        return "\n\n".join(
            parts
        )