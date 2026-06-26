"""Prompt builder for the legal contract extraction agent."""

import json


class PromptBuilder:
    """Builds deterministic, structured prompts for Gemini-based extraction."""

    def build_prompt(
        self,
        query: str,
        chunks: list[dict],
        schema: dict,
    ) -> str:
        """Build the complete extraction prompt."""

        sections = [
            self._build_instructions(),
            self._build_schema_section(schema),
            self._build_query_section(query),
            self._build_context_section(chunks),
            self._build_output_directive(),
        ]

        return "\n\n".join(sections)

    def _build_instructions(self) -> str:
        """Build the role and strict behavioral rules section."""

        return (
            "You are a precise legal information extraction system.\n"
            "Follow these rules strictly:\n"
            "1. Use ONLY information explicitly present in the provided context.\n"
            "2. Do NOT infer, assume, guess, or use outside knowledge.\n"
            "3. Never hallucinate values. If a field cannot be found, return null.\n"
            "4. If multiple conflicting values exist, do NOT choose one arbitrarily. "
            "Record the conflict in validation_notes.\n"
            "5. For every null, ambiguous, conflicting, or low-confidence field, "
            "add an entry to validation_notes.\n"
            "6. Do not add fields not defined in the schema.\n"
            "7. Return ONLY one valid JSON object matching the schema exactly."
        )

    def _build_schema_section(self, schema: dict) -> str:
        """Embed the target JSON schema."""

        schema_text = json.dumps(
            schema,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )

        return f"Target JSON Schema:\n{schema_text}"

    def _build_query_section(self, query: str) -> str:
        """Embed the user query."""

        return f"User Query:\n{query}"

    def _build_context_section(self, chunks: list[dict]) -> str:
        """Format retrieved chunks for the prompt."""

        formatted_chunks = [
            self._format_chunk(chunk)
            for chunk in chunks
        ]

        return "Context:\n" + "\n\n".join(formatted_chunks)

    def _format_chunk(self, chunk: dict) -> str:
        """Format a single retrieved chunk."""

        chunk_id = chunk.get("chunk_id", "unknown")
        page_number = chunk.get("page_number", "unknown")
        text = chunk.get("text", "")

        return (
            f"[Chunk {chunk_id} | page: {page_number}]\n"
            f"{text}"
        )

    def _build_output_directive(self) -> str:
        """Build the final output instructions."""

        return (
            "Output Format:\n"
            "Respond with ONLY a single valid JSON object.\n"
            "Do not include markdown code fences.\n"
            "Do not include explanations.\n"
            "Do not include comments.\n"
            "Do not include any text before or after the JSON object."
        )