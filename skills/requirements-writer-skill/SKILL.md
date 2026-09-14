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
  - /req/GLOSSARY.md (root-level, for term validation, centralized, in current language)
  - /req/{project_slug}/requirements-set/REQ-NNN.md (candidate requirements)
  - This skill's own reference docs in skills/requirements-writer-skill/
    (rules.md, characteristics.md, patterns.md, definitions.md,
    requirements-engineering.md, review_algorithm.md, examples.md,
    glossary_template.md) — read-only.

  Write to:
  - /req/{project_slug}/requirements-set/REQ-NNN.md (updated with validation
    score and corrections, in current language)
  - /req/{project_slug}/requirements-set/requirements-summary.md (only
    when finalizing, in current language)

scope_guard: |
  Inherited from `interview-requirements` and tech-stack agnostic:

  ALLOWED file operations:
    READ:  /req/GLOSSARY.md, /req/{slug}/requirements-set/REQ-NNN.md,
           this skill's own reference docs (skills/requirements-writer-skill/*)
    WRITE: /req/{slug}/requirements-set/REQ-NNN.md,
           /req/{slug}/requirements-set/requirements-summary.md

  FORBIDDEN actions:
    - Modify any source code, config, build manifest, schema, migration,
      test file, IaC file, CI config — in any tech stack (Laravel,
      Django, Rails, Spring, Express, FastAPI, .NET, Go, React, Vue,
      Angular, Svelte, mobile, infra, embedded, etc.).
    - Modify docs/, README*, CONTEXT*, or any existing project
      documentation.
    - Modify your own reference docs (rules.md, characteristics.md,
      patterns.md, etc.) or sibling skills.
    - Modify /req/GLOSSARY.md directly — if a term needs definition,
      return a clarification_request to the orchestrator and let
      requirements-modeling update it. This preserves single-writer
      ownership of the glossary.
    - Run install / build / migrate / deploy / commit / push.

  self_check: |
    Before returning validated_requirements, run:
      git status --short -- ':!req' ':!skills'
    Anything modified outside /req/ and your own skill home is a leak.
    Revert immediately with `git checkout -- <path>` and warn the
    user.

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

Phase 3 (Validation) and Phase 4 (Feedback Loop) of the
`interview-requirements` orchestrator. Each invocation follows the
same five steps, looping on any requirement that scores below 90.

1. **Receive input.** Read the `input_format` payload from the
   orchestrator: `project_slug`, `language` (es|en),
   `requirement_candidates` (paths under
   `/req/{project_slug}/requirements-set/REQ-NNN.md`), and the current
   `/req/GLOSSARY.md` (root-level, centralized, in the specified
   language).
2. **Load references.** Read this skill's own reference docs
   (read-only): `definitions.md`, `requirements-engineering.md`,
   `characteristics.md`, `rules.md`, `patterns.md`,
   `review_algorithm.md`, `examples.md`, `glossary_template.md`. Do
   NOT load sibling skills or any path outside
   `skills/requirements-writer-skill/` and `/req/`.
3. **Evaluate each candidate.** For every requirement:
   - Apply characteristics C1–C6 (`characteristics.md`).
   - Check rules R1–R41 (`rules.md`).
   - Match against patterns (`patterns.md`).
   - Run the review algorithm (`review_algorithm.md`): produce
     defects, rationale, corrections, and a verification method.
   - Assign a quality score in the range 50–100.
4. **Persist results.** Update each
   `/req/{project_slug}/requirements-set/REQ-NNN.md` with the
   validation score and any corrections (current language only —
   never mix es/en in one file).
5. **Return output.** Produce the `output_structure` payload:
   - `validated_requirements` — those with score ≥ 90.
   - `clarification_requests` — those with score < 90; each entry has
     `requirement_id`, `issue` (current language), `ambiguity`
     (current language), `question_for_modeling` (current language),
     `project_slug`, `language`.
   - `quality_scores` — score breakdown per requirement.
   - `all_requirements_approved` — boolean.
   - `project_slug` and `language` — propagated from input for routing.

When `all_requirements_approved` is false, the orchestrator invokes
`requirements-modeling` to update `GLOSSARY.md`, then re-invokes this
skill until every requirement scores ≥ 90. This skill MUST NOT update
`/req/GLOSSARY.md` directly — single-writer ownership belongs to
`requirements-modeling`.

## Outputs

Using de [patterns](./patterns.md) and [characteristics](./characteristics.md), the outputs of the requirements engineering process are:

- Requirement
- Violated Rules
- Quality Assessment
- Verification Method
- Corrected Requirement

See [Examples](./examples.md) for examples of good and bad requirements.

Update the GLOSSARY.md be sparse and concise, and include only the terms that are necessary for understanding the requirements engineering process. See [Glossary](./glossary_template.md).


