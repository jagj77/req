---
name: interview-requirements
description: |
  Orchestrate a complete requirements engineering workflow:
  1. Run /grilling session to extract stakeholder needs
  2. Run /requirements-modeling to formalize requirements
  3. Run /requirements-writer-skill to validate and score
  4. Handle feedback loops until all requirements >= 90/100
  5. Produce final deliverable (GLOSSARY.md, requirements-set/, docs/adr/)

applyTo:
  - "user wants to capture requirements"
  - "user wants to conduct requirements interview"
  - pattern: "interview.*requirement"

invokes:
  - skill: grilling
    with_context: [project_name, stakeholders, scope]
    expect_output: grilling_output (needs, decisions, ambiguities, terminology)
  
  - skill: requirements-modeling
    with_input: grilling_output
    expect_output: modeling_output (glossary, requirement_candidates, adrs)
  
  - skill: requirements-writer-skill
    with_input: [requirement_candidates, glossary]
    expect_output: validation_output (validated_requirements, clarification_requests, quality_scores)
  
  - skill: requirements-modeling
    when: "validation_output.any_score < 90"
    type: "feedback_loop"
    with_input: clarification_request
    then_loop: "back to requirements-writer-skill"

---

## Orchestration Workflow

This is the primary orchestrator. Do NOT ask user to manually invoke other skills.
Instead, execute automatically in sequence:

1. **Phase 1: Grilling** - Extract needs through relentless questioning
   - Invoke: `/grilling` with project context
   - Collect: needs, decisions, ambiguities, terminology
   - Proceed only when session complete

2. **Phase 2: Requirements Modeling** - Formalize and structure
   - Invoke: `/requirements-modeling` with grilling output
   - Collect: GLOSSARY.md updates, requirement candidates, ADRs
   - Ensure: no contradictions between requirements

3. **Phase 3: Validation** - Score and verify
   - Invoke: `/requirements-writer-skill` with requirement candidates
   - Check: all requirements scored >= 90/100
   - If any score < 90: Identify ambiguities

4. **Phase 4: Feedback Loops** - Iterate on low scores
   - For each requirement scored < 90:
     - Invoke: `/requirements-modeling` with clarification request
     - Wait: for updated glossary
     - Invoke: `/requirements-writer-skill` again (re-evaluation)
     - Repeat until all >= 90

5. **Phase 5: Consolidation** - Produce final deliverable
   - Verify: GLOSSARY.md completeness
   - Create: requirements-set/requirements-summary.md
   - List: all approved requirements (score >= 90)
   - Report: "Requirements engineering complete. Ready for design phase."

**Never skip phases. Always complete each phase before moving to next.**
