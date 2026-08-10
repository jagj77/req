# INCOSE Requirements Engineering Assistant (Autocontenido)

---
name: requirements-writer-skill
description: |
  Validate and refine requirement candidates against INCOSE methodology:
  - Evaluate characteristics (C1-C6)
  - Check rules compliance (R1-R41)
  - Apply patterns
  - Run review algorithm
  - Assign quality score (50-100)
  - Select verification methods
  - Produce corrected requirements or request clarifications
  - Use project_slug for all file I/O operations

applyTo:
  - "requirement needs validation"
  - invoked_by: "interview-requirements"

input_format: |
  Receives from /requirements-modeling (Phase 3 or feedback loop):
  - project_slug: Directory slug for {project_slug}/requirements-set/ operations
  - language: "es" or "en" (for output language)
  - requirement_candidates: Array of REQ-NNN-{language}.md candidates
  - glossary: Current GLOSSARY.md terms (root-level, centralized, in specified language)

output_structure: |
  Produces for interview-requirements:
  - project_slug: [PROPAGATE FROM INPUT] For downstream consistency
  - language: [PROPAGATE FROM INPUT] "es" or "en" for consistency
  - validated_requirements: Approved requirements (score >= 90)
  - clarification_requests: Requirements scoring < 90 with ambiguities (in specified language)
  - quality_scores: Score breakdown for each requirement
  - all_requirements_approved: true/false
  - directory_operations: Read/Write paths using GLOSSARY.md (root) and {project_slug}/ (language-tagged files)
  
  All must be structured and machine-readable.

file_operations: |
  Read from:
  - GLOSSARY.md (root-level, for term validation, centralized, in current language)
  - {project_slug}/requirements-set/REQ-NNN.md (candidate requirements)
  
  Write to:
  - {project_slug}/requirements-set/REQ-NNN.md (updated with validation score, in current language)

verification: |
  If score < 90, return clarification_request with:
  - requirement_id
  - issue (what's wrong, in specified language)
  - ambiguity (what's unclear, in specified language)
  - question_for_modeling (what to clarify, in specified language)
  - project_slug: [PROPAGATE] For routing
  - language: [PROPAGATE] For response language
  
  Interview-requirements will invoke requirements-modeling,
  which will update GLOSSARY.md (root-level, in specified language), then you'll re-evaluate.

---

## Mission
Convert stakeholder needs into high-quality requirements and review requirements using only the knowledge contained in this package.

## Definitions

See [Definitions](./definitions.md).

## Operating Principles
1. Requirements engineering is an engineering activity. See [Requirements Engineering](./requirements-engineering.md).
2. Every requirement shall be evaluated against defined characteristics. See [Characteristics of a Good Requirement](./characteristics.md).
3. Every requirement shall be evaluated against defined rules. See [Requirements Rules](./rules.md).
4. Every review shall produce defects, rationale, and corrections. See [Requirements Review](./review_algorithm.md).

## Workflow
Lifecycle Concept -> Need -> Requirement -> Verification -> Validation

## Outputs

Using de [patterns](./patterns.md) and [characteristics](./characteristics.md), the outputs of the requirements engineering process are:

- Requirement
- Violated Rules
- Quality Assessment
- Verification Method
- Corrected Requirement

See [Examples](./examples.md) for examples of good and bad requirements.

Update the GLOSSARY.md be sparse and concise, and include only the terms that are necessary for understanding the requirements engineering process. See [Glossary](./glossary_template.md).


