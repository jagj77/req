# Orquestación de Skills - Workflow Integrado de Captura de Requisitos

## Visión General

Este documento describe cómo los cuatro skills en este repositorio se orquestan juntos para crear un flujo end-to-end de captura, análisis y documentación de requisitos basado en metodología INCOSE.

```
USER LAUNCHES INTERVIEW-REQUIREMENTS
    ↓
┌─────────────────────────────────────────────────┐
│  SKILL: interview-requirements                  │
│  ─────────────────────────────────────────────  │
│  • Orchestrates the workflow                    │
│  • Manages conversation flow                    │
│  • Coordinates other skills                     │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  SKILL: grilling-requirements                         │
│  ─────────────────────────────────────────────  │
│  • Asks relentless, one-at-a-time questions    │
│  • Stress-tests design decisions                │
│  • Walks design tree branches                   │
│  • Waits for user feedback on each question    │
│  • Resolves dependencies                        │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  SKILL: requirements-modeling                   │
│  ─────────────────────────────────────────────  │
│  • Challenges fuzzy language                    │
│  • Sharpens terminology                         │
│  • Challenges edge cases with scenarios         │
│  • Cross-references existing requirements       │
│  • Updates GLOSSARY.md in real-time             │
│  • Documents requirements in requirements-set/  │
│  • Records ADRs (Architectural Decision Records)│
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  SKILL: requirements-writer-skill               │
│  ─────────────────────────────────────────────  │
│  • Validates against characteristics (C1-C6)    │
│  • Evaluates against rules (R1-R41)             │
│  • Formats using patterns                       │
│  • Runs review algorithm                        │
│  • Produces quality-scored requirements         │
│  • Generates verification methods               │
│  • Corrections and refinement                   │
└─────────────────────────────────────────────────┘
    ↓
    OUTPUT: High-quality, verified, documented requirements
```

---

## Flujo Detallado por Fase

### FASE 1: Iniciación (interview-requirements)

**Responsabilidad**: Orquestar el workflow completo

**Acciones**:
1. Recibe el pedido del usuario de capturar/refinar requisitos
2. Inicializa contexto: proyecto, stakeholders, ámbito
3. Invoca `/grilling-requirements` para sesión de entrevista profunda
4. Coordina handoff a `requirements-modeling` cuando emerge contenido
5. Coordina validación final con `requirements-writer-skill`

**Entrada**: 
- Descripción del problema/proyecto
- Ámbito preliminar
- Stakeholders identificados

**Salida a siguiente fase**: 
- Notas de sesión de grilling-requirements
- Candidatos de requisitos emergentes
- Decisiones pendientes

---

### FASE 2: Elicitación Profunda (grilling-requirements)

**Responsabilidad**: Extraer conocimiento mediante cuestionamiento relentless

**Patrón de Preguntas**:
```
1. Start with broad question
   ↓
2. User responds
   ↓
3. ONE follow-up question based on response
   ↓
4. User responds
   ↓
5. Repeat until branch resolved
   ↓
6. Move to next design tree branch
```

**Principios**:
- ✋ UNA pregunta por turno (no bewildering)
- 🎯 Cada pregunta propone una respuesta recomendada
- 🔄 Espera feedback antes de continuar
- 🔍 Explora codebase si la pregunta es respondible así
- 🌳 Recorre sistemáticamente branches del design tree

**Salida**:
- Necesidades de stakeholders documentadas
- Decisiones de diseño articuladas
- Dependencias identificadas
- Áreas de conflicto o ambigüedad

**Trigger para siguiente fase**: Cuando emergen términos clave, decisiones, o requisitos candidatos

---

### FASE 3: Modelado de Requisitos (requirements-modeling)

**Responsabilidad**: Afinar el modelo de requisitos y capturar decisiones

**Actividades Simultáneas**:

#### A. Challenge Language
```
User says: "El sistema debe validar rápidamente"
Modeling says: "Tu glosario define 'validación' como validación de datos.
               ¿Quieres decir Data Validation o Business Logic Validation?
               Son diferentes requisitos."
```

#### B. Escenarios Edge-Case
```
Requirement: "El usuario puede crear reportes"
Modeling propone: "¿Qué pasa si el usuario no tiene permisos? 
                   ¿Qué pasa si la base de datos está caída?
                   ¿Qué pasa si crea un reporte de 1M de filas?"
```

#### C. Cross-Reference con Requisitos Existentes
```
IF existe requirements-001.md "User Authentication"
   AND nueva request menciona "Multi-Factor Authentication"
   THEN: "Esto amplía requirements-001 o es nuevo?"
```

#### D. Actualizar GLOSSARY.md en Tiempo Real
```
Cuando un término se resuelve:
  ✍️ Escribe inmediatamente en GLOSSARY.md
  ❌ NO retrasa (no batches)
  📋 Formato: Term, Definition, Context, Related terms
```

#### E. Documentar Requisitos Emergentes
```
requirements-set/
├── REQ-001-authentication.md
├── REQ-002-data-validation.md
└── REQ-003-reporting.md

Cada uno incluye:
  • Requirement ID + nombre
  • Descripción de necesidad
  • Acceptance criteria (checkboxes)
  • Dependencias
  • Glossary terms relacionados
```

#### F. Registrar Decisiones (ADR)
```
docs/adr/
├── 0001-authentication-strategy.md
│   - Decisión: Usar OAuth 2.0
│   - Context: Múltiples clientes externos
│   - Rationale: Mejor seguridad, estándar industria
│   - Consequences: Complejidad inicial, pero más flexible
│   
└── 0002-data-validation-approach.md
    - Decisión: Client-side + Server-side validation
    - Context: UX vs Security
    ...
```

**Archivo Generado**: 
- `GLOSSARY.md` - términos ordenados alfabéticamente
- `requirements-set/*.md` - requisitos por categoría
- `docs/adr/*.md` - decisiones arquitectónicas

**Pasar a siguiente fase**: Cuando requisitos están articulados y formalizados

---

### FASE 4: Escribir y Validar Requisitos (requirements-writer-skill)

**Responsabilidad**: Transformar requisitos candidatos en requisitos de calidad verificable

**Algoritmo Aplicado**:

```
Para cada requisito candidato:

1. IDENTIFY STRUCTURE
   └─ Entity, SHALL, Verb, Object, Conditions

2. EVALUATE CHARACTERISTICS (C1-C6)
   ├─ C1: Necessary? (esencial)
   ├─ C2: Appropriate? (nivel correcto)
   ├─ C3: Unambiguous? (una sola interpretación)
   ├─ C4: Complete? (qué, cuán bien, condiciones)
   ├─ C5: Singular? (una obligación)
   └─ C6: Feasible? (lograble con restricciones)

3. EVALUATE RULES (R1-R41 selected)
   ├─ R1: Complete sentence (Subject+Shall+Verb+Object)
   ├─ R2: Active voice
   ├─ R3: Correct entity
   ├─ R4: Defined terms (from GLOSSARY.md)
   ├─ R5-R14: Grammar, spelling, punctuation
   ├─ R7: No vague terms (fast, efficient, adequate)
   ├─ R8: No escape clauses (where possible, if practical)
   └─ R15: Logical conditions explicit

4. APPLY PATTERNS (from patterns.md)
   ├─ Functional:   The <Entity> shall <Action> <Object>
   ├─ Performance:  The <Entity> shall <Action> within <Value> <Unit>
   ├─ Event-driven: When <Event>, the <Entity> shall <Action>
   └─ State-driven: While <State>, the <Entity> shall <Action>

5. QUALITY SCORE
   ├─ 100: No violations
   ├─ 90: Minor style issues
   ├─ 70: Multiple rule violations
   └─ 50: Ambiguous or unverifiable

6. SELECT VERIFICATION METHOD
   ├─ Inspection (review)
   ├─ Analysis (mathematical proof)
   ├─ Demonstration (manual execution)
   └─ Test (automated, repeatable)

7. PRODUCE CORRECTED REQUIREMENT
   └─ Final, high-quality requirement ready for design
```

**Ejemplo de Transformación**:

```
ENTRADA (candidato):
"El sistema debe responder rápidamente a las búsquedas del usuario"

EVALUACIÓN:
❌ C1-C6: Vague (C3), not measurable (C4), not feasible to verify (C6)
❌ R7: "rápidamente" es vago
❌ R4: "sistema" no es término definido

SALIDA (corregido):
"The Search_System shall display Search_Results within 2 seconds 
 of User initiating Query, measured from Query submission to 
 Results display on User screen."

✅ Scoring: 95/100
✅ Verification: Test (automated response time measurement)
```

**Archivo de Salida**:
```
requirements-set/REQ-001-search.md

# REQ-001: Search Response Time

**Requirement**: The Search_System shall display Search_Results 
                within 2 seconds of User initiating Query...

**Verification Method**: Test
  - Automated performance test
  - Measure from submission to display
  - 95th percentile < 2 seconds

**Quality Score**: 95/100

**Violations Corrected**: 
  - Replaced "rápidamente" with "2 seconds"
  - Defined entity as "Search_System"
  - Specified measurement point

**Related Glossary Terms**: Search_System, Search_Results, User, Query
```

---

## Comunicación Entre Skills

### Interview-Requirements → Grilling-requirements
```
\"Realicemos una sesión de grilling-requirements sobre los requisitos de búsqueda.
 Stakeholders: usuários finales, equipo de marketing.
 Ámbito: feature de search del portal."

GRILLING-REQUIREMENTS: Comienza con preguntas sobre necesidades, casos de uso, 
         volumetría, performance expectations, etc.
```

### Grilling-requirements → Requirements-Modeling
```
Durante grilling-requirements, emergen términos como:
- "Search_Query" (qué es?)
- "Query Performance" (cómo se mide?)
- "Relevancia" (qué tan relevante es "relevante"?)

REQUIREMENTS-MODELING: Formaliza estos en GLOSSARY.md
```

### Requirements-Modeling → Requirements-Writer-Skill
```
Requirements-Modeling propone:

"REQ-001: Search Performance
 Description: Las búsquedas deben completarse en menos de 2 segundos"

REQUIREMENTS-WRITER-SKILL: Valida, refina, produce versión final
```

### Requirements-Writer-Skill → Requirements-Modeling
```
Si el refinamiento identifica términos nuevos o ambigüedades,
requiere feedback de requirements-modeling.

"Necesito que definas 'Search_Result' precisamente.
 ¿Incluye solo título + descripción, o también metadata?"

REQUIREMENTS-MODELING: Actualiza glosario, proporciona definición
```

---

## Arquitectura de Archivos Generados

```
PROJECT/
├── .agents/
│   └── skills/
│       ├── interview-requirements/
│       ├── grilling-requirements/
│       ├── requirements-modeling/
│       └── requirements-writer-skill/
│
├── REQ/
│   ├── GLOSSARY.md
│   │   ├── ## Search_System
│   │   │   - Definition: [precise definition]
│   │   │   - Context: [where/how used]
│   │   │   - Related terms: [links]
│   │   ├── ## Query
│   │   └── ## Search_Results
│   │
│   ├── requirements-set/
│   │   ├── REQ-001-search.md
│   │   ├── REQ-002-performance.md
│   │   ├── REQ-003-security.md
│   │   └── requirements-summary.md
│   │
│   └── docs/
│       └── adr/
│           ├── 0001-search-algorithm-choice.md
│           │   - Decision: Use Elasticsearch
│           │   - Rationale: Scalability, FTS capabilities
│           │   - Consequences: Additional infrastructure
│           │
│           ├── 0002-query-timeout-strategy.md
│           └── 0003-security-model.md
│
└── src/
    ├── search/
    │   ├── GLOSSARY.md (if multi-context)
    │   ├── requirements-set/
    │   └── docs/adr/
    └── [other modules]
```

---

## Flujo Completo - Ejemplo Real

### Escenario: Capturar requisitos para Feature "Búsqueda Avanzada"

```
┌─────────────────────────────────────────────────────┐
│ USER                                                │
│ "Necesito capturar requisitos para búsqueda        │
│  avanzada. Tengo 3 stakeholders."                  │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ INTERVIEW-REQUIREMENTS Skill                       │
│ • Recibe input                                      │
│ • Setup: 3 stakeholders, feature scope             │
│ • Invoca /grilling                                 │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ GRILLING (Sesión 1)                                │
│ Q1: "¿Cuál es el mayor problema que resuelve      │
│     la búsqueda avanzada?"                         │
│ USER: "Usuarios no encuentran documentos antiguos" │
│                                                     │
│ Q2: "¿Cuántos documentos en promedio tienen       │
│     estos usuarios que buscar?"                    │
│ USER: "Entre 100k y 1M"                            │
│                                                     │
│ Q3: "¿Cuál es el tiempo máximo aceptable para     │
│     una búsqueda?"                                 │
│ USER: "Menos de 3 segundos"                        │
│                                                     │
│ ... (continúa) ...                                 │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ REQUIREMENTS-MODELING (Sesión 1)                   │
│                                                     │
│ Emergen términos: Search Query, Document,          │
│ Relevance Score                                    │
│                                                     │
│ Challenge: "¿Qué es 'Relevance'? ¿Proximidad     │
│            de palabras? ¿Frecuencia? ¿Ambos?"    │
│ USER: "Ambos, con pesos"                          │
│                                                     │
│ ✍️ GLOSSARY.md se actualiza:                       │
│    ## Relevance_Score                              │
│    Definition: Weighted measure combining word     │
│    proximity (40%) and frequency (60%)...          │
│                                                     │
│ Scenario testing:                                  │
│ "¿Qué pasa si document_count > 1M?               │
│  ¿Sigue siendo < 3 segundos?"                     │
│ USER: "Debería seguir siendo < 3 seg, pero si    │
│        no es posible, al menos < 10 seg"          │
│                                                     │
│ ✍️ ADR-001: "Elasticsearch for scalability"        │
│ ✍️ ADR-002: "2-tier timeout: 3s preferred, 10s max"│
│                                                     │
│ ✍️ requirements-set/REQ-001-search-speed.md        │
│    Candidato: "The Search_System shall return      │
│    Search_Results within 3 seconds for document   │
│    counts up to 1M..."                             │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ REQUIREMENTS-WRITER-SKILL (Review Phase)           │
│                                                     │
│ Input Candidato:                                   │
│ "The Search_System shall return Search_Results    │
│  within 3 seconds for document counts up to 1M    │
│  when searching indexed documents"                 │
│                                                     │
│ Evaluation:                                        │
│ ✅ C1-C6: Necessary, Appropriate, Unambiguous,    │
│    Complete, Singular, Feasible                   │
│ ✅ R1-R15: Proper structure, defined terms,       │
│    measurable, no vague words                      │
│ ✅ Follows Performance Pattern                     │
│                                                     │
│ Score: 95/100                                      │
│ Verification: Automated performance test           │
│              (95th percentile < 3 seconds)         │
│                                                     │
│ ✍️ REQ-001-search-speed.md (final version)        │
│                                                     │
│ Issues identified:                                 │
│ "Document counts' unit not precise.               │
│  How are counts measured? Indexed vs total?"      │
│ BACK to REQUIREMENTS-MODELING                     │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ REQUIREMENTS-MODELING (Refinement)                 │
│                                                     │
│ Clarify: "By document count, you mean indexed     │
│         documents in the searchable index, not    │
│         total documents in system?"                │
│ USER: "Yes, indexed documents"                     │
│                                                     │
│ ✍️ GLOSSARY.md updated:                            │
│    ## Indexed_Document_Count                       │
│    Definition: Count of documents currently       │
│    in the active search index...                   │
│                                                     │
│ BACK to REQUIREMENTS-WRITER-SKILL                 │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ REQUIREMENTS-WRITER-SKILL (Final)                  │
│                                                     │
│ Final Requirement:                                 │
│ "The Search_System shall return Search_Results    │
│  within 3 seconds for Indexed_Document_Count up   │
│  to 1,000,000 when queried by User."              │
│                                                     │
│ ✅ Score: 98/100                                   │
│ ✅ Verification: Automated test                    │
│ ✅ Ready for design & development                  │
│                                                     │
│ ✍️ Final file: REQ-001-search-speed.md            │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ INTERVIEW-REQUIREMENTS (Orchestration)             │
│                                                     │
│ Compila outputs:                                   │
│ ✅ REQ-001, REQ-002, REQ-003 (finales)            │
│ ✅ GLOSSARY.md completo                           │
│ ✅ 5 ADRs documentados                            │
│ ✅ Todas las dependencias resueltas                │
│ ✅ Todos los requisitos verificables               │
│                                                     │
│ Produce: requirements-set/requirements-summary.md │
└─────────────────────────────────────────────────────┘
                    ↓
            ✅ DELIVERABLE
    High-quality requirements ready for design
```

---

## Criterios de Completitud

Para que el workflow sea "completo":

✅ **Grilling Phase**:
- [ ] Todas las branches del design tree exploradas
- [ ] Dependencias entre decisiones resueltas
- [ ] Stakeholder needs articuladas
- [ ] Casos de uso documentados

✅ **Requirements-Modeling Phase**:
- [ ] GLOSSARY.md contiene todos los términos clave
- [ ] Requisitos candidatos documentados en requirements-set/
- [ ] ADRs creados para decisiones clave
- [ ] Escenarios edge-case explorados
- [ ] No hay contradicciones entre requisitos

✅ **Requirements-Writer-Skill Phase**:
- [ ] Todos los requisitos scored ≥ 90/100
- [ ] Verificación method definida para cada uno
- [ ] Cero violaciones de características C1-C6
- [ ] Cero violaciones de reglas R1-R15
- [ ] Términos usados están en GLOSSARY.md

✅ **Output Final**:
- [ ] requirements-set/ contiene requisitos finales validados
- [ ] GLOSSARY.md es la fuente única de términos
- [ ] ADRs documentan decisiones arquitectónicas
- [ ] Trazabilidad desde needs → requirements → verification
- [ ] requirements-summary.md integra todo

---

## Puntos de Integración Críticos

### 1. GLOSSARY.md es el Hub
- **Grilling-requirements** identifica términos
- **Requirements-Modeling** los formaliza
- **Requirements-Writer** los valida y usa
- **TODOS** consultan antes de introducir nuevos términos

### 2. Feedback Loops
```
Requirements-Writer → "Necesito clarificar 'Performance'"
    ↓
Requirements-Modeling → Actualiza GLOSSARY.md
    ↓
Requirements-Writer → Re-evalúa con definición clara
    ↓
Requisito refinado → Score mejora 90 → 95
```

### 3. Versionamiento
- Cada skill mantiene su propia "versión" durante sesión
- Al finalizar, `interview-requirements` produce versión final consolidada
- Cambios posteriores generan nuevo ADR registrando rationale

---

## Cómo Iniciar el Flujo

### Usuario invoca:
```bash
/interview-requirements

Parámetro: Descripción del proyecto/feature
```

### Interview-Requirements inicia:
```bash
/grilling

Con contexto:
- Proyecto: [name]
- Stakeholders: [list]
- Scope: [description]
```

---

## Próximos Pasos Recomendados

1. **Crear archivo AGENTS.md** que defina cómo los skills se invocan mutuamente
2. **Crear ejemplos** end-to-end documentados en `examples/`
3. **Definir interfaz** entre skills (inputs/outputs esperados)
4. **Crear templates** para requirements-set/ y ADR/
5. **Documentar guardrails** - cuándo cada skill debe say "no" o request clarification
