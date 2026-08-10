# WORKFLOW.md - Guía Rápida

## En 30 segundos

```
USER: /interview-requirements [project description]
  ↓
GRILLING: Ask questions one-at-a-time → needs + decisions
  ↓
REQUIREMENTS-MODELING: Formalize → GLOSSARY.md + REQ candidates + ADRs
  ↓
REQUIREMENTS-WRITER: Validate → scored, verified requirements
  ↓
OUTPUT: requirements-set/, GLOSSARY.md, docs/adr/
```

---

## Cada Skill en Una Línea

| Skill | Hace | Entrada | Salida |
|-------|------|---------|--------|
| **interview-requirements** | Orquesta todo | Descripción proyecto | Deliverable final |
| **grilling** | Entrevista profunda | Contexto | Necesidades+decisiones |
| **requirements-modeling** | Formaliza modelo | Grilling output | GLOSSARY+REQ+ADRs |
| **requirements-writer-skill** | Valida requisitos | REQ candidatos | REQ scored ✅ |

---

## Archivo Structure Generado

```
PROJECT/
├── REQ/
│   ├── GLOSSARY.md                           ← Términos centralizados
│   ├── requirements-set/
│   │   ├── REQ-001-[feature].md              ← Requisitos finales
│   │   └── requirements-summary.md           ← Resumen
│   └── docs/adr/
│       ├── 0001-[decision].md                ← Decisiones arquitectónicas
│       └── 0002-[decision].md
```

---

## Flujo Visual Paso a Paso

### Paso 1️⃣ : Usuario Inicia

```
/interview-requirements
  Proyecto: Búsqueda Avanzada
  Stakeholders: Usuarios finales, Marketing, Producto
```

### Paso 2️⃣ : Grilling (Extracción)

```
GRILLING Q1: "¿Cuál es el mayor problema que resuelve?"
   USER: "Usuarios no encuentran docs antiguos"
   
GRILLING Q2: "¿Cuántos docs típicamente?"
   USER: "100k a 1M"
   
GRILLING Q3: "¿Máximo tiempo aceptable?"
   USER: "< 3 segundos"
   
[... continúa ...]

OUTPUT: Needs articuladas, decisiones, ambigüedades
```

### Paso 3️⃣ : Requirements-Modeling (Formalización)

```
Término: "búsqueda rápida"
DESAFÍO: "¿Rápida significa < 3 seg? ¿Cómo se mide?"

✍️ GLOSSARY.md:
   ## Search_Performance
   Definition: Search results returned < 3 seconds
   Units: milliseconds
   Related: Query, Search_System

Escenario: ¿Si hay 1M docs?
DECISIÓN: "< 3 seg normal, < 10 seg máximo"

✍️ ADR: "Elasticsearch para escalabilidad"

✍️ REQ-001-search-performance.md (candidato)
```

### Paso 4️⃣ : Requirements-Writer (Validación)

```
CANDIDATO:
"The Search_System shall return results within 3 seconds"

EVALUACIÓN:
- C1-C6: ✅ Todas pasan
- R1-R41: ✅ Cumple
- Score: 95/100

✍️ REQ-001-search-performance.md (final)
  • Requirement validated
  • Verification: Automated test
  • Quality: 95/100
  • Ready for design
```

### Paso 5️⃣ : Completación

```
✅ GLOSSARY.md completo
✅ REQ-001, REQ-002, REQ-003 finales
✅ ADRs documentados
✅ Traceabilidad completa
✅ Listo para diseño y desarrollo
```

---

## Puntos de Quiebre (Cuándo Loops Iteran)

### Loop 1: Requirements-Writer → Requirements-Modeling

```
TRIGGER: Score < 90 o ambigüedad detectada

MENSAJE:
"REQ-001 necesita clarificar 'Performance'.
 ¿Es 3 segundos para query simple? ¿Para 1M docs?
 ¿Incluye network latency?"

REQUIREMENTS-MODELING actualiza GLOSSARY,
REQUIREMENTS-WRITER re-evalúa
```

### Loop 2: Escenarios Edge Case

```
REQUIREMENTS-MODELING propone:
"¿Qué pasa si:"
- "Database está caída?"
- "Usuario sin permisos?"
- "Query malformada?"
- "Result set > 1M rows?"

Cada escenario puede generar nuevo requisito
o refinar existente
```

---

## Criterios de Completitud

✅ **GRILLING completado cuando:**
- [ ] Todas las branches del design tree exploradas
- [ ] Dependencias entre decisiones resueltas
- [ ] Stakeholder needs articuladas
- [ ] No hay preguntas abiertas críticas

✅ **REQUIREMENTS-MODELING completado cuando:**
- [ ] GLOSSARY.md contiene todos los términos
- [ ] requirements-set/ tiene todos los requisitos candidatos
- [ ] ADRs documentan decisiones clave
- [ ] No hay contradicciones entre requisitos

✅ **REQUIREMENTS-WRITER completado cuando:**
- [ ] Todos los requisitos scored ≥ 90/100
- [ ] Método de verificación definido para cada uno
- [ ] Cero violaciones C1-C6
- [ ] Cero violaciones R1-R15
- [ ] Todos los términos en GLOSSARY.md

✅ **WORKFLOW completado cuando:**
- [ ] requirements-set/requirements-summary.md existe
- [ ] Trazabilidad needs → requirements → verification completa
- [ ] Todos stakeholders satisfied
- [ ] Listo para design phase

---

## Comandos Rápidos

```bash
# Iniciar flujo completo
/interview-requirements "Descripción del proyecto"

# Solo grilling
/grilling

# Solo modelado
/requirements-modeling

# Solo validación
/requirements-writer-skill

# Ver estado actual
Abrir: REQ/GLOSSARY.md
Abrir: REQ/requirements-set/
Abrir: REQ/docs/adr/
```

---

## Definiciones Clave (Muy Conciso)

| Término | Significa |
|---------|-----------|
| **Grilling** | Preguntar relentlessly, uno/uno |
| **Modeling** | Formalizar términos + estructura |
| **Glossary** | Hub central de términos |
| **REQ-NNN** | Requisito con ID único |
| **ADR** | Architectural Decision Record |
| **C1-C6** | Características de buen requisito |
| **R1-R41** | Reglas de formato de requisito |
| **Score 90+** | Requisito listo para diseño |

---

## Errores Comunes

❌ **NO hacer:**
- Preguntar múltiples preguntas a la vez (grilling)
- Batching glossary updates (formalizar en tiempo real)
- Saltar requirements-writer validation (todos ≥90)
- Requisitos sin verification method

✅ **SÍ hacer:**
- Una pregunta → feedback → siguiente pregunta
- Actualizar GLOSSARY.md inmediatamente
- Iterar si score < 90
- Definir verification method para cada REQ

---

## Inversión de Tiempo Típica

| Fase | Duración | Salida |
|------|----------|--------|
| Grilling | 30-60 min | Necesidades articuladas |
| Modeling | 45-90 min | GLOSSARY + REQ candidatos + ADRs |
| Validation | 30-60 min | REQ finales scored |
| **Total** | **2-4 horas** | **Requisitos de calidad** |

*(varía según complejidad del proyecto)*

---

## Documentación de Apoyo

- [ORCHESTRATION.md](./ORCHESTRATION.md) - Flujo conceptual detallado
- [AGENTS.md](./AGENTS.md) - Configuración técnica y protocolos
- [requirements-writer-skill/SKILL.md](./requirements-writer-skill/SKILL.md) - Validación
- [requirements-writer-skill/characteristics.md](./requirements-writer-skill/characteristics.md) - C1-C6
- [requirements-writer-skill/rules.md](./requirements-writer-skill/rules.md) - R1-R41
- [requirements-writer-skill/review_algorithm.md](./requirements-writer-skill/review_algorithm.md) - Algoritmo

---

## Contacto con la Metodología INCOSE

Este workflow implementa:
- ✅ **Systematic process** (INCOSE SE Handbook)
- ✅ **Structured lifecycle** (Concept → Needs → Requirement → Verification → Validation)
- ✅ **Quality characteristics** (C1-C6 based on INCOSE/IEEE standards)
- ✅ **Formal specification** (R1-R41 rules)
- ✅ **Traceability** (needs → requirements → verification)
- ✅ **Configuration management** (GLOSSARY, ADRs)
- ✅ **Verification methods** (Inspection, Analysis, Demo, Test)

Ver [requirements-engineering.md](./requirements-writer-skill/requirements-engineering.md) para detalle.
