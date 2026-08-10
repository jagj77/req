# README.md - Documentación de Skills Integrados

## 🎯 Propósito

Este repositorio contiene cuatro skills integrados que orquestan un workflow end-to-end de **captura, análisis y documentación de requisitos** basado en la metodología **INCOSE Systems Engineering**.

El usuario inicia con `/interview-requirements` y obtiene:
- ✅ **GLOSSARY.md** - Términos formalizados
- ✅ **requirements-set/** - Requisitos validados, scored
- ✅ **docs/adr/** - Decisiones arquitectónicas documentadas
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

**[AGENTS.md](./AGENTS.md)**
- Configuración YAML de cada skill
- Handoff protocols entre skills
- Feedback loop protocols
- Algoritmos detallados (grilling, modeling, validation)
- Tabla de integración

### NIVEL 4: Metodología Base

**[requirements-writer-skill/requirements-engineering.md](./requirements-writer-skill/requirements-engineering.md)**
- 7 Principios INCOSE
- Lifecycle phases
- Conexión con otros archivos

---

## 🛠️ Los Cuatro Skills

### 1. interview-requirements
**Orquestador Principal**
- Inicia el flujo completo
- Coordina entre otros skills
- Produce deliverable final consolidado

📍 Archivo: [interview-requirements/SKILL.md](./interview-requirements/SKILL.md)

### 2. grilling
**Extracción de Requisitos**
- Entrevista profunda
- Una pregunta por turno
- Camina design tree branches
- Output: needs articuladas, decisiones, ambigüedades

📍 Archivo: [grilling/SKILL.md](./grilling/SKILL.md)

### 3. requirements-modeling
**Formalización del Modelo**
- Afina terminología
- Crea escenarios edge-case
- Actualiza GLOSSARY.md en tiempo real
- Documenta requisitos en requirements-set/
- Registra ADRs

📍 Archivo: [requirements-modeling/SKILL.md](./requirements-modeling/SKILL.md)

### 4. requirements-writer-skill
**Validación y Refinamiento**
- Evalúa C1-C6 (características)
- Verifica R1-R41 (reglas)
- Aplica patterns
- Corre review algorithm
- Asigna quality score (50-100)
- Selecciona verification method

📍 Archivos:
- [SKILL.md](./requirements-writer-skill/SKILL.md) - Descripción
- [characteristics.md](./requirements-writer-skill/characteristics.md) - C1-C6
- [rules.md](./requirements-writer-skill/rules.md) - R1-R41
- [patterns.md](./requirements-writer-skill/patterns.md) - Patrones
- [review_algorithm.md](./requirements-writer-skill/review_algorithm.md) - Algoritmo
- [examples.md](./requirements-writer-skill/examples.md) - Ejemplos

---

## 🔄 Flujo de Ejecución

```
USER invoca: /interview-requirements [proyecto]
    ↓
[ORCHESTRATION PHASE]
    ↓
┌─────────────────────────────┐
│  /grilling                  │  ← Extrae necesidades
│  one-at-a-time questions   │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  /requirements-modeling     │  ← Formaliza terminología
│  Challenge language         │     Documenta decisiones
│  Create scenarios           │
│  Update GLOSSARY.md         │
│  Document requirements      │
│  Record ADRs                │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  /requirements-writer-skill │  ← Valida requisitos
│  Evaluate C1-C6             │     Asigna score
│  Check R1-R41               │     Selecciona verificación
│  Apply patterns             │
│  Run algorithm              │
└─────────────────────────────┘
    ↓
[FEEDBACK LOOPS as needed]
    ↓
✅ OUTPUT DELIVERABLE
   ├── GLOSSARY.md
   ├── requirements-set/
   └── docs/adr/
```

---

## 📋 Archivos Generados por el Workflow

### GLOSSARY.md
```
## Search_System
Definition: System component responsible for...
Context: Used in [requirements]
Related terms: Search_Query, Search_Results

## Search_Results
Definition: Data structure containing...
Units: array of results
Related terms: Search_System, Relevance_Score
```

### requirements-set/REQ-001-search.md
```
# REQ-001: Search Performance

**Requirement**: The Search_System shall return 
Search_Results within 3 seconds...

**Quality Score**: 95/100

**Verification Method**: Test

**Related Glossary Terms**: [list]
```

### docs/adr/0001-search-algorithm.md
```
# ADR-0001: Elasticsearch Selection

## Decision
Use Elasticsearch for search indexing

## Rationale
- Scalability to 1M documents
- Full-text search capabilities
- Performance requirements

## Consequences
- Additional infrastructure required
- Operational complexity
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
- [ ] ADRs documentan decisiones
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
- Quality scoring

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
- Sigue el workflow
- Obten tus requisitos

### Paso 4: Revisa AGENTS.md si necesitas detalles técnicos
**Tiempo**: 10 minutos
- Configuración YAML
- Handoff protocols
- Feedback loops

---

## 📞 Soporte y Referencia

### Para cada skill, consulta:

| Skill | SKILL.md | Detalles | Requisito de Entrada |
|-------|----------|---------|------------------|
| interview-requirements | [✓](./interview-requirements/SKILL.md) | Orquestación | Descripción proyecto |
| grilling | [✓](./grilling/SKILL.md) | Preguntas 1x1 | Contexto |
| requirements-modeling | [✓](./requirements-modeling/SKILL.md) | Formalización | Grilling output |
| requirements-writer-skill | [✓](./requirements-writer-skill/SKILL.md) | Validación | REQ candidatos |

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

## 🎯 Resultado Final

Después de completar el workflow, tendrás:

```
PROJECT/REQ/
├── GLOSSARY.md
│   └── Todos los términos formalizados
│
├── requirements-set/
│   ├── REQ-001-[feature].md (scored ≥90)
│   ├── REQ-002-[feature].md (scored ≥90)
│   ├── REQ-003-[feature].md (scored ≥90)
│   └── requirements-summary.md
│
└── docs/adr/
    ├── 0001-[decision].md
    ├── 0002-[decision].md
    └── [...]
```

**Calidad garantizada:**
- ✅ Todos los requisitos scored ≥ 90/100
- ✅ Métodos de verificación definidos
- ✅ Trazabilidad completa
- ✅ Ninguna ambigüedad
- ✅ Listo para diseño y desarrollo

---

## 📖 Más Información

- **WORKFLOW.md** - Guía rápida y cheat sheet
- **ORCHESTRATION.md** - Flujo detallado y escenario real
- **AGENTS.md** - Configuración técnica y protocolos
- **README.md** - Este documento (índice)

---

**Versión**: 1.0  
**Basado en**: INCOSE Systems Engineering Handbook v4.0+  
**Últimas actualizaciones**: 2026-08-10
