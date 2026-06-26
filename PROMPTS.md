# PROMPTS.md

# 1. Architecture Prompt

**Date:** 2026-06-26

## Prompt

You are a senior AI engineer.

I am building an Agentic RAG pipeline for a legal contract extraction challenge.

Requirements:

- Python 3.12
- FastAPI
- LangChain
- LangGraph (if useful)
- FAISS
- Sentence Transformers
- Pydantic
- pdfplumber or Unstructured
- Strict JSON schema extraction
- Validation agent that detects contradictions and populates validation_notes

Important constraints:

- The application must also include a CLI in addition to the FastAPI API.
- The code should be modular, production-quality, and easy to explain in an interview.
- Do not generate any code yet.

Instead provide:

1. Overall architecture
2. Folder structure
3. Responsibilities of every module
4. End-to-end data flow
5. CLI design
6. FastAPI endpoints
7. Validation strategy
8. Error handling strategy
9. Logging strategy
10. Development roadmap in implementation order

Do not write any implementation code.

---

## AI Response Summary

- Proposed a modular Agentic RAG architecture.
- Suggested LangGraph orchestration.
- Introduced FastAPI + CLI.
- Added FAISS, validation agent, and service layer.

---

# 2. Refinement Loop

## Refinement 1

### Prompt

Review the proposed architecture as if you are an Staff AI Engineer conducting a production design review.

Do not rewrite everything.

Instead identify:

1. Unnecessary complexity for a 24-hour internship assignment.
2. Places where the architecture is overengineered.
3. Missing design decisions.
4. Risks in the chunking strategy.
5. Risks in retrieval.
6. Risks in validation.
7. Improvements specifically for legal contracts with tables, cross references and schedule overrides.
8. Explain how the validator should detect contradictory values like:
   - different signatory titles
   - overridden clauses
   - headline fee vs effective fee
   - conflicting notice periods

Finally provide a revised architecture that is simpler, interview-friendly, and more robust.

### AI Response Summary

The AI reviewed its own architecture and identified:

- LangGraph was unnecessary for a linear pipeline.
- Background jobs and batch APIs added unnecessary complexity.
- Retrieval needed better coverage for contradiction detection.
- Validation required deterministic checks before LLM reasoning.
- Table extraction and cross-reference resolution were missing.

### What Was Wrong

After reviewing the proposed architecture, I identified a few areas that were not well suited for a 24-hour internship challenge:

- The architecture introduced unnecessary complexity by using LangGraph, background jobs, and batch APIs for a simple linear extraction workflow.
- The retrieval strategy focused on semantic search but did not sufficiently address retrieval recall for contradiction detection.
- The validation strategy relied heavily on an LLM and lacked deterministic checks for conflicting values.
- The design did not clearly explain how tables, schedule overrides, and cross-references would be preserved during chunking and retrieval.
- Some infrastructure components (index registry, persistent indexing, detailed exception hierarchy) increased implementation effort without significantly improving the assignment outcome.

These observations led me to simplify the architecture and focus more on document understanding, retrieval quality, and deterministic validation.

### Final Decision

I simplified the architecture by:

- Removing LangGraph.
- Removing background jobs and index registry.
- Using a single pipeline orchestrator.
- Adding table-aware chunking.
- Adding deterministic validation before LLM-based contradiction -detection.
- Adding cross-reference expansion and document-role metadata for legal overrides..

---

## Refinement 2

### Prompt

Generate only a production-ready pyproject.toml file for this project.

### AI Response Summary

The AI generated a complete `pyproject.toml` with project metadata, dependencies, build configuration, and development tools.

### What Was Wrong

- The generated build configuration assumed a `legal-rag` package, while the project uses a `src/` layout.
- Gemini dependencies were missing.
- The author information was left as a placeholder.
- The development dependencies did not include Black.

### Final Decision

- Updated the author information.
- Added Gemini dependencies.
- Removed the incorrect package configuration.
- Added Black to the development dependencies.
- Kept the configuration aligned with the current project structure.

## Refinement 3

### Prompt

Generate only `src/core/config.py`.

### AI Response Summary

The AI generated a strongly typed configuration module using `pydantic-settings`, including environment variable loading, validation, and a singleton `Settings` instance.

### What Was Wrong

- The default embedding model was heavier than required for this assignment.
- I preferred using a lightweight embedding model that is commonly used for RAG pipelines and faster to run locally.

### Final Decision

- Replaced the default embedding model with `BAAI/bge-small-en-v1.5`.
- Kept the remaining implementation unchanged because it already followed good engineering practices.

## Refinement 4

### Prompt

Generate only `src/core/logging.py`.

### AI Response Summary

The AI generated a reusable logging module with configurable log levels, a shared logger instance, and protection against duplicate handlers.

### What Was Wrong

No major issues were found during review. The generated implementation already matched the project requirements and followed good engineering practices.

### Final Decision

Accepted the implementation without functional changes because it was simple, reusable, and appropriate for the project.

## Refinement 5

### Prompt

Generate only `src/core/exceptions.py`.

### AI Response Summary

The AI generated a clean exception hierarchy with a shared base exception and dedicated exception types for each pipeline stage.

### What Was Wrong

No significant issues were identified. The implementation was simple, modular, and matched the intended architecture.

### Final Decision

Accepted the implementation without modifications because it clearly separates different failure categories while keeping the code easy to understand and maintain.

## Refinement 6

### Prompt

Analyze the provided JSON schema. Do not generate code. Identify the hierarchy, required fields, optional fields, nested objects, validation constraints, implementation challenges, and the best order for implementing the corresponding Pydantic models.

### AI Response Summary

The AI performed a detailed structural analysis of the schema, identified reusable models, nullable fields, validation constraints, and recommended a bottom-up implementation strategy.

### What Was Wrong

No major issues were found. However, the analysis highlighted implementation decisions that are not explicitly defined by the schema, such as handling reimbursement caps, percentage validation, and strict handling of additional properties.

### Final Decision

Accepted the analysis and decided to implement the Pydantic models in a bottom-up order before adding any cross-field validation logic.

## Refinement 7

### Prompt

Generate the Pydantic models for the analyzed JSON schema.

### AI Response Summary

The AI generated reusable Pydantic models using a bottom-up approach with enums, nested models, and strict schema enforcement.

### What Was Wrong

- Nullable fields that are required by the JSON schema were incorrectly implemented as optional (`default=None`) instead of required nullable fields.
- The reimbursement currency was typed as a generic string instead of reusing the existing Currency enum.
- A field description assumed implementation details that were not guaranteed by the schema.

### Final Decision

Updated the models to distinguish required-nullable fields from optional fields, reused existing enums where appropriate, and aligned field descriptions more closely with the schema.

## Refinement 8

### Prompt

Generate `src/ingestion/loader.py` using pdfplumber.

### AI Response Summary

The AI generated a reusable PDF loader that extracts page-wise text, uses custom exceptions, and integrates project logging.

### What Was Wrong

- The loader did not log when the PDF loading process started.
- It included an unnecessary `except IngestionError` block that could never be reached.

### Final Decision

Added a log message before opening the PDF and simplified the exception handling by removing redundant code.

## Refinement 9

### Prompt

Generate `src/ingestion/chunker.py` for page-preserving character-based chunking.

### AI Response Summary

The AI generated a deterministic character-based chunker that preserves page boundaries, supports overlap, skips empty pages, and produces metadata for each chunk.

### What Was Wrong

The generated implementation returns `list[dict]`, which is less type-safe than using a dedicated `TypedDict` or Pydantic model. However, introducing additional types would increase complexity without providing significant value for the internship assignment.

### Final Decision

Accepted the implementation as-is to keep the ingestion pipeline simple, readable, and interview-friendly. A stronger typed chunk representation can be added later if needed.

## Refinement 10

### Prompt

Generate `src/retrieval/embeddings.py` using Sentence-Transformers.

### AI Response Summary

The AI generated an embedding service that loads a Sentence-Transformers model once, supports single and batch embeddings, integrates logging, and raises custom retrieval exceptions.

### What Was Wrong

The generated implementation did not normalize embeddings before returning them. Normalized vectors are more appropriate for cosine similarity search with FAISS.

### Final Decision

Enabled embedding normalization while keeping the remaining implementation unchanged.

## Refinement 11

### Prompt

Generate `src/retrieval/vector_store.py` using FAISS.

### AI Response Summary

The AI generated a reusable FAISS-backed vector store with lazy initialization, metadata mapping, similarity search, and custom error handling.

### What Was Wrong

The implementation included a redundant `except RetrievalError` block that could never be reached because no code inside the `try` block explicitly raises that exception.

### Final Decision

Removed the unnecessary exception block and kept the remaining implementation unchanged.

## Refinement 12

### Prompt

Generate `src/retrieval/retrieval.py`.

### AI Response Summary

The AI generated a retriever that connects the embedding service with the FAISS vector store.

### What Was Wrong

- Exception messages duplicated information already preserved through exception chaining.
- The logger recorded the raw query string, which is unnecessary and could expose user input in logs.

### Final Decision

Simplified exception messages and switched to parameterized logging without recording the raw query text.

## Refinement 13

### Prompt

Generate `src/agents/prompt_builder.py`.

### AI Response Summary

The AI generated a deterministic prompt builder that structures the extraction prompt into instructions, schema, query, context, and output directives.

### What Was Wrong

- The chunk formatter expected a `page` field instead of the existing `page_number` field produced by the ingestion pipeline.
- An unused import (`Any`) was included.
- The JSON schema serialization did not explicitly preserve Unicode characters.

### Final Decision

Aligned the prompt builder with the existing chunk metadata, removed the unused import, and serialized the schema using `ensure_ascii=False` for better robustness.

## Refinement 14

### Prompt

Generate `src/agents/gemini_client.py`.

### AI Response Summary

The AI generated a reusable Gemini client using `ChatGoogleGenerativeAI`, loading the model once and exposing a `generate()` method for deterministic text generation.

### What Was Wrong

- The API key was initially passed as a `SecretStr` instead of extracting its value.
- Exception handling and logging were made consistent with the rest of the project.
- The model response was explicitly converted to `str` before returning for safer downstream processing.

### Final Decision

Updated the client to use `settings.google_api_key.get_secret_value()`, standardized exception handling, and returned `str(response.content)` for consistency.

## Refinement 15

### Prompt

Generate `src/agents/extraction_agent.py`.

### AI Response Summary

The AI generated an orchestration layer that coordinates prompt construction, Gemini inference, JSON parsing, and validation.

### What Was Wrong

- The implementation logged the raw user query instead of keeping logs generic.
- Empty LLM responses were not handled before JSON parsing.
- Exception handling was aligned with the project's convention by using exception chaining and simplified error messages.

### Final Decision

Updated the extraction agent to use privacy-friendly logging, detect empty model responses before parsing, and standardize exception handling across the project.

## Refinement 16

### Prompt

Generate `src/agents/validation_agent.py`.

### AI Response Summary

The AI generated a validation layer using the Pydantic `ContractExtraction` model with optional recovery logic.

### What Was Wrong

- Recovery logic was placed inside the validation layer, violating single responsibility.
- Validation errors were appended as plain strings instead of structured `ValidationNote` objects.
- Exception handling and error messages were not fully aligned with the rest of the project.
- The unused `schema` parameter remained in the interface.

### Final Decision

Simplified the validation agent to focus solely on schema validation, produce structured validation notes, and raise `ValidationError` for unrecoverable validation failures. Recovery decisions will be handled by the extraction pipeline instead.

---

# 3. AI Blindspot

(To be completed after the project is finished.)
