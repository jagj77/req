# README.md - Documentación de Skills Integrados

## 🎯 Propósito

Este repositorio contiene cuatro skills integrados que orquestan un workflow end-to-end de **captura, análisis y documentación de requisitos** basado en la metodología **INCOSE Systems Engineering**.

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

## 🛠️ Los Cuatro Skills (AHORA INTEGRADOS)

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

### Para documentación de integración:

- [AGENTS.md](./AGENTS.md) - Especificación técnica de orquestación
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Guía de cambios en SKILL.md
- [ORCHESTRATION.md](./ORCHESTRATION.md) - Flujo conceptual
- [WORKFLOW.md](./WORKFLOW.md) - Guía rápida

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

## 🔑 Cambios Principales desde v1.0

### Versión v2.0 (Actual) - ORQUESTACIÓN FUNCIONAL

✅ **interview-requirements/SKILL.md**
- Ahora especifica invocación automática de otros skills
- Define fases 1-5
- Implementa feedback loops

✅ **grilling-requirements/SKILL.md**
- Especifica output estructurado
- Define protocolo de datos

✅ **requirements-modeling/SKILL.md**
- Especifica input/output format
- Lista actividades principales

✅ **requirements-writer-skill/SKILL.md**
- Añade frontmatter YAML
- Especifica input/output format
- Define feedback loops

✅ **IMPLEMENTATION.md** (NUEVO)
- Guía exacta de cambios implementados
- Valida que los SKILL.md cumplan AGENTS.md

---

## 📖 Más Información

- **WORKFLOW.md** - Guía rápida y cheat sheet
- **ORCHESTRATION.md** - Flujo detallado y escenario real
- **AGENTS.md** - Especificación técnica (QUÉ debe pasar)
- **IMPLEMENTATION.md** - Guía de implementación (CÓMO hacerlo)
- **README.md** - Este documento (índice)

---

**Versión**: 2.0 (Orquestación Funcional)  
**Basado en**: INCOSE Systems Engineering Handbook v4.0+  
**Estado**: ✅ COMPLETAMENTE EJECUTABLE  
**Últimas actualizaciones**: 2026-08-10
