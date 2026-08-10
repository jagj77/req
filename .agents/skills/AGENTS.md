# AGENTS.md - Integración Técnica de Skills

## Visión General

Define cómo los skills `grilling`, `requirements-modeling`, y `requirements-writer-skill` se orquestan desde `interview-requirements`.

---

## Skill: interview-requirements

### Propósito
Orquestar el flujo completo de captura y documentación de requisitos.

### Configuración YAML Mejorada

```yaml
---
name: interview-requirements
description: |
  Sesión integrada de elicitación de requisitos que ejecuta:
  1. Entrevista profunda con /grilling
  2. Modelado de requisitos con /requirements-modeling
  3. Validación y escritura con /requirements-writer-skill
  
  Produce: GLOSSARY.md, requirements-set/, docs/adr/
  
applyTo:
  - "user wants to capture requirements"
  - "user wants to refine requirements"
  - "user says: requirements interview"
  - "user says: interview requirements"

disable-model-invocation: true

invokes:
  - skill: grilling
    when: "initial elicitation"
    context:
      pass: [project_description, stakeholders, scope]
      expect: [needs_articulated, design_decisions, ambiguities]
      
  - skill: requirements-modeling
    when: "after grilling produces output"
    context:
      pass: [grilling_output, existing_glossary, existing_requirements]
      expect: [glossary_updated, requirements_formalized, adrs_created]
      
  - skill: requirements-writer-skill
    when: "after requirements-modeling produces candidates"
    context:
      pass: [requirement_candidates, glossary, patterns, rules, characteristics]
      expect: [validated_requirements, verification_methods, quality_scores]
      
  - skill: requirements-modeling
    when: "requirements-writer-skill identifies ambiguities"
    context:
      type: "feedback loop"
      pass: [ambiguities_identified, requirement_id]
      expect: [clarifications_added_to_glossary]
      
  - skill: requirements-writer-skill
    when: "requirements-modeling provides clarifications"
    context:
      type: "feedback loop"
      pass: [clarified_glossary_terms, requirement_id]
      expect: [refined_requirement, improved_score]

---

## Workflow Description

Run a comprehensive requirements elicitation and formalization session:

1. Initialize the requirements environment
   - Check for existing GLOSSARY.md
   - Check for existing requirements-set/
   - Check for existing docs/adr/
   - Create if not present (lazy creation)

2. Execute /grilling session
   - Topic: Capture stakeholder needs for [project/feature]
   - Duration: Until all design tree branches explored
   - Output: Needs, decisions, ambiguities documented

3. Transition to /requirements-modeling
   - Input: Grilling output
   - Activity: Challenge language, sharpen terminology
   - Activity: Create edge-case scenarios
   - Activity: Update GLOSSARY.md in real-time
   - Activity: Document requirements in requirements-set/
   - Activity: Record ADRs

4. Validate with /requirements-writer-skill
   - Input: Requirement candidates from requirements-modeling
   - Activity: Evaluate C1-C6 characteristics
   - Activity: Check R1-R41 rules
   - Activity: Apply patterns
   - Activity: Score quality
   - Activity: Select verification methods
   - Output: Validated, corrected requirements

5. Iterate
   - If requirements-writer-skill identifies ambiguities
   - Return to requirements-modeling for clarification
   - Loop until all requirements scored ≥ 90/100

6. Produce summary
   - Create requirements-set/requirements-summary.md
   - Consolidate all outputs
   - Confirm completeness
   - Ready for design phase

---
```

### Handoff Protocol

#### Grilling → Requirements-Modeling

```
INPUT from grilling:
  • user_needs: [list of articulated needs]
  • design_decisions: [decisions made during grilling]
  • stakeholder_concerns: [areas of disagreement/ambiguity]
  • terminology: [terms used that need definition]
  • dependencies: [identified dependencies between needs]

INSTRUCTION to requirements-modeling:
  "Use these grilling outputs to:
   1. Formalize terminology into GLOSSARY.md
   2. Challenge ambiguous terms with scenarios
   3. Create structured requirement candidates
   4. Record architectural decisions as ADRs
   
   Requirement candidates should be documented in 
   requirements-set/ with this format:
   
   # REQ-NNN: [Name]
   
   **Description**: [articulated need]
   
   **Acceptance Criteria**:
   - [ ] Criterion 1
   - [ ] Criterion 2
   
   **Depends on**: [related requirements]
   
   **Glossary terms**: [terms from GLOSSARY.md]
   
   When complete, signal ready for validation."
```

#### Requirements-Modeling → Requirements-Writer-Skill

```
INPUT from requirements-modeling:
  • requirement_candidates: [list of REQ-NNN.md files]
  • glossary: [GLOSSARY.md with all defined terms]
  • architectural_decisions: [ADRs created]

INSTRUCTION to requirements-writer-skill:
  "Validate these requirement candidates:
   
   For each candidate:
   1. Evaluate against C1-C6 characteristics
   2. Check compliance with R1-R41 rules
   3. Match against patterns
   4. Apply review_algorithm
   5. Assign quality score
   6. Define verification method
   7. Produce corrected version
   
   Provide output in this format:
   
   # REQ-NNN: [Name]
   
   **Requirement (Final)**:
   [Corrected requirement text]
   
   **Quality Score**: [XX/100]
   
   **Characteristic Evaluation**:
   - C1 Necessary: [✅/❌] [rationale]
   - C2 Appropriate: [✅/❌] [rationale]
   - ... (C3-C6)
   
   **Rules Violations**: [list]
   
   **Corrections Made**: [list]
   
   **Verification Method**: [Inspection|Analysis|Demonstration|Test]
   
   **Verification Details**:
   - [specific steps/criteria]
   
   If score < 90 or ambiguities detected, request
   requirements-modeling clarification."
```

#### Requirements-Writer-Skill → Requirements-Modeling (Feedback)

```
TRIGGER: Requirement scoring < 90 OR ambiguities detected

MESSAGE to requirements-modeling:
  "REQ-NNN: [Name]
   
   Issue: [description of ambiguity/rule violation]
   
   Required clarification:
   - Is term 'X' defined as 'Y' or 'Z'?
   - Does this requirement overlap with REQ-MMM?
   - Please refine glossary entry for [term]
   
   Once clarified, return for re-evaluation."

REQUIREMENTS-MODELING RESPONSE:
  "Clarification provided:
   - Updated GLOSSARY.md: [term] redefined as [clear definition]
   - Cross-checked with REQ-MMM: [relationship clarified]
   - No overlap detected OR consolidated into REQ-ZZZ
   
   Ready for re-evaluation."

REQUIREMENTS-WRITER-SKILL RESUMES:
  "Re-evaluating REQ-NNN with updated glossary...
   New score: [YY/100]
   Status: [✅ Approved / 🔄 Still needs work]"
```

---

## Skill: grilling

### Propósito
Ejecutar cuestionamiento relentless para extraer necesidades y decisiones de diseño.

### Configuración YAML Mejorada

```yaml
---
name: grilling
description: |
  Interview the user relentlessly about a plan or design
  until reaching shared understanding. Walk design tree
  branches one-by-one, asking one question per turn.

applyTo:
  - "user wants to stress-test a plan"
  - "user says: grill me"
  - "user says: let's grill this"
  - pattern: "grill"

protocol:
  question_style: "one-at-a-time"
  recommendation: "provide recommended answer"
  wait_for_feedback: true
  explore_codebase: "if question is answerable by code inspection"
  
receives_from:
  - skill: interview-requirements
    parameter: interview_context
    contains: [project_name, stakeholders, scope, existing_decisions]

sends_to:
  - skill: requirements-modeling
    output: grilling_output
    contains: [needs_list, decisions, ambiguities, terminology, dependencies]

---

## Grilling Protocol

### Question Pattern (Always One Per Turn)

```
TURN N:
┌──────────────────────────────────────────┐
│ GRILLING SKILL ASKS:                     │
│                                          │
│ "What is [aspect of design]?"           │
│                                          │
│ My recommendation: [suggested answer]    │
└──────────────────────────────────────────┘
         ↓
USER RESPONDS
         ↓
┌──────────────────────────────────────────┐
│ GRILLING SKILL ACKNOWLEDGES              │
│ "OK, so [repeats understanding]"        │
│                                          │
│ NEXT QUESTION (based on response):      │
│ "That means [consequence]?"              │
└──────────────────────────────────────────┘
         ↓
USER RESPONDS
         ↓
[LOOP continues]
```

### Question Taxonomy

Questions should cover:

**Needs/Problems**:
- "What problem does [feature] solve?"
- "Who needs this most?"
- "How often do they need it?"
- "What's the cost of NOT having this?"

**Constraints**:
- "What's the timeline constraint?"
- "What resources are available?"
- "What are the budget limits?"
- "What technical constraints exist?"

**Boundaries**:
- "In/out of scope: [item]?"
- "Does this include [edge case]?"
- "What about [related feature]?"

**Interdependencies**:
- "Does [feature A] depend on [feature B]?"
- "What happens if [assumption] is false?"
- "Who else needs to agree to this?"

**Measurement**:
- "How will we know it's done?"
- "What's the success metric?"
- "What's unacceptable performance?"

**Failure Modes**:
- "What could go wrong?"
- "What's the worst case?"
- "What's the recovery plan?"

### Output Format

```
# Grilling Session Output

## Project: [name]
## Date: [date]
## Stakeholders: [list]

### Articulated Needs
1. [Need 1] - from [stakeholder]
2. [Need 2] - from [stakeholder]
3. [Need 3] - from [stakeholder]

### Design Decisions
1. [Decision 1] - rationale: [why]
2. [Decision 2] - rationale: [why]
3. [Decision 3] - rationale: [why]

### Identified Ambiguities
1. [Ambiguity 1] - requires definition
2. [Ambiguity 2] - requires clarification
3. [Ambiguity 3] - requires scenario testing

### Terminology Introduced
- Term 1: [context in which used]
- Term 2: [context in which used]
- Term 3: [context in which used]

### Dependencies Identified
- [Component A] depends on [Component B]
- [Feature X] depends on [Feature Y]
- [Assumption P] depends on [Decision Q]

### Questions Not Yet Answered
1. [Open question 1]
2. [Open question 2]

---
**Status**: Ready for requirements-modeling phase
```

---
```

---

## Skill: requirements-modeling

### Propósito
Afinar el modelo de requisitos, formalizar terminología, documentar decisiones.

### Configuración YAML Mejorada

```yaml
---
name: requirements-modeling
description: |
  Build and sharpen the project's requirements model by:
  - Challenging fuzzy language
  - Creating edge-case scenarios
  - Updating GLOSSARY.md in real-time
  - Documenting requirements in requirements-set/
  - Recording ADRs

applyTo:
  - "user wants to pin down requirements terminology"
  - "user wants to define requirements glossary"
  - "user wants to record architectural decisions"
  - pattern: "requirements model"

protocol:
  challenge_language: true
  scenario_testing: true
  cross_reference: "check existing requirements-set/ for conflicts"
  live_documentation: true
  lazy_creation: "only create files when content exists"

receives_from:
  - skill: grilling
    parameter: grilling_output
    
  - skill: requirements-writer-skill
    parameter: clarification_request
    type: feedback_loop

sends_to:
  - skill: requirements-writer-skill
    output: requirement_candidates
    
  - skill: requirements-writer-skill
    output: clarifications (feedback loop)
    
workflow:
  step1: "Load existing GLOSSARY.md if present"
  step2: "For each grilling output term, challenge and define"
  step3: "Create GLOSSARY.md entries immediately (don't batch)"
  step4: "Structure requirement candidates"
  step5: "Create requirements-set/REQ-NNN.md files"
  step6: "For each major decision, create ADR"
  step7: "Ready for requirements-writer-skill validation"

---

## Requirements-Modeling Activities

### Activity 1: Challenge Language

```
Grilling said: "The system must validate quickly"

CHALLENGE:
- "Your glossary defines 'Validation' - which type?
   • Data Validation (format, type, range)
   • Business Logic Validation (rules, constraints)
   • Both?"

- "What does 'quickly' mean?
   • < 100ms for single field?
   • < 1 second for form?
   • < 5 seconds for batch?"

USER CLARIFIES:
"Both data and business logic, and we need form 
validation in < 1 second"

✍️ GLOSSARY.md UPDATED:

## Validation

**Definition**: Multi-layer check process including:
1. **Data Validation**: Format, type, range checking
2. **Business Logic Validation**: Rules and constraint checking

**Context**: Applied to form submissions

**Performance**: Complete within 1 second

**Related terms**: Data_Validation, Business_Logic_Validation
```

### Activity 2: Scenario Testing

```
Requirement candidate: 
"User can create reports"

SCENARIOS:
1. "User has no permissions - what happens?"
   → Requirement: Authorization check first

2. "Database is down - what happens?"
   → Requirement: Graceful degradation strategy

3. "User creates 1M row report - what happens?"
   → Requirement: Performance bounds

4. "User cancels while creating - what happens?"
   → Requirement: Cleanup/rollback strategy

EACH scenario produces new requirements or 
refinements to existing ones.
```

### Activity 3: Document Requirements

```
REQ-001-validation.md:

# REQ-001: Form Data Validation

**Description**:
Users must be able to submit forms knowing their data
will be validated correctly, with clear error messages
if validation fails.

**Acceptance Criteria**:
- [ ] Data validation (type, format, range) completes
- [ ] Business logic validation (rules) completes
- [ ] Combined validation time < 1 second
- [ ] Error messages are specific and actionable
- [ ] User can correct and resubmit

**Depends on**:
- User authentication (REQ-XXX)
- Permission system (REQ-YYY)

**Glossary terms**:
- Validation
- Data_Validation
- Business_Logic_Validation
- User_Permission
```

### Activity 4: Record ADRs

```
docs/adr/0001-validation-timing-requirement.md:

# ADR 0001: Validation Completion Within 1 Second

## Status
Accepted

## Context
Users expect fast feedback when submitting forms.
Testing showed that performance > 1 second causes
user frustration and bounce rate increases.

Grilling session with [stakeholders] confirmed
that 1 second is the target, with 5 second maximum.

## Decision
Validation (data + business logic combined) shall
complete within 1 second for typical form submissions
(< 50 fields, < 10 validation rules).

## Rationale
- User experience: Fast feedback improves usability
- Feasibility: Achievable with current infrastructure
- Risk: None identified

## Consequences
- Backend validation must be optimized
- Database queries must be indexed
- Batch operations may need special handling
- Monitoring required for SLA tracking

## Related Requirements
- REQ-001: Form Data Validation
```

---

```

### Output Format

```
# Requirements-Modeling Session Output

## GLOSSARY.md (Updated/Created)

## Validation
**Definition**: Multi-layer check process including...
**Context**: Form submissions, API calls
**Performance**: < 1 second
**Related terms**: Data_Validation, Business_Logic_Validation

## User_Permission
**Definition**: Authorization entity that...
**Context**: Access control for features
**Related terms**: Role, Authorization

[... more terms ...]

## requirements-set/ (Created)

- REQ-001-validation.md
- REQ-002-error-handling.md
- REQ-003-performance-bounds.md
- REQ-004-auth-strategy.md
- REQ-005-data-integrity.md

## docs/adr/ (Created)

- 0001-validation-timing-requirement.md
- 0002-error-message-strategy.md
- 0003-performance-monitoring.md

---
**Status**: Ready for requirements-writer-skill validation
```

---

## Skill: requirements-writer-skill

### Propósito
Validar y refinar requisitos candidatos según INCOSE methodology.

### Configuración YAML Mejorada

```yaml
---
name: requirements-writer-skill
description: |
  Evaluate requirement candidates against:
  - Characteristics (C1-C6)
  - Rules (R1-R41)
  - Patterns
  - Review algorithm
  
  Produce quality-scored, verified, final requirements.

applyTo:
  - "requirement needs validation"
  - "user wants requirements scored"
  - "user says: review requirement"

protocol:
  evaluation_order:
    1: "Evaluate C1-C6 characteristics"
    2: "Check R1-R41 rules compliance"
    3: "Match against patterns"
    4: "Run review algorithm"
    5: "Assign score"
    6: "Select verification method"
  
  minimum_score: 90
  loop_on_low_score: true
  
  uses_files:
    - characteristics.md
    - rules.md
    - patterns.md
    - review_algorithm.md
    - requirements-engineering.md
    - definitions.md

receives_from:
  - skill: requirements-modeling
    parameter: requirement_candidates
    
sends_to:
  - skill: requirements-modeling
    parameter: clarification_request
    type: feedback_loop
    when: score < 90

---

## Validation Algorithm

### STEP 1: Parse Structure

```
INPUT:
"User shall be able to create reports"

PARSE:
- Entity: User
- Modal: shall
- Verb: create
- Object: reports

STATUS: ❌ ISSUE - Entity is wrong
RULE VIOLATED: R3 (Subject must be correct entity)
ISSUE: "User" is subject, but requirement should 
       be on SYSTEM
```

### STEP 2: Evaluate C1-C6

```
C1 Necessary: Is this essential?
   ✅ YES - Users need to create reports

C2 Appropriate: Right architecture level?
   ✅ YES - System-level capability

C3 Unambiguous: One interpretation only?
   ❌ NO - "reports" is vague
   ISSUE: What type of report? Format? Contents?

C4 Complete: What, how well, conditions?
   ❌ NO - No performance constraint
   ISSUE: How long can report generation take?

C5 Singular: One obligation?
   ✅ YES - Create operation only

C6 Feasible: Achievable?
   ⚠️ UNCERTAIN - Depends on report complexity
```

### STEP 3: Check R1-R41 Rules

```
R1 Complete sentence: Subject+Shall+Verb+Object
   ❌ NO - Missing object precision

R2 Active voice
   ✅ YES

R3 Correct entity
   ❌ NO - Subject should be System/Reporting_Module

R4 Defined terms
   ❌ NO - "reports" not in GLOSSARY.md

R7 No vague terms
   ❌ NO - "reports" is vague

...
```

### STEP 4: Run Review Algorithm

```
Algorithm (from review_algorithm.md):

1. Identify entity
2. Identify SHALL
3. Identify verb
4. Identify object
5. Identify conditions
6. Check measurability
7. Check units
8. Check glossary terms
9. Evaluate C1-C9
10. Evaluate applicable R1-R41
11. Select verification method
12. Produce corrected requirement

Scoring:
- 100: No violations
- 90: Minor style issues
- 70: Multiple rule violations
- 50: Ambiguous or unverifiable
```

### STEP 5-6: Score & Verify

```
CURRENT SCORE: 60/100 (Multiple violations)

VIOLATIONS:
- R3: Wrong entity (User vs System)
- R4: Undefined terms (reports)
- R7: Vague language (reports)
- C3: Ambiguous (what is a report?)
- C4: Incomplete (no performance criteria)

CORRECTIONS NEEDED:
1. Change entity to Reporting_System
2. Define "Report" type (PDF, JSON, HTML?)
3. Add performance criteria
4. Add conditions (report size, data range)

PROPOSED CORRECTION:
"The Reporting_System shall generate PDF_Report 
 containing [specific data], within 5 seconds, 
 initiated by authorized User with valid Report_Query."

VERIFICATION METHOD: Test
  - Automated report generation test
  - Verify PDF output format
  - Measure generation time
  - Confirm data accuracy

NEW SCORE: 92/100 ✅
```

### Output Format

```
# REQ-001: Report Generation

## Requirement (Final)
"The Reporting_System shall generate PDF_Report 
 containing specified data fields, within 5 seconds, 
 in response to valid Report_Query from authorized User."

## Quality Evaluation

### Characteristics
| Char | Status | Rationale |
|------|--------|-----------|
| C1 Necessary | ✅ | Stakeholder need: users export data |
| C2 Appropriate | ✅ | System capability, not user capability |
| C3 Unambiguous | ✅ | PDF_Report clearly defined in glossary |
| C4 Complete | ✅ | What (PDF), How well (5 sec), Conditions (authorized, valid query) |
| C5 Singular | ✅ | One obligation: generate |
| C6 Feasible | ✅ | Achievable with current PDF library |

### Rules Compliance
| Rule | Status | Comment |
|------|--------|---------|
| R1 | ✅ | Complete sentence with S+S+V+O |
| R2 | ✅ | Active voice (shall generate) |
| R3 | ✅ | Correct entity: Reporting_System |
| R4 | ✅ | All terms defined: PDF_Report, Report_Query, User |
| R7 | ✅ | No vague terms (5 seconds, specified data fields) |
| R8 | ✅ | No escape clauses |
| R15 | ✅ | Conditions explicit (authorized, valid query) |

### Quality Score
**92/100** ✅

### Violations Corrected
1. Entity changed: User → Reporting_System
2. Object clarified: reports → PDF_Report
3. Performance added: 5 seconds
4. Conditions added: authorized User, valid Query

### Verification Method
**Test** (Automated)
- Test 1: PDF generation with valid query
  - Input: Valid Report_Query
  - Expected: PDF_Report generated within 5 seconds
  - Success criteria: Output valid PDF, time < 5s
  
- Test 2: Authorization check
  - Input: Report_Query from unauthorized User
  - Expected: Request denied
  - Success criteria: No report generated, error returned
  
- Test 3: Data accuracy
  - Input: Report_Query with known dataset
  - Expected: PDF contains correct data fields
  - Success criteria: All fields present and accurate

### Related Glossary Terms
- PDF_Report
- Report_Query
- Reporting_System
- User (in authorization context)

### Related Requirements
- REQ-XXX: User Authentication
- REQ-YYY: Data Validation
- REQ-ZZZ: Performance Bounds

---
**Status**: ✅ APPROVED FOR DESIGN
```

---

```

---

## Integration Points

### 1. Glossary Synchronization

```
ALL SKILLS must check GLOSSARY.md before:
- Introducing a new term
- Evaluating a requirement using a term
- Challenging terminology

If term not in glossary:
  → Requirements-Modeling adds it
  → Other skills wait for update
  → No requirement moves forward until glossary stable
```

### 2. Feedback Loop Protocol

```
Requirements-Writer → Requirements-Modeling:

MESSAGE:
"REQ-001 requires clarification on 'Report' definition.
 Glossary says: 'formatted data output'
 But requirement needs: format type (PDF/JSON/HTML)
 
 Please update GLOSSARY with:
 - Report_PDF
 - Report_JSON  
 - Report_HTML
 
 Then I can rescore REQ-001"

Requirements-Modeling → Requirements-Writer:

MESSAGE:
"Updated GLOSSARY.md with:
 - Report_PDF: Portable Document Format output...
 - Report_JSON: JSON structured output...
 - Report_HTML: HTML web-viewable output...
 
 Ready for re-evaluation of REQ-001"

Requirements-Writer:

"Re-evaluating REQ-001 with clarified glossary...
 New score: 93/100 ✅
 REQ-001 APPROVED"
```

### 3. Output Consolidation

```
interview-requirements consolidates:

✅ GLOSSARY.md
   (from requirements-modeling)

✅ requirements-set/
   - REQ-001.md (final, scored)
   - REQ-002.md (final, scored)
   - requirements-summary.md

✅ docs/adr/
   - 0001-*.md
   - 0002-*.md
   - (from requirements-modeling)

✅ COMPLETION REPORT
   - All requirements scored ≥ 90
   - All terms defined
   - All decisions documented
   - Traceability verified
```

---

## Summary

| Skill | Role | Input | Output | Scores |
|-------|------|-------|--------|--------|
| grilling | Extraction | Project info | Needs, decisions | N/A |
| requirements-modeling | Formalization | Grilling output | GLOSSARY, REQ candidates, ADRs | N/A |
| requirements-writer-skill | Validation | REQ candidates | Final REQ, verified, scored | 50-100 |
| interview-requirements | Orchestration | User request | Consolidated deliverable | N/A |

This architecture ensures:
✅ One question at a time (grilling)
✅ Live documentation (glossary)
✅ Systematic validation (requirements)
✅ Quality gates (minimum 90 score)
✅ Complete traceability (needs → req → verify → validate)
