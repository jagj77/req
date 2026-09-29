# GLOSARIO - Diccionario de Términos Centralizados

**Proyecto/Proyectos**: [Todos | multi-proyecto]  
**Idioma**: {language} (Español/English)  
**Última actualización**: {date}  

---

## Cómo usar este glosario

- Este glosario es el **único punto de verdad** para terminología en todos los requisitos
- Todos los términos definidos aquí DEBEN usarse consistentemente en todos los REQ-NNN.md
- Si un término no está definido aquí, es **ambiguo** y debe ser rechazado
- Cada entrada incluye: Definición, Contexto, Términos relacionados, Ejemplos

---

## Términos Centralizados

### Sistema_Búsqueda

**Definición**: Componente del sistema responsable de indexar, almacenar y recuperar información documentada según criterios de búsqueda especificados por el usuario.

**Contexto**: Se utiliza en requisitos de búsqueda, indexación y recuperación de datos.

**Términos relacionados**: 
- Consulta_Búsqueda
- Índice_Búsqueda
- Resultados_Búsqueda

**Ejemplo**: "El Sistema_Búsqueda debe procesar 100k documentos sin exceder 3 segundos de latencia."

**Notas adicionales**: También conocido como "Motor de Búsqueda" en contextos empresariales. No confundir con "Búsqueda Avanzada" que es una característica.

---

### Consulta_Búsqueda

**Definición**: Solicitud estructurada del usuario al Sistema_Búsqueda que especifica criterios de búsqueda mediante operadores (AND, OR, NOT) y filtros (rango de fechas, tipo de documento, autor).

**Contexto**: Entrada del usuario que inicia el proceso de búsqueda.

**Términos relacionados**:
- Sistema_Búsqueda
- Operador_Búsqueda
- Filtro_Búsqueda

**Ejemplo**: "El usuario envía una Consulta_Búsqueda: 'python AND framework AND 2023:2024' con filtro autor='Guido'"

**Notas adicionales**: Una Consulta_Búsqueda puede ser simple (palabra clave) o compleja (operadores booleanos + filtros).

---

### Resultados_Búsqueda

**Definición**: Conjunto ordenado de documentos que coinciden con los criterios de una Consulta_Búsqueda, presentados al usuario con relevancia y metadatos asociados.

**Contexto**: Salida del Sistema_Búsqueda después de procesar una Consulta_Búsqueda.

**Términos relacionados**:
- Sistema_Búsqueda
- Consulta_Búsqueda
- Relevancia
- Clasificación

**Ejemplo**: "Los Resultados_Búsqueda se muestran en orden de relevancia descendente con snippet de 150 caracteres."

**Notas adicionales**: Un Resultado_Búsqueda es un elemento individual; Resultados_Búsqueda (plural) es la colección completa.

---

### Índice_Búsqueda

**Definición**: Estructura de datos optimizada que mapea términos clave a documentos, permitiendo retrieval rápido sin necesidad de scanning secuencial.

**Contexto**: Componente interno del Sistema_Búsqueda para optimizar rendimiento.

**Términos relacionados**:
- Sistema_Búsqueda
- Indexación
- Token

**Ejemplo**: "El Índice_Búsqueda se construye durante la fase de indexación usando tokenización estándar."

**Notas adicionales**: Puede ser inverted index, full-text index, u otro tipo según implementación.

---

### Latencia_Búsqueda

**Definición**: Tiempo transcurrido desde que el Sistema_Búsqueda recibe una Consulta_Búsqueda hasta que retorna los Resultados_Búsqueda al usuario.

**Contexto**: Métrica de rendimiento crítica en requisitos de búsqueda.

**Términos relacionados**:
- Sistema_Búsqueda
- Consulta_Búsqueda
- SLA

**Ejemplo**: "La Latencia_Búsqueda no debe exceder 3 segundos para 99.9% de consultas."

**Notas adicionales**: Incluye tiempo de procesamiento + transmisión de red. No incluye rendering en UI.

---

### Relevancia

**Definición**: Medida cuantitativa de qué tan bien un documento coincide con los criterios de una Consulta_Búsqueda, calculada mediante algoritmos de scoring.

**Contexto**: Criterio de ordenamiento en Resultados_Búsqueda.

**Términos relacionados**:
- Resultados_Búsqueda
- Clasificación
- Scoring

**Ejemplo**: "Los documentos se ordenan por Relevancia utilizando algoritmo BM25 con boosts para campos de título."

**Notas adicionales**: La Relevancia es subjetiva; debe validarse contra expectativas del usuario.

---

### [Agregar más términos según proyecto...]

---

## Validación de Consistencia

**Total de términos definidos**: {count}

**Términos verificados en requisitos**: ✅ Sí/❌ No

**Últimas acciones**:
- [Terminología agregada en REQ-001]
- [Aclaración de término "Búsqueda Avanzada" vs "Sistema_Búsqueda"]
- [Nuevo término: "Latencia_Búsqueda" para SLA]

---

## Historial de Cambios

| Fecha | Acción | Término | Versión |
|-------|--------|---------|---------|
| 2026-08-10 | Agregar | Sistema_Búsqueda | 1.0 |
| 2026-08-10 | Agregar | Consulta_Búsqueda | 1.0 |
| 2026-08-10 | Agregar | Resultados_Búsqueda | 1.0 |

---

**Status**: ✅ Activo  
**Mantenido por**: [nombre del equipo]
