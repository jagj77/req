# Evaluation Framework

The scorecard for grading the current grouping and the proposed cut. Five axes, each 0–5. Higher is better on every axis except **blast radius** and **churn correlation**, where lower (more focused) is better.

Use the numbers in the report. Never publish a "high cohesion" claim without the number behind it.

## Axes

### 1. Cohesion (intra-context) — 0 to 5

How tightly coupled are the files of a single concept, today and after the cut?

- **0**: every file of one feature lives in a different top-level dir (Controller in one place, UseCase in another, Service in a third, View in a fourth).
- **3**: files of one feature share a namespace inside one or two top-level dirs (e.g. all under `app/UseCase/Reportes/` but Controllers in `app/Http/Controllers/`).
- **5**: every file of one feature lives under a single namespace (`app/Context/Planificacion/` contains Controller + UseCase + Service + View + tests).

**How to measure**: for each feature signal, count the number of top-level `app/` subdirs the feature's files are spread across. ≤ 1 dir → 5, 2 dirs → 3, 3 dirs → 2, ≥ 4 dirs → 0–1.

### 2. Coupling (inter-context) — 0 to 5

How many **shared files** exist that aren't in the proposed shared kernel?

- **0**: every feature imports Models, Services, or value objects from every other feature with no encapsulation. (Typical Laravel layered layout.)
- **3**: shared models exist (`User`, `Role`, `Reparticion`) but the coupling is one-way (features consume, don't mutate the shared model's contracts).
- **5**: a defined shared kernel ≤ 5 files. Features import only from the shared kernel or their own context.

**How to measure**: walk the imports of files inside one proposed context. Count files imported from outside the context that are not in the shared kernel.

### 3. Blast radius — 0 to 5 (lower is better; **invert for total score**)

How many top-level `app/` directories does a one-feature change touch today vs after the cut?

- **0**: a feature change touches 5+ directories (Controllers + UseCases + Services + Repositories + Views + migrations + routes).
- **3**: a feature change touches 3–4 directories.
- **5**: a feature change touches ≤ 2 directories (the context namespace + `routes/web.php`).

**Inversion**: when scoring, do `axis_score = 5 - blast_radius_raw`. Otherwise the scorecard is ambiguous (lower blast radius = better, but lower cohesion = worse — same direction in the number, opposite direction in reality).

### 4. Churn correlation — 0 to 5

Do files that change together live together? Use git history as evidence, not as the deciding factor.

**How to measure** (the scout, not the main thread):

```bash
git log --name-only --pretty=format: --since="6 months ago" -- app/ | \
  grep -E '^app/' | sort | uniq -c | sort -rn | head -30
```

Then cluster by feature signal: do the top-churn files for one feature live in the same proposed context? If yes → 4–5. If they're scattered → 0–2.

**Important caveat**: churn is evidence, not ground truth. Some features are young and have low churn; some are stable and have low churn. A young feature with 5 commits can still be high-correlation if all 5 commits touched the same files. A "stable" feature with 100 commits across 30 files is **low** correlation regardless of volume. The skill reports the number and the caveat.

### 5. Discoverability — 0 to 5

Can a new agent (human or AI) find "the report planning code" in ≤ 5 directory hops?

- **0**: the answer requires reading `routes/web.php` → finding the controller → grepping the controller for `app(` → finding the UseCase → grepping the UseCase for `app(` → finding the Service. 6+ hops.
- **3**: the controller name and the UseCase name share a noun (e.g. `ReportePlanificacionController` + `ObtenerReportePlanificacionUseCase`), so a string match reveals the cluster. 3–4 hops.
- **5**: a single namespace (`app/Context/Planificacion/`) contains everything. 1 hop.

**How to measure**: pick 3 random feature signals. For each, count the `find` / `grep` / `cat` invocations an agent would need to list every file that implements it. Average the three counts.

## Scoring the report

For each candidate context card, show a small table:

| Axis | Current | Proposed |
|------|---------|----------|
| Cohesion | 2 | 5 |
| Coupling | 1 | 4 |
| Blast radius | 0 (raw 5) | 4 (raw 1) |
| Churn correlation | 3 | 4 |
| Discoverability | 2 | 5 |
| **Total** | **8 / 25** | **22 / 25** |

The total is informational, not decisive. A context with low churn correlation but high cohesion can still be worth slicing if the cohesion gain is the user's stated goal (e.g. "we want AI agents to find this faster").

## What the scorecard is not

- It is **not** a quality gate. A feature with score 0 on every axis is not forbidden — it might be a candidate for **deferral** rather than slicing (see "What this skill never does" in `SKILL.md`).
- It is **not** a metric for code review. It grades **namespace layout**, not the code inside.
- It is **not** a substitute for grilling. When two contexts tie on every axis, the deciding factor is domain language: which term is in `CONTEXT.md`? which one would a new hire use first?

## When to skip scoring

If the codebase has < 20 source files total, scorecard axes collapse (cohesion is trivially 5, churn correlation is undefined). In that case, render the candidate cards **without** the score table and note in the header: "_small codebase — scorecard omitted; proposal stands on the diagrams alone._"
