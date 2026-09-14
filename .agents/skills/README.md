# README.md - Documentación de Skills Integrados

## 🎯 Propósito

Este repositorio contiene **cinco skills**: cuatro orquestan un workflow end-to-end de **captura, análisis y documentación de requisitos** (basado en INCOSE), y un quinto complementario para refactor seguro de código legacy sin cobertura.

El usuario inicia con `/interview-requirements` y el agente orquesta automáticamente:
1. `/grilling-requirements` - Extrae necesidades (preguntas 1x1)
2. `/requirements-modeling` - Formaliza (GLOSSARY + REQ candidatos + ADRs)
3. `/requirements-writer-skill` - Valida (Characteristics + Rules + Score)
4. Feedback loops automáticos si algún requisito scores < 90/100

**Resultado**: 
- ✅ **GLOSSARY.md** (root) - Términos formalizados, compartidos por todos los proyectos
- ✅ **{project_slug}/requirements-set/** - Requisitos validados, scored ≥90
- ✅ **Trazabilidad completa** - needs → requirements → verification

---

## 📚 Estructura de Documentación

### NIVEL 1: Inicio Rápido

**[WORKFLOW.md](./WORKFLOW.md)** (👈 **COMIENZA AQUÍ**)
- Guía de 30 segundos
- Paso a paso visual
- Comandos rápidos
- Criterios de completitud

### NIVEL 2: Flujo y Conceptos

**[ORCHESTRATION.md](./ORCHESTRATION.md)**
- Flujo conceptual completo
- Ejemplo real end-to-end: Búsqueda Avanzada
- Responsabilidades de cada skill
- Arquitectura de archivos generados
- Puntos de integración críticos

### NIVEL 3: Implementación Técnica

**[AGENTS.md](./AGENTS.md)** ← Especificación técnica (QUÉ debe pasar)
- Configuración YAML de cada skill
- Handoff protocols entre skills
- Feedback loop protocols
- Algoritmos detallados

**[IMPLEMENTATION.md](./IMPLEMENTATION.md)** ← Guía de implementación (CÓMO hacerlo)
- Cambios exactos necesarios en cada SKILL.md
- Ejemplos de YAML mejorado
- Protocolos de entrada/salida
- Validación end-to-end

### NIVEL 4: Metodología Base

**[requirements-writer-skill/requirements-engineering.md](./requirements-writer-skill/requirements-engineering.md)**
- 7 Principios INCOSE
- Lifecycle phases
- Conexión con otros archivos

---

## 🛠️ Los Cinco Skills

### 1. interview-requirements ⭐ ORQUESTADOR
**Estado**: ✅ Actualizado para orquestar automáticamente

```
Invoca automáticamente:
1. /grilling-requirements → Captura needs, decisions, ambiguities
2. /requirements-modeling → Formaliza GLOSSARY + REQ candidatos
3. /requirements-writer-skill → Valida y score
4. Loops feedback si score < 90
5. Consolida deliverable final
```

📍 Archivo: [interview-requirements/SKILL.md](./interview-requirements/SKILL.md)

### 2. grilling-requirements
**Estado**: ✅ Actualizado para output estructurado

```
Extrae mediante cuestionamiento:
- articulated_needs
- design_decisions
- identified_ambiguities
- terminology_introduced
- dependencies_identified
```

📍 Archivo: [grilling-requirements/SKILL.md](./grilling-requirements/SKILL.md)

### 3. requirements-modeling
**Estado**: ✅ Actualizado para input/output estructurado

```
Formaliza y estructura:
- Desafía lenguaje vago
- Crea escenarios edge-case
- Actualiza GLOSSARY.md en tiempo real
- Documenta REQ-NNN candidatos
- Registra ADRs
- Retorna datos estructurados para interview-requirements
```

📍 Archivo: [requirements-modeling/SKILL.md](./requirements-modeling/SKILL.md)

### 4. requirements-writer-skill
**Estado**: ✅ Actualizado para validación + feedback loops

```
Valida y refina:
- Evalúa C1-C6 (características)
- Verifica R1-R41 (reglas)
- Aplica patterns
- Corre review algorithm
- Asigna quality score (50-100)
- Selecciona verification method
- Si score < 90: retorna clarification_request
```

📍 Archivo: [requirements-writer-skill/SKILL.md](./requirements-writer-skill/SKILL.md)
### 5. seams-test 🧰 COMPLEMENTARIO
**Estado**: ✅ Disponible desde v3.0

**No participa del orquestador de requisitos** — se invoca manualmente
cuando hay que tocar código sin cobertura. Tech-stack agnostic
(Laravel, .NET, Java, Python, Node, COBOL, etc.).

```
Cubre (basado en Michael Feathers, "Working Effectively with Legacy Code"):
- Árbol de decisión universal para encontrar seams
- Sprout Method/Class y Wrap Method/Class
- Scratch Refactoring descartable (rama temporal)
- Approval Testing (Snapshotting / Golden Master)
- Characterization tests con aislamiento transaccional
- Mutation Testing manual como criterio de confianza
- Pinch points: cubrir el punto de convergencia, no 20 deps

Triggers:
- "legacy code" / "brownfield" / "no tests for this"
- "before I refactor" / "safety net" / "seams"
- "characterization tests" / "golden master"
- Cualquier refactor / extracción sobre código sin cobertura
```

📍 Archivo: [seams-test/SKILL.md](./seams-test/SKILL.md)

---

## 🔄 Flujo de Ejecución (AUTOMÁTICO)


```
USER invoca: /interview-requirements "Búsqueda Avanzada"
    ↓
[interview-requirements ORQUESTA automáticamente]
    ↓
┌─────────────────────────────┐
│  /grilling-requirements     │  ← Extrae necesidades
│  one-at-a-time questions   │     Retorna: structured output
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  /requirements-modeling     │  ← Recibe grilling-requirements output
│  Challenge language         │     Formaliza terminología
│  Create scenarios           │     Retorna: GLOSSARY + REQ candidatos
│  Update GLOSSARY.md         │
│  Document requirements      │
│  Record ADRs                │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  /requirements-writer-skill │  ← Recibe REQ candidatos
│  Evaluate C1-C6             │     Valida cada requisito
│  Check R1-R41               │     Score: 50/70/90/100
│  Apply patterns             │
│  Run algorithm              │     Si score < 90:
│  Assign score               │     ↓ retorna clarification_request
└─────────────────────────────┘
    ↓
[FEEDBACK LOOP - si score < 90]
    ↓
┌─────────────────────────────┐
│  /requirements-modeling     │  ← Recibe clarification_request
│  (Loop)                     │     Actualiza GLOSSARY.md
│                             │     Retorna: clarifications
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  /requirements-writer-skill │  ← Re-evalúa con GLOSSARY actualizado
│  (Loop)                     │     Nuevo score: ≥90 → APROBADO
└─────────────────────────────┘
    ↓
[interview-requirements CONSOLIDA]
    ↓
✅ OUTPUT DELIVERABLE
   ├── GLOSSARY.md (root-level, centralized - shared by all projects)
   ├── {project_slug}/
   │   ├── requirements-set/ (todos REQ scored ≥90)
   │   └── requirements-summary.md (resumen ejecutivo)
   └── {another_project_slug}/
       └── requirements-set/
```

---

## 📋 Archivos Generados por el Workflow

### GLOSSARY.md (root-level, centralized)
```markdown
## Search_System
Definition: System component responsible for...
Context: Used in [requirements]
Related terms: Search_Query, Search_Results

## Search_Results
Definition: Data structure containing...

## Payment_Gateway
Definition: External service for payment processing...
```
*Same GLOSSARY.md is referenced by all projects*

### busqueda-avanzada/requirements-set/REQ-001-search.md
```markdown
# REQ-001: Search Performance

**Requirement**: The Search_System shall return 
Search_Results within 3 seconds...

**Quality Score**: 95/100 ✅

**Verification Method**: Test
```

### payment-integration/requirements-set/REQ-001-payment.md
```markdown
# REQ-001: Payment Processing

**Requirement**: The Payment_Gateway shall process
transactions within 5 seconds...

**Quality Score**: 92/100 ✅
```

---

## ✅ Criterios de Completitud

### Fase: Grilling ✅
- [ ] Design tree branches explorados
- [ ] Stakeholder needs articuladas
- [ ] Decisiones documentadas
- [ ] Dependencias identificadas

### Fase: Requirements-Modeling ✅
- [ ] GLOSSARY.md contiene todos los términos
- [ ] requirements-set/ tiene requisitos candidatos
- [ ] Sin contradicciones entre requisitos

### Fase: Requirements-Writer ✅
- [ ] Todos los requisitos scored ≥ 90/100
- [ ] Métodos de verificación definidos
- [ ] Cero violaciones C1-C6
- [ ] Cero violaciones R1-R15

### Deliverable Final ✅
- [ ] requirements-summary.md existe
- [ ] Trazabilidad completa
- [ ] Stakeholders satisfied
- [ ] Listo para diseño

---

## 🎓 Metodología: INCOSE Systems Engineering

Este workflow implementa:

✅ **Systematic Process** (INCOSE SE Handbook v4.0+)
- Structured lifecycle phases
- Formal traceability
- Quality gates

✅ **Stakeholder-Centric** (Principle P1)
- Diverse perspectives captured
- Needs → Requirements mapping

✅ **Quality-Driven** (Principle P3)
- Characteristics C1-C6
- Rules R1-R41
- Quality scoring (minimum 90/100)

✅ **Formal Specification** (Principle P4)
- SHALL-based requirements
- Defined terminology
- Structured patterns

✅ **Complete Traceability** (Principle P5)
- Needs → Requirements → Verification
- Impact analysis enabled

✅ **Configuration Management** (Principle P6)
- Baseline requirements
- Formal change control
- Version control

✅ **Feedback Loops** (Principle P7)
- Automatic re-validation if score < 90
- Iterative refinement
- Continuous validation

Ver [requirements-writer-skill/requirements-engineering.md](./requirements-writer-skill/requirements-engineering.md) para detalle.

---

## 🚀 Cómo Empezar

### Paso 1: Lee WORKFLOW.md
**Tiempo**: 5 minutos
- Comprende el flujo de 30 segundos
- Ve el paso a paso
- Conoce los criterios de completitud

### Paso 2: Lee ORCHESTRATION.md
**Tiempo**: 15 minutos
- Entiende el flujo conceptual
- Ve ejemplo real completo
- Aprende arquitectura de archivos

### Paso 3: Ejecuta /interview-requirements
**Tiempo**: 2-4 horas (según complejidad)
- El agente orquesta automáticamente
- Sigue los 5 pasos automáticamente
- Obten tus requisitos

**Ejemplo**:
```bash
/interview-requirements "Búsqueda Avanzada" stakeholders="users,marketing,product" scope="Advanced search feature"
```

### Paso 4: Revisa AGENTS.md + IMPLEMENTATION.md si necesitas detalles técnicos
**Tiempo**: 15 minutos
- Especificación técnica (AGENTS.md)
- Guía de implementación (IMPLEMENTATION.md)
- Cómo actualizar SKILL.md si es necesario

---

## 📞 Soporte y Referencia

### Para cada skill, consulta:

| Skill | SKILL.md | Detalles | Entrada |
|-------|----------|---------|---------|
| interview-requirements | [✓](./interview-requirements/SKILL.md) | Orquestación | Descripción proyecto |
| grilling-requirements | [✓](./grilling-requirements/SKILL.md) | Preguntas 1x1 | Contexto |
| requirements-modeling | [✓](./requirements-modeling/SKILL.md) | Formalización | Grilling output |
| requirements-writer-skill | [✓](./requirements-writer-skill/SKILL.md) | Validación | REQ candidatos |
| seams-test | [✓](./seams-test/SKILL.md) | Refactor seguro | Código sin cobertura |

### Para documentación de integración:

- [AGENTS.md](./AGENTS.md) - Especificación técnica de orquestación
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Guía de cambios en SKILL.md
- [ORCHESTRATION.md](./ORCHESTRATION.md) - Flujo conceptual
- [WORKFLOW.md](./WORKFLOW.md) - Guía rápida
- [seams-test/SKILL.md](./seams-test/SKILL.md) - Teoría de seams + characterization testing

### Para metodología INCOSE:

- [requirements-engineering.md](./requirements-writer-skill/requirements-engineering.md) - Principios base
- [characteristics.md](./requirements-writer-skill/characteristics.md) - Criterios C1-C6
- [rules.md](./requirements-writer-skill/rules.md) - Reglas R1-R41
- [definitions.md](./requirements-writer-skill/definitions.md) - Terminología
- [review_algorithm.md](./requirements-writer-skill/review_algorithm.md) - Algoritmo de validación

### Para patrones y ejemplos:

- [patterns.md](./requirements-writer-skill/patterns.md) - Estructuras de requisitos
- [examples.md](./requirements-writer-skill/examples.md) - Ejemplos buenos/malos

---

## 🎯 Resultado Final Garantizado

Después de completar el workflow automático, tendrás:

```
PROJECT/REQ/
├── GLOSSARY.md
│   └── Todos los términos formalizados y coherentes
│
├── requirements-set/
│   ├── REQ-001-[feature].md (scored ≥90, verificable)
│   ├── REQ-002-[feature].md (scored ≥90, verificable)
│   ├── REQ-003-[feature].md (scored ≥90, verificable)
│   └── requirements-summary.md (resumen ejecutivo)
│
└── docs/adr/
    ├── 0001-[decision].md (decisión + rationale)
    ├── 0002-[decision].md (decisión + rationale)
    └── [...]
```

**Calidad garantizada:**
- ✅ Todos los requisitos scored ≥ 90/100
- ✅ Métodos de verificación definidos para cada uno
- ✅ Trazabilidad completa (needs → requirements → verification)
- ✅ Ninguna ambigüedad o contradicción
- ✅ Terminology consistente (GLOSSARY.md único)
- ✅ Listo para diseño y desarrollo

---

## 🔑 Cambios Principales

### Versión v3.0 (Actual) — Scope Guards + Reframing + seams-test

Refuerza el contrato "skill de requirements = artefactos en `/req/`
solo" y agrega el skill complementario `seams-test` para refactor
seguro.

#### Alcance del cambio

✅ **`interview-requirements/SKILL.md`** — reescritura mayor:
- Frontmatter con `applyTo` ampliado: dispara también ante pedidos de
  implementación (`"asigná permisos"`, `"add middleware"`, `"creá endpoint"`).
- Patterns regex multi-idioma que detectan verbos imperativos + tech-entity
  y los re-enmarcan como requisitos sin ejecutarlos.
- Bloque nuevo **"Hard Rules (Non-Negotiable)"**: tabla de outputs
  permitidos, forbidden actions por tech-stack, tabla de **Trigger
  detection** con 9 patrones de re-framing (Laravel/Django/Express/etc.),
  self-check con `git status` antes de cada fase.
- **Failure recovery**: si accidentalmente empezó a tocar código, revertir
  con `git checkout -- <file>` y reanudar STEP 0.

✅ **`grilling-requirements/SKILL.md`** — bloque **Scope guard** añadido al
final (heredado). Define: ✅ read-only tools (`grep`, `codegraph`,
`read`, `webfetch`, `glob`) y ❌ explícitos (no `edit`/`write` a nada
fuera de `/req/`, no install/build/commit, no modificar skills).

✅ **`requirements-modeling/SKILL.md`** — `scope_guard` heredado +
explicitado como tech-stack agnostic; añade `docs/adr/NNNN-*.md` como
path permitido (ADRs nuevos); regla `lazy_creation` (crear archivos solo
cuando hay contenido).

✅ **`requirements-writer-skill/SKILL.md`** — frontmatter
`name`/`description`, paths explícitos de read (incluye su propio home
read-only), write ampliado a `requirements-summary.md`. `scope_guard`
con regla crítica: **no modifica `/req/GLOSSARY.md`** — devuelve
`clarification_request` al orchestrator para preservar
**single-writer ownership** del glossary. Añade `self_check` con
`git status`.

✅ **`seams-test/SKILL.md`** (NUEVO, 9.2 KB) — skill complementario,
tech-stack agnostic (Laravel, .NET, Java, Python, Node, COBOL).
Cubre el trabajo de Michael Feathers: árbol de decisión universal
para encontrar seams, Sprout/Wrap, Scratch Refactoring descartable,
Approval Testing (Snapshotting), Mutation Testing manual, pinch
points. Triggers: "legacy code", "brownfield", "no tests for this",
"before I refactor", "safety net", "seams", "characterization tests",
"golden master". **No participa del orquestador de requisitos** — se
invoca manualmente cuando hay que tocar código sin cobertura.

#### Contrato unificado (los 4 skills comparten)

```
ALLOWED file outputs:
  /req/GLOSSARY.md (root, compartido)
  /req/{slug}/requirements-set/REQ-NNN.md
  /req/{slug}/requirements-set/requirements-summary.md
  /req/{slug}/docs/adr/NNNN-*.md (ADRs nuevos solamente)
  .req-config.yml (config a nivel repo)

FORBIDDEN actions (cualquier stack):
  - Tocar código fuente, config, build manifests, schemas,
    migrations, tests, IaC, CI en cualquier tech stack.
  - Correr install / build / migrate / deploy / lint / format.
  - git commit / push / abrir PR.
  - Tratar un pedido de implementación como ticket y ejecutarlo.
  - Modificar docs/, README*, CONTEXT* existentes.

Self-check antes de cada transición de fase:
  git status --short -- ':!req' ':!.req-config.yml' ':!.agents/skills'
  Cualquier leak → revertir con git checkout -- <path> y advertir.
```

#### Reframing universal (tech-stack agnostic)

| Pedido literal (ejemplos) | Re-encuadre como requisito |
|---|---|
| "Asigná X permiso a Y rol" | "The system SHALL allow [actor] to [action] on [resource] within [scope]." |
| "Add this middleware/guard" | "The system SHALL restrict access to [endpoint] to users with [roles/conditions]." |
| "Add a column to table T" | "The system SHALL persist [field] per [entity]." |
| "Add a field to form F" | "The system SHALL capture [field] during [process]." |
| "API returns JSON not XML" | "The system SHALL respond to [endpoint] with Content-Type [type]." |
| "Two-step approval flow" | "The system SHALL require approval from [N] [role] before [action]." |
| "Expose POST /foo" | "The system SHALL expose POST /foo with the documented request/response contract." |
| "Filter listing by user's org" | "The system SHALL scope [listing] to records belonging to the user's [org/unit]." |
| "Send email when X happens" | "The system SHALL notify [recipient] via [channel] when [event] occurs." |

### Versión v2.0 — ORQUESTACIÓN FUNCIONAL

✅ **interview-requirements/SKILL.md**

✅ **grilling-requirements/SKILL.md**

✅ **requirements-modeling/SKILL.md**

✅ **requirements-writer-skill/SKILL.md**

✅ **IMPLEMENTATION.md** (NUEVO)


## 📖 Más Información



**Versión**: 3.0 (Scope Guards + Reframing + seams-test)
**Basado en**: INCOSE Systems Engineering Handbook v4.0+
**Estado**: ✅ COMPLETAMENTE EJECUTABLE
**Últimas actualizaciones**: 2026-09-14
