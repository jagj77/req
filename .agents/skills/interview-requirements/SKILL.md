---
name: interview-requirements
description: |
  Orchestrate a complete requirements engineering workflow:
  1. Run /grilling-requirements session to extract stakeholder needs
  2. Run /requirements-modeling to formalize requirements
  3. Run /requirements-writer-skill to validate and score
  4. Handle feedback loops until all requirements >= 90/100
  5. Produce final deliverable (GLOSSARY.md [shared], project-slug/requirements-set/)

applyTo:
  - "user wants to capture requirements"
  - "user wants to conduct requirements interview"
  - pattern: "interview.*requirement"

slug_transformation: |
  Convert project_name to valid directory slug:
  - Convert to lowercase
  - Replace spaces/underscores with hyphens
  - Remove special characters
  - Example: "Búsqueda Avanzada" → "busqueda-avanzada"
  - Example: "Payment Integration" → "payment-integration"

invokes:
  - skill: grilling-requirements
    with_context: [project_name, project_slug, stakeholders, scope]
    expect_output: grilling_requirements_output (needs, decisions, ambiguities, terminology, project_slug)
  
  - skill: requirements-modeling
    with_input: [grilling_requirements_output, project_slug]
    expect_output: modeling_output (glossary, requirement_candidates, adrs, project_slug)
  
  - skill: requirements-writer-skill
    with_input: [requirement_candidates, glossary, project_slug]
    expect_output: validation_output (validated_requirements, clarification_requests, quality_scores, project_slug)
  
  - skill: requirements-modeling
    when: "validation_output.any_score < 90"
    type: "feedback_loop"
    with_input: [clarification_request, project_slug]
    then_loop: "back to requirements-writer-skill"

---

## Orchestration Workflow

This is the primary orchestrator. Do NOT ask user to manually invoke other skills.
Instead, execute automatically in sequence:

**STEP 0: Project Slug Generation**
   - Capture: user's project_name (e.g., "Búsqueda Avanzada")
   - Generate: project_slug (e.g., "busqueda-avanzada")
   - Propagate: project_slug to all phases
   - All output will use: `{project_slug}/` directory structure

1. **Phase 1: Grilling-requirements** - Extract needs through relentless questioning
   - Invoke: `/grilling-requirements` with project context + project_slug
   - Collect: needs, decisions, ambiguities, terminology
   - Proceed only when session complete
   - Output includes: project_slug for downstream use

2. **Phase 2: Requirements Modeling** - Formalize and structure
   - Invoke: `/requirements-modeling` with grilling output + project_slug
   - Update: `GLOSSARY.md` (root-level, shared by all projects)
   - Create: `{project_slug}/requirements-set/` directory
   - Collect: GLOSSARY updates, requirement candidates
   - Ensure: no contradictions between requirements

3. **Phase 3: Validation** - Score and verify
   - Invoke: `/requirements-writer-skill` with requirement candidates + project_slug
   - Read: `GLOSSARY.md` (centralized, root-level)
   - Check: all requirements scored >= 90/100
   - If any score < 90: Identify ambiguities

4. **Phase 4: Feedback Loops** - Iterate on low scores
   - For each requirement scored < 90:
     - Invoke: `/requirements-modeling` with clarification request + project_slug
     - Wait: for updated `GLOSSARY.md` (root-level)
     - Invoke: `/requirements-writer-skill` again (re-evaluation) + project_slug
     - Repeat until all >= 90

5. **Phase 5: Consolidation** - Produce final deliverable
   - Verify: `GLOSSARY.md` (root-level) completeness
   - Create: `{project_slug}/requirements-set/requirements-summary.md`
   - List: all approved requirements (score >= 90) in `{project_slug}/requirements-set/`
   - Report: "Requirements engineering complete for '{project_name}'. Output in: {project_slug}/"

**Never skip phases. Always complete each phase before moving to next.**
**GLOSSARY.md is centralized at root level (shared by all projects).**
**Each project uses its own {project_slug}/requirements-set/ directory.**
