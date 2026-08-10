# IMPLEMENTATION.md - Cómo Hacer Funcionar la Orquestación

## Propósito

Este documento especifica **exactamente qué cambios** necesita cada SKILL.md para que la orquestación automática de `interview-requirements` funcione correctamente.

**AGENTS.md** = Especificación (QUÉ debe hacer)
**IMPLEMENTATION.md** = Instrucciones (CÓMO implementarlo)
**SKILL.md actual** = Punto de partida (DÓNDE cambiar)

---

## Flujo que Necesitamos

```
USER: /interview-requirements "Búsqueda Avanzada"
  ↓
[interview-requirements/SKILL.md]
  - Recibe input del usuario
  - Inicializa contexto (proyecto, stakeholders, scope)
  - INVOCA /grilling CON PARÁMETROS
  ↓
[grilling/SKILL.md]
  - Recibe contexto
  - Ejecuta sesión
  - RETORNA: grilling_output (JSON/estructura)
  ↓
[interview-requirements/SKILL.md]
  - Captura grilling_output
  - INVOCA /requirements-modeling CON grilling_output
  ↓
[requirements-modeling/SKILL.md]
  - Recibe grilling_output
  - Ejecuta actividades
  - RETORNA: requirement_candidates (JSON)
  ↓
[interview-requirements/SKILL.md]
  - Captura requirement_candidates
  - INVOCA /requirements-writer-skill CON requirement_candidates
  ↓
[requirements-writer-skill/SKILL.md]
  - Recibe requirement_candidates
  - Valida cada uno
  - Score < 90? → RETORNA clarification_request
  ↓
[interview-requirements/SKILL.md]
  - Detecta score < 90
  - INVOCA /requirements-modeling CON clarification_request (LOOP)
  ↓
[requirements-modeling/SKILL.md] (Loop)
  - Recibe clarification_request
  - Actualiza GLOSSARY.md
  - RETORNA: clarifications
  ↓
[interview-requirements/SKILL.md]
  - Captura clarifications
  - INVOCA /requirements-writer-skill CON clarified_glossary
  ↓
[requirements-writer-skill/SKILL.md] (Re-evaluation)
  - Score ≥ 90? → ✅ APROBADO
  ↓
[interview-requirements/SKILL.md]
  - Consolida todos los outputs
  - Genera requirements-summary.md
  - ✅ WORKFLOW COMPLETO
```

---

## CAMBIO 1: interview-requirements/SKILL.md

### Estado Actual
```yaml
---
name: interview-requirements
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Run a `/grilling` session, using the `/requirements-writer-skill` skill.
```

### Problema
- No especifica cómo pasar parámetros
- No menciona qué datos capturar
- No define la lógica de orquestación
- `disable-model-invocation: true` puede bloquear invocaciones

### Solución: Interview-Requirements Mejorado

```yaml
---
name: interview-requirements
description: |
  Orchestrate a complete requirements engineering workflow:
  1. Run /grilling session to extract needs
  2. Run /requirements-modeling to formalize requirements
  3. Run /requirements-writer-skill to validate and score
  4. Handle feedback loops and produce final deliverable

applyTo:
  - "user wants to capture requirements"
  - "user wants to conduct requirements interview"
  - "user says: interview requirements"
  - pattern: "interview.*requirement"

parameters:
  project_name: "Name of the project or feature"
  stakeholders: "List of stakeholders (comma-separated)"
  scope: "Preliminary scope description"
  
orchestration:
  enable: true
  async: false
  timeout: null

workflow:
  step1_grilling:
    skill: grilling
    pass:
      project_name: $project_name
      stakeholders: $stakeholders
      scope: $scope
    expect:
      output_var: grilling_output
      contains: [needs, decisions, ambiguities, terminology, dependencies]
    
  step2_modeling:
    skill: requirements-modeling
    pass:
      grilling_output: $grilling_output
    expect:
      output_var: modeling_output
      contains: [glossary_updates, requirement_candidates, adrs]
    
  step3_validation:
    skill: requirements-writer-skill
    pass:
      requirement_candidates: $modeling_output.requirement_candidates
      glossary: $modeling_output.glossary_updates
    expect:
      output_var: validation_output
      contains: [validated_requirements, quality_scores, verification_methods]
    
  step4_feedback_loop:
    condition: "validation_output.any_score < 90"
    if_true:
      skill: requirements-modeling
      pass:
        clarification_request: $validation_output.ambiguities
        requirement_id: $validation_output.failing_requirement_id
      expect:
        output_var: clarifications
        contains: [updated_glossary_terms]
      then_step: step3_validation (re-run with clarified_glossary)
  
  step5_consolidate:
    action: "Produce final deliverable"
    outputs:
      - GLOSSARY.md
      - requirements-set/requirements-summary.md
      - docs/adr/*.md
      - requirements-set/REQ-*.md (all scored >= 90)

---

## Orchestration Instructions

**DO NOT** ask the user to manually invoke each skill. Instead:

1. Initialize the requirements environment
   - Check for existing REQ/, GLOSSARY.md, requirements-set/, docs/adr/
   - Create if not present

2. Grilling Phase
   - Call: `/grilling with context` (see AGENTS.md for protocol)
   - Capture output structure (needs, decisions, ambiguities)
   - Do not proceed until user confirms readiness

3. Modeling Phase
   - Call: `/requirements-modeling with grilling_output`
   - Wait for completion
   - Capture: GLOSSARY.md, requirement_candidates, ADRs

4. Validation Phase
   - Call: `/requirements-writer-skill with requirement_candidates`
   - For each requirement:
     - If score >= 90: ✅ Move to approved list
     - If score < 90: Check if ambiguities can be clarified

5. Feedback Loop (if needed)
   - Identify which requirements scored < 90
   - For each ambiguity:
     - Call: `/requirements-modeling with clarification_request`
     - Wait for GLOSSARY.md update
     - Call: `/requirements-writer-skill again` (re-evaluate)
   - Continue until ALL requirements >= 90

6. Consolidation
   - Verify GLOSSARY.md completeness
   - Create requirements-set/requirements-summary.md
   - List all approved requirements (score >= 90)
   - List all ADRs created
   - Report: "Requirements engineering complete. Ready for design phase."

---
```

**Cambios Clave**:
- ✅ Define parámetros de entrada
- ✅ Especifica qué skills invocar en qué orden
- ✅ Define qué datos esperar de cada skill
- ✅ Implementa feedback loops
- ✅ Marca condiciones para iteración
- ✅ Define consolidación final

---

## CAMBIO 2: grilling/SKILL.md

### Estado Actual
```yaml
---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

### Problema
- No especifica qué retornar
- No define estructura de output
- No menciona cómo será invocado programáticamente

### Solución: Grilling Mejorado

```yaml
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

parameters:
  project_name: "Name of project/feature"
  stakeholders: "List of stakeholders"
  scope: "Scope of questioning"

protocol:
  question_style: "one-at-a-time"
  provide_recommendation: true
  wait_for_feedback: true
  explore_codebase: true

output_format: |
  Structure your output as JSON-compatible format:
  
  {
    "session_metadata": {
      "project_name": "[name]",
      "date": "[ISO date]",
      "stakeholders": ["[list]"],
      "duration_minutes": N
    },
    "articulated_needs": [
      { "need": "[description]", "stakeholder": "[who]", "priority": "high|medium|low" }
    ],
    "design_decisions": [
      { "decision": "[what was decided]", "rationale": "[why]", "impacts": ["[affected areas]"] }
    ],
    "identified_ambiguities": [
      { "ambiguity": "[description]", "requires": "definition|clarification|scenario_testing" }
    ],
    "terminology_introduced": [
      { "term": "[word/phrase]", "context": "[how used]", "definition_needed": true|false }
    ],
    "dependencies_identified": [
      { "from": "[component A]", "to": "[component B]", "type": "depends_on|blocks|enables" }
    ],
    "open_questions": [
      { "question": "[unanswered]", "criticality": "high|medium|low" }
    ],
    "status": "complete|incomplete",
    "ready_for_modeling": true|false
  }

send_to: requirements-modeling

---

## Grilling Execution

Interview user one question at a time:

1. **Start with needs identification**
   - "What is the primary problem this solves?"
   - "Who benefits most?"
   - "How often is this needed?"

2. **Move through design tree branches**
   - Ask about constraints
   - Ask about boundaries
   - Ask about interdependencies
   - Ask about measurement/success
   - Ask about failure modes

3. **For each branch:**
   - Ask ONE question
   - Provide recommended answer
   - Wait for user response
   - Acknowledge understanding
   - Ask follow-up or move to next branch

4. **Capture explicitly:**
   - Write down exact stakeholder needs in their words
   - Record decisions made
   - Note areas of disagreement
   - Identify terms that need definition
   - Map dependencies

5. **When complete:**
   - User says they're satisfied
   - All design tree branches explored
   - Produce structured JSON output (see output_format above)
   - Signal: "Ready for requirements-modeling phase"

---
```

**Cambios Clave**:
- ✅ Define estructura JSON de output exacta
- ✅ Especifica qué datos capturar
- ✅ Marca dónde se envía el output (`send_to: requirements-modeling`)
- ✅ Define criterio de completitud

---

## CAMBIO 3: requirements-modeling/SKILL.md

### Estado Actual
```yaml
---
name: requirements-modeling
description: Build and sharpen a project's requirements model. Use when the user wants to pin down requirements terminology, define a requirements glossary, record architectural decisions, or when another skill needs to maintain the requirements model.
---

# Requirements Modeling

[60+ líneas de contenido...]
```

### Problema
- No especifica qué input espera
- No define qué output producir en qué formato
- No menciona feedback loops

### Solución: Requirements-Modeling Mejorado

```yaml
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
  Receives output from /grilling skill:
  
  {
    "articulated_needs": [...],
    "design_decisions": [...],
    "identified_ambiguities": [...],
    "terminology_introduced": [...]
  }
  
  OR receives clarification request from /requirements-writer-skill:
  
  {
    "type": "clarification_request",
    "requirement_id": "REQ-NNN",
    "issue": "[description of ambiguity]",
    "required_clarification": "[what needs clarifying]"
  }

output_format: |
  Produces:
  
  {
    "glossary_updates": {
      "file": "REQ/GLOSSARY.md",
      "new_terms": [
        { "term": "[name]", "definition": "[text]", "related_terms": ["[list]"] }
      ],
      "updated_terms": [
        { "term": "[name]", "previous": "[old]", "updated": "[new]" }
      ]
    },
    "requirement_candidates": [
      {
        "id": "REQ-001",
        "name": "[feature name]",
        "description": "[need description]",
        "acceptance_criteria": ["[list]"],
        "depends_on": ["[REQ-ids]"],
        "glossary_terms": ["[terms]"]
      }
    ],
    "architectural_decisions": [
      {
        "id": "ADR-001",
        "title": "[decision name]",
        "decision": "[what was decided]",
        "rationale": "[why]",
        "consequences": "[impacts]",
        "related_requirements": ["REQ-ids"]
      }
    ],
    "clarifications_provided": [
      {
        "requirement_id": "REQ-NNN",
        "clarification": "[what was clarified]",
        "glossary_updated": true,
        "ready_for_revalidation": true
      }
    ]
  }

send_to: requirements-writer-skill (or interview-requirements for feedback loops)

---

## Activities (from existing SKILL.md)

1. **Challenge Language**
   - Input: Terminology from grilling
   - Action: Question each term, propose precise definition
   - Output: Glossary entries

2. **Scenario Testing**
   - Input: Requirements being considered
   - Action: Invent edge cases, stress-test boundaries
   - Output: New/refined requirements

3. **Cross-Reference**
   - Input: New requirement candidates
   - Action: Check against existing requirements-set/ for conflicts
   - Output: Consolidated requirements, flagged conflicts

4. **Document Requirements**
   - Input: Agreed requirements
   - Action: Structure as REQ-NNN with acceptance criteria, dependencies
   - Output: requirements-set/REQ-NNN.md files

5. **Record ADRs**
   - Input: Major decisions from grilling
   - Action: Document decision, rationale, consequences
   - Output: docs/adr/NNNN-[name].md files

---
```

**Cambios Clave**:
- ✅ Define input_format exacto
- ✅ Define output_format exacto (JSON)
- ✅ Especifica qué archivos crea (GLOSSARY.md, REQ-*.md, ADR-*.md)
- ✅ Menciona feedback loops

---

## CAMBIO 4: requirements-writer-skill/SKILL.md

### Estado Actual
```yaml
---
name: requirements-writer-skill
description: Build and sharpen a project's requirements model...
disable-model-invocation: true
---

...
```

### Problema
- No especifica qué input espera
- No define estructura exacta de output
- No menciona qué hacer si score < 90

### Solución: Requirements-Writer Mejorado

```yaml
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

applyTo:
  - "requirement needs validation"
  - "user wants requirements scored"
  - invoked_by: "interview-requirements"

input_format: |
  Receives from /requirements-modeling:
  
  {
    "requirement_candidates": [
      {
        "id": "REQ-001",
        "name": "[name]",
        "description": "[text]",
        "acceptance_criteria": ["[list]"],
        "depends_on": ["[ids]"],
        "glossary_terms": ["[terms]"]
      }
    ],
    "glossary": {
      "file": "REQ/GLOSSARY.md",
      "terms": [
        { "term": "[name]", "definition": "[text]" }
      ]
    }
  }

output_format: |
  Produces:
  
  {
    "validated_requirements": [
      {
        "id": "REQ-001",
        "name": "[name]",
        "requirement_final": "[corrected requirement text]",
        "quality_score": 95,
        "score_rationale": "[why this score]",
        "characteristics": {
          "C1_necessary": { "status": "pass|fail", "rationale": "[text]" },
          "C2_appropriate": { "status": "pass|fail", "rationale": "[text]" },
          "C3_unambiguous": { "status": "pass|fail", "rationale": "[text]" },
          "C4_complete": { "status": "pass|fail", "rationale": "[text]" },
          "C5_singular": { "status": "pass|fail", "rationale": "[text]" },
          "C6_feasible": { "status": "pass|fail", "rationale": "[text]" }
        },
        "rules_violations": ["[rule ids violated]"],
        "corrections_made": ["[list]"],
        "verification_method": "inspection|analysis|demonstration|test",
        "verification_details": "[specific steps]",
        "related_glossary_terms": ["[terms]"],
        "related_requirements": ["[REQ-ids]"]
      }
    ],
    "clarification_requests": [
      {
        "requirement_id": "REQ-NNN",
        "issue": "[description]",
        "ambiguity": "[what's unclear]",
        "question_for_modeling": "[what needs clarifying]",
        "current_score": 65
      }
    ],
    "all_requirements_approved": true|false,
    "approval_rate": "X/Y requirements scored >= 90"
  }

send_to: interview-requirements (or back to requirements-modeling for clarifications)

uses_files:
  - characteristics.md
  - rules.md
  - patterns.md
  - review_algorithm.md
  - requirements-engineering.md
  - definitions.md
  - examples.md

---

## Validation Execution

For each requirement candidate:

1. Parse structure (entity, shall, verb, object, conditions)
2. Evaluate C1-C6 characteristics
3. Check R1-R41 rules
4. Apply patterns
5. Run review algorithm
6. Assign score (50/70/90/100)
7. Select verification method
8. If score >= 90: ✅ APPROVED
9. If score < 90: 
   - Identify specific ambiguities
   - Return clarification_request to interview-requirements
   - interview-requirements will call /requirements-modeling
   - Will call you again with updated glossary
   - You re-evaluate same requirement

10. Produce output in format above

---
```

**Cambios Clave**:
- ✅ Define input_format exacto
- ✅ Define output_format exacto
- ✅ Especifica clarification_requests (feedback loop)
- ✅ Define criterio de aprobación (>= 90)

---

## Resumen de Cambios

| SKILL.md | Cambio Principal | Impacto |
|----------|------------------|--------|
| **interview-requirements** | Agregar workflow orchestration (steps, passes, expect) | 🔴 CRÍTICO - Define todo el flujo |
| **grilling** | Agregar output_format JSON | 🟡 IMPORTANTE - Debe pasar datos al siguiente skill |
| **requirements-modeling** | Agregar input_format + output_format JSON | 🟡 IMPORTANTE - Debe recibir y enviar estructurado |
| **requirements-writer-skill** | Agregar input_format + output_format + clarification_requests | 🟡 IMPORTANTE - Feedback loops |

---

## Pasos de Implementación

### Paso 1: Actualizar interview-requirements/SKILL.md
- Copiar configuración de arriba
- Testear que reconoce parámetros

### Paso 2: Actualizar grilling/SKILL.md
- Agregar output_format
- Verificar que produce JSON
- Verificar que se puede capturar structured output

### Paso 3: Actualizar requirements-modeling/SKILL.md
- Agregar input_format + output_format
- Mantener actividades del SKILL.md actual
- Pero producir output en formato especificado

### Paso 4: Actualizar requirements-writer-skill/SKILL.md
- Agregar input_format + output_format
- Mantener lógica de validación actual
- Pero producir output en formato especificado
- Agregar clarification_requests

### Paso 5: Test End-to-End
```bash
/interview-requirements "Búsqueda Avanzada" stakeholders=["users", "marketing"] scope="Advanced search feature"
```

Verificar:
- ✅ interview-requirements invoca grilling
- ✅ grilling produce output estructurado
- ✅ interview-requirements captura y invoca requirements-modeling
- ✅ requirements-modeling produce output estructurado
- ✅ interview-requirements captura e invoca requirements-writer-skill
- ✅ requirements-writer-skill produce output estructurado
- ✅ Si score < 90, feedback loop funciona
- ✅ Deliverable final consolidado

---

## Nota Técnica: Captura de Output

Los skills necesitan poder **retornar datos estructurados** que el skill orquestador pueda capturar.

Opción A (Recomendada): JSON al final
```
[... execution ...]
=== STRUCTURED OUTPUT ===
{
  "grilling_output": { ... }
}
```

Opción B: Variables de sesión
```
Skills guardan output en variables
interview-requirements lee variables
```

Opción C: Archivos intermedios
```
Cada skill escribe archivo temporal
interview-requirements lee archivo
Limpia cuando termina
```

**Recomendación**: Opción A (JSON explícito) es más portable y debuggeable.

---

## Conclusión

Con estos cambios, el flujo será:

```
USER: /interview-requirements "Búsqueda Avanzada"
  ↓
interview-requirements orquesta automáticamente:
  → Invoca /grilling CON parámetros
  → Captura output JSON
  → Invoca /requirements-modeling CON grilling_output
  → Captura output JSON
  → Invoca /requirements-writer-skill CON requirement_candidates
  → Si score < 90: Feedback loop
  → Consolida deliverable final
  ↓
✅ Entrega: GLOSSARY.md, requirements-set/, docs/adr/
```

**AGENTS.md especifica QUÉ debe pasar. IMPLEMENTATION.md especifica CÓMO. Este documento (IMPLEMENTATION.md) es el puente.**
