---
name: interview-requirements
description: |
  Orchestrate a complete requirements engineering workflow:
  1. Run /grilling-requirements session to extract stakeholder needs
  2. Run /requirements-modeling to formalize requirements
  3. Run /requirements-writer-skill to validate and score
  4. Handle feedback loops until all requirements >= 90/100
  5. Produce final deliverable (GLOSSARY.md [shared], project-slug/requirements-set/)
  6. Support multi-language: Spanish (es) or English (en)

applyTo:
  - "user wants to capture requirements"
  - "user wants to conduct requirements interview"
  - pattern: "interview.*requirement"

language_detection: |
  Detect project language from project_name (or read from .req-config.yml default):
  - If contains Spanish accents (á, é, í, ó, ú, ñ) → "es"
  - Else → "en"
  - Can override with explicit language parameter: language="es" or language="en"
  - Single execution = single language (no duplicates)
  - Global config: .req-config.yml (default_language, language_detection_strategy)

slug_transformation: |
  Convert project_name to valid directory slug:
  - Convert to lowercase
  - Replace spaces/underscores with hyphens
  - Remove special characters
  - Example: "Búsqueda Avanzada" → "busqueda-avanzada"
  - Example: "Payment Integration" → "payment-integration"

invokes:
  - skill: grilling-requirements
    with_context: [project_name, project_slug, stakeholders, scope, language]
    expect_output: grilling_requirements_output (needs, decisions, ambiguities, terminology, project_slug, language)
  
  - skill: requirements-modeling
    with_input: [grilling_requirements_output, project_slug, language]
    expect_output: modeling_output (glossary, requirement_candidates, project_slug, language)
  
  - skill: requirements-writer-skill
    with_input: [requirement_candidates, glossary, project_slug, language]
    expect_output: validation_output (validated_requirements, clarification_requests, quality_scores, project_slug, language)
  
  - skill: requirements-modeling
    when: "validation_output.any_score < 90"
    type: "feedback_loop"
    with_input: [clarification_request, project_slug, language]
    then_loop: "back to requirements-writer-skill"

---

## Orchestration Workflow

This is the primary orchestrator. Do NOT ask user to manually invoke other skills.
Instead, execute automatically in sequence:

**STEP 0: Project Slug Generation & Language Detection**
   - Capture: user's project_name (e.g., "Búsqueda Avanzada")
   - Generate: project_slug (e.g., "busqueda-avanzada")
   - Detect: language from project_name (auto or explicit parameter)
   - Propagate: project_slug + language to all phases
   - All output will use: `{project_slug}/` directory structure in detected language

1. **Phase 1: Grilling-requirements** - Extract needs through relentless questioning
   - Invoke: `/grilling-requirements` with project context + project_slug + language
   - Questions asked in: detected language (Spanish or English)
   - Collect: needs, decisions, ambiguities, terminology
   - Proceed only when session complete
   - Output includes: project_slug, language for downstream use

2. **Phase 2: Requirements Modeling** - Formalize and structure
   - Invoke: `/requirements-modeling` with grilling output + project_slug + language
   - Update: `GLOSSARY.md` (root-level, shared by all projects, in current language)
   - Create: `{project_slug}/requirements-set/` directory
   - Generate: REQ-NNN.md (single language, e.g., REQ-001.md)
   - Collect: GLOSSARY updates, requirement candidates, in specified language
   - Ensure: no contradictions between requirements

3. **Phase 3: Validation** - Score and verify
   - Invoke: `/requirements-writer-skill` with requirement candidates + project_slug + language
   - Read: `GLOSSARY.md` (centralized, root-level, in detected language)
   - Check: all requirements scored >= 90/100
   - Feedback messages in: detected language
   - If any score < 90: Identify ambiguities

4. **Phase 4: Feedback Loops** - Iterate on low scores
   - For each requirement scored < 90:
     - Invoke: `/requirements-modeling` with clarification request + project_slug + language
     - Wait: for updated `GLOSSARY.md` (root-level, same language)
     - Invoke: `/requirements-writer-skill` again (re-evaluation) + project_slug + language
     - Repeat until all >= 90

5. **Phase 5: Consolidation** - Produce final deliverable
   - Verify: `GLOSSARY.md` (root-level) completeness in current language
   - Create: `{project_slug}/requirements-set/requirements-summary.md` (in current language)
   - List: all approved requirements (score >= 90) in `{project_slug}/requirements-set/` (single language)
   - Report: "Requirements engineering complete for '{project_name}' (language: {language}). Output in: {project_slug}/"

**Multi-Language Support (Single Language per Execution):**
- ✅ Questions in grilling-requirements: Spanish (es) or English (en)
- ✅ GLOSSARY.md: Single source, entries in current language only
- ✅ REQ-NNN.md: No language suffix (single language per run)
- ✅ All feedback: In current language
- ✅ Configuration: .req-config.yml defines default_language

**Never skip phases. Always complete each phase before moving to next.**
**GLOSSARY.md is centralized at root level (shared by all projects, single language per execution).**
**Each project uses its own {project_slug}/requirements-set/ directory with single-language files.**
