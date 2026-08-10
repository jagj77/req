---
name: grilling
description: |
  Execute relentless one-at-a-time questioning to extract stakeholder needs,
  design decisions, and identify ambiguities. Produces structured output for
  requirements-modeling phase.

applyTo:
  - "user wants to stress-test a plan"
  - pattern: "grill"
  - invoked_by: "interview-requirements"

protocol:
  question_style: "one-at-a-time"
  provide_recommendation: true
  wait_for_feedback: true
  explore_codebase: true

output_structure: |
  Produce structured output containing:
  - articulated_needs: Array of needs with stakeholder attribution
  - design_decisions: Array of decisions with rationale
  - identified_ambiguities: Terms/concepts that need clarification
  - terminology_introduced: New terms requiring definition
  - dependencies_identified: Component/feature interdependencies
  - open_questions: Unanswered questions and criticality level
  - status: "complete" or "incomplete"
  - ready_for_modeling: true/false

---

## Grilling Session Protocol

Interview the user relentlessly, asking **ONE question at a time**:

1. Start with needs identification
   - "What is the primary problem this solves?"
   - "Who benefits most?"
   - "How often is this needed?"

2. Walk through design tree branches systematically
   - Constraints (time, budget, resources)
   - Boundaries (in/out of scope)
   - Interdependencies (what depends on what)
   - Measurement (success metrics, KPIs)
   - Failure modes (what could go wrong)

3. For each question:
   - Provide ONE question
   - Suggest a recommended answer
   - Wait for user feedback
   - Acknowledge their response
   - Ask follow-up or move to next branch

4. Capture explicitly:
   - Exact stakeholder needs in their words
   - Decisions made and rationale
   - Areas of disagreement
   - Terms needing definition
   - Dependencies and interactions

5. When complete:
   - Summarize what you've learned
   - Ask: "Are we ready to formalize this into requirements?"
   - Produce structured output
   - Signal: "Grilling session complete. Ready for requirements-modeling phase."

**Output must be machine-readable for interview-requirements to process.**
