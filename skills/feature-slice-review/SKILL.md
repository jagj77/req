---
name: feature-slice-review
description: Evaluate how a Laravel/PHP (or any layered) codebase is split and recommend a cut that groups files by bounded context / feature instead of by technical layer (Controllers, Services, UseCase, etc.). Renders a self-contained HTML report with Mermaid diagrams proposing the restructure. Always starts with a scout sub-agent so the heavy read passes through a minimal-info return.
disable-model-invocation: true
---

# Feature Slice Review

Audit the codebase's **current grouping** (technical layers vs bounded contexts) and propose a **cut that co-locates files by feature**. The aim: every change to a feature lives in one namespace; AI agents and humans find the moving parts without hopping across `app/Http/Controllers`, `app/Services`, `app/UseCase`, `app/Repository` for a single concept.

This skill is **deliberately distinct from** [`improve-codebase-architecture`](improve-codebase-architecture/SKILL.md):

- That skill asks "is each module deep or shallow?" and proposes interface-level deepenings. Its unit is the **module**.
- This skill asks "are files grouped in a way that matches how features evolve?" and proposes **namespace-level cuts**. Its unit is the **bounded context** (DDD) or **feature slice** (vertical slice).

Vocabulary stays shared:

- The module/interface/depth/seam terms come from `codebase-design` — used exactly, never substituted with "component", "service", "API", or "boundary".
- The bounded-context terms come from DDD: **bounded context**, **context map**, **ubiquitous language**, **anti-corruption layer**, **shared kernel**, **core domain**, **supporting subdomain**, **generic subdomain**.
- "Bounded context" is preferred over "microservice" because the output is almost always a namespace/module split, not a deployable unit. The report can still note when a context is large/independent enough to extract later.

## Reference docs

- [CONTEXT.md](CONTEXT.md) — the project's domain glossary. The cut's names must come from here (or be added as decisions land). If the file does not exist, the skill creates it lazily when a term survives grilling.
- [EVALUATION-FRAMEWORK.md](EVALUATION-FRAMEWORK.md) — the heuristic scorecard (cohesion, coupling, blast radius, churn correlation) used to grade the current grouping and the proposed cut.
- [HTML-REPORT.md](HTML-REPORT.md) — the HTML scaffold (Tailwind via CDN + Mermaid via CDN), diagram patterns (`flowchart`, `graph` for context maps), card templates, and styling guidance.

## Process

### 1. Scope the cut

Before any read, decide the unit of analysis:

- **Whole repo** (default): everything in `app/`, `database/`, `routes/`, `resources/js/Pages`. Proposes a global restructure.
- **Subsystem** (when the user names one): only files matching the concept (e.g. "the report building pipeline", "the home cards"). Proposes a per-subsystem cut.

State the scope in one sentence at the top of the report. A scope that grows during grilling is a sign the user wanted the whole repo.

### 2. Scout sub-agent — minimal-info return

**The heavy read happens in a sub-agent, not in the main thread.** The scout walks the codebase and returns a compressed digest, never verbatim source. This is a hard rule:

- The scout is dispatched with `agent: "scout"` and an output schema shaped exactly like the digest below. The main thread never reads the same files the scout reads.
- The scout's contract: **return the smallest payload that lets the main thread evaluate**. Verbatim code is forbidden. Counts, paths, and 1-line summaries only.

The scout MUST return (JSON or structured markdown — pick one):

```
{
  "scope": "<one-sentence scope>",
  "top_dirs_app": [
    { "path": "app/UseCase", "file_count": 47, "subdir_count": 8,
      "subdirs": [
        { "name": "Reportes", "file_count": 5,
          "files": ["ObtenerReportePlanificacionUseCase.php", "DbGuard.php", ...] }
      ]
    },
    ...
  ],
  "controllers": [
    { "path": "app/Http/Controllers/ReportePlanificacionController.php",
      "namespace_hint": "Reportes",
      "usecase_calls": ["ObtenerReportePlanificacionUseCase"],
      "route_hints": ["reporte/planificacion", "api/reporte/planificacion"] }
  ],
  "use_cases": [
    { "path": "app/UseCase/Reportes/ObtenerReportePlanificacionUseCase.php",
      "uses_models": ["Reparticion", "Role", "User"],
      "uses_services": ["PlanificacionSIGECI"],
      "uses_db_tables": ["vw_analisis_tratamiento_riesgo", "presupuesto_reparticion"],
      "reads_routes_or_pages": ["reporte/planificacion"] }
  ],
  "services": [
    { "path": "app/Services/PlanificacionSIGECI.php",
      "imports": ["Illuminate\\Support\\Facades\\DB"],
      "db_connections": ["sigeci"] }
  ],
  "models": [
    { "path": "app/Models/Reparticion.php",
      "table_hint": "public.reparticiones",
      "shared_with": ["User", "Role"] }
  ],
  "pages": [
    { "path": "resources/js/Pages/Reporte/Planificacion/Index.vue",
      "props_used": ["areas", "ministerios", "cicloAuditoria"] }
  ],
  "routes_files": ["routes/web.php"],
  "migration_count": 87,
  "feature_signals": [
    { "signal": "Planificación", "evidence": ["ReportePlanificacionController", "ObtenerReportePlanificacionUseCase", "PlanificacionSIGECI", "Index.vue"], "size_loc": 2400 }
  ],
  "cross_feature_imports": [
    { "from": "Reportes/ObtenerReportePlanificacionUseCase", "to": "User", "kind": "shared-model" }
  ]
}
```

How the scout gets there:

1. Walk `app/` first: list every directory under `app/Http/Controllers`, `app/UseCase`, `app/Services`, `app/Repository`, `app/Models`, `app/Actions`, `app/Rules`. Record `file_count` and `subdir_count` for each top dir, then list the immediate children.
2. For each controller, parse the constructor and method bodies (just `use` statements and 1-line method signatures). Record what `UseCase`/`Service` it calls. The scout does **not** dump method bodies.
3. For each `UseCase`, record its `use` imports (Models, Services, other UseCases, facades) and the SQL strings it issues (just the table names, not the queries).
4. For each Service, record its imports and DB connection strings.
5. For each Model, record the path and a table name from `$table` or convention.
6. Walk `routes/web.php` (and `routes/api.php` if present) for route → controller mappings. Record 1-line route hints (URL prefix + name).
7. Walk `resources/js/Pages` and group by top-level folder (Reporte, Home, etc.). For each top-level folder, list the page files and the props they consume from Inertia (just the prop names).
8. Walk `database/migrations` and `database/migrations/*` (any `fn_*`, `vw_*`, `tr_*` files are domain-specific). Record counts, not contents.
9. From the accumulated evidence, infer **feature signals**: clusters of files that look like they serve the same concept. The scout names them with a noun phrase and cites the files. Names are guesses, not facts — the main thread will grill them.

**Hard rule on file count**: if a single top-level app dir has > 60 files, the scout lists only the top-15 subdirs by file count and aggregates the rest under a `_other` bucket. The report's goal is decision-making, not exhaustive coverage.

**Hard rule on source dumps**: the scout may not include more than 2 verbatim lines from any single file. If the main thread needs more, it asks the scout for a specific symbol.

### 3. Main thread evaluation

With the digest, score the current grouping and propose the cut. The scorecard lives in `EVALUATION-FRAMEWORK.md` — read it before grading. Five axes, each 0–5:

- **Cohesion (intra-context)**: are files of one feature in the same namespace? Today: low (Controllers separated from UseCase separated from Services).
- **Coupling (inter-context)**: do features share files that shouldn't be shared? Today: high (User, Role, Reparticion shared everywhere).
- **Blast radius of a feature change**: how many directories does a one-feature change touch? Higher is worse.
- **Churn correlation**: do files that change together live together? Use `git log --name-only --pretty=format: -- <since>` to spot clusters, but only as evidence — the cut can ignore churn if the user wants a clean-slate proposal.
- **Discoverability**: can a new agent find "the report planning code" in < 5 hops?

For the **proposed cut**:

- **Top-level contexts**: 4–8 names, each a noun phrase. Names come from the feature signals the scout found. Each context lists which existing files move into it.
- **Shared kernel** (optional, small): files every context genuinely needs (User, Role, common value objects). Cap at 5 files. Anything bigger belongs in its own context.
- **Anti-corruption layer** (optional, per external system): e.g. `app/Context/Planificacion/Infrastructure/SIGECI/` wraps the SIGECI connection so the context's domain layer never imports `Illuminate\Support\Facades\DB::connection('sigeci')` directly.
- **Migration path**: 3–5 phases. Phase 1 is always "introduce the new namespace tree, move 1 context as a vertical slice, leave everything else alone." Each phase must be independently shippable. Phase 4+ must include a feature flag or a `// TODO(feature-slice)` shim if the old path stays live.

### 4. Render the HTML report

Write to `<tmpdir>/feature-slice-review-<timestamp>.html` (resolve `$TMPDIR` → `/tmp` → `%TEMP%`). Open it (`start` / `open` / `xdg-open`). Absolute path returned to the user.

Scaffold, card structure, and diagram patterns are in [HTML-REPORT.md](HTML-REPORT.md). Key points:

- **Tailwind + Mermaid via CDN**, same style as the architecture review so the two reports look like siblings.
- **Three diagrams minimum**: current layout (boxes per technical layer), proposed context map (boxes per bounded context, edges for shared-kernel/ACL/shared-state), and the migration roadmap (sequenceDiagram or timeline).
- Each **candidate context** gets a card with: name, files-in / files-out, cohesion/coupling scores (current vs proposed), before/after diagram, migration phase, blast-radius delta.
- **Top recommendation**: which context to slice first and why. Default: the context with the worst cohesion × highest churn.
- Tone is editorial, not corporate-dashboard. Plain English, no hedging.

Use the project's `CONTEXT.md` vocabulary for the domain; use the `codebase-design` vocabulary for the architecture (module/interface/depth/seam). If `CONTEXT.md` defines "Planificación", the card says "the Planificación context", not "the Reportes folder" and not "the planning service".

### 5. Grilling loop

After the file is written, ask the user: **"Which context would you like to cut first, or do you want to grill the cut names before any move?"**

If they want to grill the names, call the `grilling` skill. Decisions land inline:

- A new term survives (e.g. "the Auditoría context, distinct from Planificación") → add to `CONTEXT.md` (create the file if missing) under a `## Bounded contexts` section.
- A term is rejected with a load-bearing reason (e.g. "we can't touch `app/Http/Controllers` because of an audit-trail policy") → offer to write an ADR under `docs/adr/`. Frame it as: _"Want me to record this as an ADR so future reviews don't re-suggest it?"_
- Two contexts want to share a Model (e.g. `Reparticion` between Planificación and Home cards) → grill whether it goes in shared kernel, in one context with the other consuming via ACL, or duplicated.

Once a context is approved, call `improve-codebase-architecture` for that single context — it's the right next skill for module-level deepening inside the new namespace.

## What this skill never does

- **Never moves files.** The output is a plan, not a refactor. The user (or a follow-up skill) decides when to execute the migration phases.
- **Never proposes microservices.** A bounded context is a namespace, not a deployable unit. The report can flag a context as "candidate for extraction" but does not recommend it.
- **Never touches `vendor/`, `node_modules/`, `public/build/`, `storage/framework/`.** These are out of scope.
- **Never deletes a context.** A context with score 0 on every axis is still listed with a note "_deferred: low value to slice, leave as-is for now._"
- **Never invents domain terms.** Names come from `CONTEXT.md`, from the scout's feature signals, or from grilling. If no source, the skill surfaces the gap and asks.

## Acceptance

A review is complete when:

- The HTML report opens cleanly in a browser (Tailwind + Mermaid render).
- Each candidate context card shows a real before/after diagram (no "TODO: draw diagram").
- The Top recommendation section names one context and cites the evidence (churn + cohesion numbers from the scout).
- The migration roadmap has ≥ 3 phases, each independently shippable.
- The scout's output schema is respected: no verbatim source dumps in the digest.
