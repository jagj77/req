# HTML Report Format

The feature-slice review renders as a single self-contained HTML file in the OS temp directory. Tailwind and Mermaid both come from CDNs. Mermaid handles context maps and timelines reliably; hand-built divs and SVG handle the more editorial visuals.

The format is a **sibling** of `improve-codebase-architecture/HTML-REPORT.md` — same scaffold, same accent palette, same conventions — so a reader can put both reports side-by-side without cognitive overhead. Differences are local to the diagrams and the candidate card.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Feature slice review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .shared-kernel { fill: #fef3c7; stroke: #d97706; }
      .context { fill: #ecfdf5; stroke: #047857; }
      .external { fill: #f1f5f9; stroke: #475569; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="scorecard">...</section>
      <section id="current-layout">...</section>
      <section id="proposed-cut">...</section>
      <section id="contexts" class="space-y-10">...</section>
      <section id="migration">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

- Repo name (e.g. "SICORE").
- Date.
- Scope sentence (one line): "Whole repo (app/, database/, routes/, resources/js/Pages/)" or the subsystem named by the user.
- Compact legend:
  - Green box = bounded context.
  - Amber box = shared kernel.
  - Slate box = external system (DB, third-party, framework boundary).
  - Dashed line = anti-corruption layer (the context imports the external through a wrapper).
  - Red arrow = coupling that survives the cut (e.g. a feature still imports a Model from another context).

## Scorecard section

A small table at the top, before any context cards:

| Axis | Current | Proposed |
|------|---------|----------|
| Cohesion | 2 / 5 | 4 / 5 |
| Coupling | 1 / 5 | 4 / 5 |
| Blast radius (lower better) | 0 (raw 5) | 4 (raw 1) |
| Churn correlation | 3 / 5 | 4 / 5 |
| Discoverability | 2 / 5 | 5 / 5 |
| **Total** | **8 / 25** | **21 / 25** |

If the codebase has < 20 source files, replace the table with a note: "_small codebase — scorecard omitted; proposal stands on the diagrams alone._"

## Current layout diagram

A Mermaid `graph LR` of the existing top-level dirs:

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    graph LR
      subgraph Layered
        direction LR
        C[app/Http/Controllers<br/>47 files]
        U[app/UseCase<br/>52 files]
        S[app/Services<br/>18 files]
        R[app/Repository<br/>11 files]
        M[app/Models<br/>34 files]
        V[resources/js/Pages<br/>76 files]
      end
      C -->|controllers call| U
      U -->|use cases call| S
      U -->|use cases call| R
      U -->|models| M
      V -->|Inertia props from| C
      classDef layered fill:#f1f5f9,stroke:#475569;
      class C,U,S,R,M,V layered;
  </pre>
</div>
```

The point: the diagram alone shows that **one feature lives across 5+ boxes**. No prose needed.

## Proposed context map

A Mermaid `graph TB` showing the proposed contexts, the shared kernel, and the external systems:

```html
<pre class="mermaid">
  graph TB
    subgraph SharedKernel["Shared kernel"]
      SK1[User]
      SK2[Role]
      SK3[Reparticion]
    end
    subgraph PlanningCtx["Planificación context"]
      PC1[ReportePlanificacionController]
      PC2[ObtenerReportePlanificacionUseCase]
      PC3[PlanificacionSIGECI]
      PC4[Planificacion/Index.vue]
    end
    subgraph HomeCtx["Home context"]
      HC1[HomeController]
      HC2[CardRenderers]
      HC3[Home.vue]
    end
    subgraph MaturityCtx["Madurez context"]
      MC1[ObtenerConsolidadoMadurezUseCase]
      MC2[MadurezService]
    end
    subgraph External["External"]
      EX1[(pgsql: sicore)]
      EX2[(pgsql: sigeci)]
    end
    PlanningCtx -.ACL.-> External
    HomeCtx --> SharedKernel
    PlanningCtx --> SharedKernel
    MaturityCtx --> SharedKernel
    PlanningCtx -->|consumes NGC| MaturityCtx
    classDef ctx fill:#ecfdf5,stroke:#047857;
    classDef sk fill:#fef3c7,stroke:#d97706;
    classDef ext fill:#f1f5f9,stroke:#475569;
    class PC1,PC2,PC3,PC4,HC1,HC2,HC3,MC1,MC2 ctx;
    class SK1,SK2,SK3 sk;
    class EX1,EX2 ext;
</pre>
```

Edges mean:

- Solid arrow → direct call / import.
- `-.ACL.->` (dashed) → anti-corruption layer (the context accesses an external system through a wrapper in its own namespace, never the bare connection string).
- Two contexts with a solid arrow between them is a **shared state** or **direct dependency**. The skill surfaces these in the scorecard's coupling row.

## Context cards (per bounded context)

Each context is one `<article>`:

- **Title**: the bounded context name (noun phrase). Use the project's `CONTEXT.md` term, or the term that survived grilling.
- **Badge row**:
  - Recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate, `Defer` = stone).
  - Scope tag (`Core domain` / `Supporting subdomain` / `Generic subdomain`).
  - Size tag (`~ N files`, `~ M lines`).
- **Files**: monospaced list. Two columns when > 6 files: `moves in` / `moves out`.
- **Before / After diagram**: the centerpiece. Two columns, side by side. The "before" shows the same files scattered across the layered layout. The "after" shows them inside the new namespace.
- **Cohesion / Coupling table**: per the framework, current vs proposed. Always present, even when the gain is small.
- **Migration phase**: which of the 3–5 phases this context is cut in. Phase 1 is always low-risk; later phases depend on it.
- **Blast-radius delta**: "today a one-line feature change touches 5 dirs; after, 1 dir + 1 line in `routes/web.php`."
- **Risks**: 2–4 bullets. Things that could go wrong (shared Model mutation, hidden tests, route-name conflicts).
- **Wins**: 2–4 bullets. In `codebase-design` vocabulary: locality (changes concentrate in one namespace), leverage (one move reaches all call sites), discoverability (one `find app/Context/Planificacion` lists everything).

### Before / After patterns

Three patterns, mix them. Don't make every card look the same.

#### Pattern A — File scatter (the workhorse)

Use when the "before" is files spread across `Controllers / UseCase / Services / Views`.

```
BEFORE:
  app/Http/Controllers/ReportePlanificacionController.php
  app/UseCase/Reportes/ObtenerReportePlanificacionUseCase.php
  app/UseCase/Reportes/DbGuard.php
  app/Services/PlanificacionSIGECI.php
  resources/js/Pages/Reporte/Planificacion/Index.vue
  resources/js/Pages/Reporte/Planificacion/CicloAuditoriaTabla.vue

AFTER:
  app/Context/Planificacion/
    Controllers/ReportePlanificacionController.php
    UseCase/ObtenerReportePlanificacionUseCase.php
    UseCase/DbGuard.php
    Infrastructure/PlanificacionSIGECI.php
    Pages/Index.vue
    Pages/CicloAuditoriaTabla.vue
    Pages/Composables/useReportePlanificacion.js
```

Hand-built `<div>` with monospaced text in two columns. No need for Mermaid here — a file-list diff is the clearest visualization.

#### Pattern B — Context map zoom (when the context shares state)

Use when the context imports from other contexts (e.g. Planificación reads NGC from Madurez). A small Mermaid `graph LR` showing only the dependencies of this context:

```html
<pre class="mermaid">
  graph LR
    PC[Planificación] -->|NGC| MC[Madurez]
    PC -->|User, Role| SK[Shared kernel]
    PC -.ACL.-> SIG[(sigeci)]
    classDef ctx fill:#ecfdf5,stroke:#047857;
    classDef sk fill:#fef3c7,stroke:#d97706;
    class PC,MC ctx;
    class SK sk;
</pre>
```

#### Pattern C — Sequence (when the cut removes a hop)

Use when the current call chain crosses layers unnecessarily and the cut consolidates it.

```html
<pre class="mermaid">
  sequenceDiagram
    participant V as Planificacion/Index.vue
    participant C as ReportePlanificacionController
    participant U as ObtenerReportePlanificacionUseCase
    participant S as PlanificacionSIGECI
    V->>C: HTTP GET (today: 4 hops)
    C->>U: execute
    U->>S: query SIGECI
    S-->>U: rows
    U-->>C: DTO
    C-->>V: Inertia response
    Note over V,S: After cut: V → C → U → S all live in<br/>app/Context/Planificacion/
</pre>
```

## Migration roadmap section

A Mermaid `sequenceDiagram` or a custom timeline showing the 3–5 phases. Each phase is one `<article>` with:

- **Phase N**: <verb> <context>.
- **Files moved**: monospaced list.
- **Ship signal**: what makes this phase mergeable (e.g. "all tests pass + feature flag toggles between old/new namespace").
- **Rollback**: 1 sentence on how to revert without losing data.
- **Estimated risk**: `Low` / `Medium` / `High`. Phase 1 is always `Low`. Any phase that touches `routes/web.php` is at least `Medium`.

Phase template:

```html
<article class="rounded-lg border border-slate-200 bg-white p-6">
  <div class="flex items-center justify-between mb-3">
    <h3 class="text-lg font-bold">Phase 1 — Introduce the namespace + move Madurez</h3>
    <span class="text-xs uppercase tracking-wider px-2 py-1 rounded bg-emerald-100 text-emerald-800">Low risk</span>
  </div>
  <p class="text-sm text-slate-700 mb-3">
    Create <code class="font-mono">app/Context/Madurez/</code>. Move the three files in
    (controller, use case, page). Update <code class="font-mono">composer.json</code> autoload
    if needed. Add <code class="font-mono">app/Context/Madurez/README.md</code> with the
    context's contract.
  </p>
  <p class="text-sm text-slate-700">
    <strong>Ship signal</strong>: all existing tests pass with the new paths.
    <strong>Rollback</strong>: revert the rename commit; namespaces are pure PHP.
  </p>
</article>
```

## Top recommendation section

One larger card. Context name, one sentence on why, anchor link to its card. Cite the numbers (e.g. "_Planificación: cohesion 2 → 5, blast radius 5 → 1, 2400 lines of the most-churned code in the repo_").

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace.
- Colour sparingly: emerald for context, amber for shared kernel, slate for external, red for leakage.
- Diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams.
- No interactivity beyond Mermaid's own rendering. No app code, no analytics, no chart libraries.

## Tone

Plain English, concise. Use `codebase-design` vocabulary for the architecture (module, interface, depth, seam) and DDD vocabulary for the grouping (bounded context, shared kernel, anti-corruption layer, ubiquitous language). Concision is not an excuse to drift.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality, bounded context, shared kernel, anti-corruption layer, ubiquitous language, core domain, supporting subdomain, generic subdomain.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module) · microservice (for bounded context — a context is a namespace, not a deployable unit).

**Phrasings that fit the style:**

- "Planificación is a **bounded context** with low cohesion today: 5 dirs to change one feature."
- "The **shared kernel** is User + Role + Reparticion. Anything bigger is its own context."
- "The **anti-corruption layer** wraps SIGECI so the context's UseCases never `DB::connection('sigeci')` directly."
- "**Locality**: a one-line change to the planning chart now touches one namespace."
- "**Discoverability**: `find app/Context/Planificacion -name '*.php'` lists every file that implements the feature."

No hedging, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in `codebase-design` or DDD, reach for one that is before inventing a new one.
