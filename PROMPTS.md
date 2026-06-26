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

---

# 3. AI Blindspot

(To be completed after the project is finished.)
