# Guía de Configuración Multi-idioma

## Resumen

- **Una ejecución = Un solo idioma** (no hay duplicados)
- **Archivo de configuración global**: `.req-config.yml`
- **REQ-001.md** (sin sufijo de idioma)
- **GLOSSARY.md** (centralizado, en idioma actual)
- **Auto-detección**: Acentos en project_name = Español; sin acentos = Inglés

---

## Configuración Global (.req-config.yml)

Ubicado en: `/req/.req-config.yml`

```yaml
# Idioma por defecto para toda la documentación
default_language: "es"  # o "en"

# Estrategia de detección
language_detection_strategy: "auto"  # auto, explicit, o prompt
```

---

## Cómo Funciona

### OPCIÓN 1: Auto-detección (Recomendado)

```bash
/interview-requirements "Búsqueda Avanzada"
```

**Lógica:**
1. Detecta acentos en "Búsqueda Avanzada" → Español
2. Lee default_language de .req-config.yml → "es"
3. Ejecuta TODO en español:
   - Preguntas en español
   - GLOSSARY.md en español
   - REQ-001.md en español
   - requirements-summary.md en español

**Salida:**
```
/req/
├── GLOSSARY.md (en español)
└── busqueda-avanzada/
    └── requirements-set/
        ├── REQ-001.md (contenido en español)
        ├── REQ-002.md
        └── requirements-summary.md (en español)
```

---

### OPCIÓN 2: Sin acentos (Auto-detección a Inglés)

```bash
/interview-requirements "Advanced Search"
```

**Lógica:**
1. No detecta acentos → Inglés
2. Ejecuta TODO en inglés:
   - Questions in English
   - GLOSSARY.md in English
   - REQ-001.md in English

**Salida:**
```
/req/
├── GLOSSARY.md (in English)
└── advanced-search/
    └── requirements-set/
        ├── REQ-001.md (content in English)
        ├── REQ-002.md
        └── requirements-summary.md (in English)
```

---

### OPCIÓN 3: Forzar idioma (Override)

```bash
/interview-requirements "Payment Integration" language="es"
```

**Lógica:**
1. Ignora auto-detección
2. Usa parámetro explícito: `language="es"`
3. Ejecuta TODO en español (aunque project_name sea en inglés)

**Salida:**
```
/req/
├── GLOSSARY.md (en español)
└── payment-integration/
    └── requirements-set/
        ├── REQ-002.md
        ├── REQ-001.md (contenido en español)
        └── requirements-summary.md (en español)
```

---

## Estructura de Archivos Generados

**Cada ejecución genera:**

```
/req/
├── .req-config.yml (configuración global) - SIN sufijo)
│   └── Una sola versión: generada en el idioma de ejecución
│
├── busqueda-avanzada/
│   └── requirements-set/
│       ├── REQ-001.md (idioma actual, SIN sufijo de idioma)
│       ├── REQ-002.md
│       └── requirements-summary.md
│
└── payment-integration/
    └── requirements-set/
        ├── REQ-001.md (idioma actual, SIN sufijo de idioma)
        ├── REQ-002.md
        └── requirements-summary.md
```

**Nota:** 
- Los archivos generados NO tienen sufijo de idioma (REQ-001.md, no REQ-001-es.md)
- El idioma está determinado por la ejecución, NO por el nombre del archivo
- Templates de referencia existen en inglés y español (`templates/REQ-NNN-en.md`, `templates/REQ-NNN.md`)
**Nota:** No hay `REQ-001-es.md` + `REQ-001-en.md`. Solo `REQ-001.md` en el idioma de la ejecución actual.

---

## GLOSSARY.md Compartido

**Importante:**
- GLOSSARY.md es **centralizado** a nivel de proyecto
- Se actualiza en **el idioma de la ejecución actual**
- Si tienes proyectos en español e inglés:
  - Primer `interview-requirements` en español → GLOSSARY.md en español
  - Segundo `interview-requirements` en inglés → GLOSSARY.md se sobrescribe en inglés

**Solución (si necesitas mantener términos en ambos idiomas):**
- Usar `language_detection_strategy: "explicit"` en .req-config.yml
- Esto fuerza usar `default_language` siempre
- O: mantener múltiples configuraciones (`.req-config-es.yml`, `.req-config-en.yml`)

---

## Ventajas de Este Enfoque

✅ **Simplificidad**: Un archivo, un idioma por ejecución  
✅ **Claridad**: No hay confusión entre versiones  
✅ **Consistencia**: GLOSSARY.md único, centralized  
✅ **Eficiencia**: No hay duplicación de trabajo  
✅ **Flexibilidad**: Auto-detect o override según necesidad  

---

## Ejemplos de Uso Real

### Proyecto 1: Búsqueda (Español)

```bash
/interview-requirements "Búsqueda Avanzada" stakeholders="usuarios,product"
```
→ Auto-detect: "es"  
→ Genera: `busqueda-avanzada/requirements-set/REQ-00X.md`  
→ GLOSSARY.md: español  

### Proyecto 2: Pagos (Inglés)

```bash
/interview-requirements "Payment Gateway" stakeholders="finance,devops"
```
→ Auto-detect: "en"  
→ Genera: `payment-gateway/requirements-set/REQ-00X.md`  
→ GLOSSARY.md: sobrescrito en inglés

### Proyecto 3: Notificaciones (Forzar Español)

```bash
/interview-requirements "Notification System" language="es"
```
→ Override: "es"  
→ Genera: `notification-system/requirements-set/REQ-00X.md`  
→ GLOSSARY.md: español  

---

## Cambiar Default Language

**Editar `.req-config.yml`:**

```yaml
default_language: "en"  # Cambiar a inglés por defecto
```

Luego todas las auto-detecciones sin acentos usarán inglés.

---

## Resumen Rápido

| Caso | Comando | Resultado |
|------|---------|-----------|
| Español auto | `/interview-requirements "Búsqueda Avanzada"` | es ✅ |
| Inglés auto | `/interview-requirements "Advanced Search"` | en ✅ |
| Forzar español | `/interview-requirements "Project" language="es"` | es ✅ |
| Forzar inglés | `/interview-requirements "Proyecto" language="en"` | en ✅ |

---

**Status**: ✅ Implementado - FASE 1  
**Config**: `.req-config.yml`  
**Templates**: `templates/REQ-NNN.md`, `templates/GLOSSARY.md`
