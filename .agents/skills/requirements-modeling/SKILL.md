---
name: requirements-modeling
description: |
  Formalize and sharpen the requirements model by:
  - Challenging fuzzy language from grilling output
  - Creating edge-case scenarios
  - Updating GLOSSARY.md in real-time
  - Documenting requirement candidates
  - Recording architectural decisions (ADRs)

applyTo:
  - "user wants to pin down terminology"
  - "user wants to define glossary"
  - "user wants to record decisions"
  - invoked_by: "interview-requirements"

input_format: |
  Receives from /grilling (Phase 2) OR /requirements-writer-skill (feedback loop):
  
  Phase 2 Input (from grilling):
  - project_slug: Directory slug for {project_slug}/requirements-set/ and {project_slug}/docs/adr/
  - articulated_needs
  - design_decisions
  - identified_ambiguities
  - terminology_introduced
  
  Feedback Loop Input (from requirements-writer-skill):
  - project_slug: Directory slug for project-specific directories
  - requirement_id: "REQ-NNN"
  - issue: description of ambiguity
  - required_clarification: what needs clarifying

output_structure: |
  Produces for interview-requirements:
  - project_slug: [PROPAGATE FROM INPUT] For downstream consistency
  - glossary_updates: New/updated terms in GLOSSARY.md (root-level, shared)
  - requirement_candidates: Array of REQ-NNN candidates
  - architectural_decisions: Array of ADRs for {project_slug}/docs/adr/
  - clarifications_provided: (for feedback loops)
  - directory_structure: {project_slug}/ [created if not exists]
  
  All must be structured and machine-readable.

file_operations: |
  Create/Update these directories and files:
  - GLOSSARY.md (root-level, centralized, shared by all projects)
  - {project_slug}/requirements-set/REQ-NNN.md (each requirement)
  - {project_slug}/docs/adr/NNNN-decision-name.md (each decision)
  - {project_slug}/requirements-set/requirements-summary.md (final)

---

# Requirements Modeling

Actively build and sharpen the project's requirements model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single requirements context:

```
/REQ
├── GLOSSARY.md
├── requirements-set/
│   ├── requirements-001.md
│   ├── requirements-002.md
│   └── requirements-summary.md
└── docs/
    └── adr/
        ├── 0001-authentication-strategy.md
        └── 0002-data-validation-approach.md
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple requirements contexts. The map points to where each one lives:

```
/REQ
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── auth/
│   │   ├── GLOSSARY.md
│   │   ├── requirements-set/
│   │   └── docs/adr/                 ← context-specific decisions
│   └── payments/
│       ├── GLOSSARY.md
│       ├── requirements-set/
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `requirements-set/` exists, create it when the first requirement document is needed. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'requirement' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'validation' — do you mean Data Validation or Business Logic Validation? Those are different requirements."

### Discuss concrete scenarios

When requirement relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between requirements.

### Cross-reference with existing requirements

When the user states a new requirement, check whether it conflicts with, depends on, or duplicates existing requirements in `requirements-set/`. If you find a contradiction or overlap, surface it: "You defined 'user authentication' in requirements-001.md, but this seems to add multi-factor authentication — should they be combined?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up — capture them as they happen. Use a clear format:

```markdown
## Term Name

**Definition**: Clear, concise definition of the requirement or concept.

**Context**: Where and how this term is used.

**Related terms**: Links to related glossary entries.
```

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Document requirements in requirements-set/

When new requirements emerge or are refined, group them into `requirements-set/` documents by category or feature area. Each document should:

1. **Identify the requirement** — clear, unique identifier
2. **Describe the need** — what problem does this solve?
3. **Define acceptance criteria** — how do we know when it's done?
4. **Link to glossary terms** — which glossary entries does this require?
5. **Note dependencies** — does this depend on other requirements?

Use this format:

```markdown
# Requirements: [Category/Feature Name]

## REQ-001: [Short requirement name]

**Description**: What the user needs or the system must do.

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Depends on**: REQ-XXX, REQ-YYY

**Related glossary terms**: [Term 1], [Term 2]

---

## REQ-002: [Another requirement]
...
```

