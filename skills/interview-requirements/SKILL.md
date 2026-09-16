---
name: interview-requirements
description: |
  Requirements-engineering orchestrator. Use this skill whenever the user
  describes a need, feature, permission, role, workflow, bug, integration,
  or any other product change — even when phrased as a direct
  implementation request.

  Runs a complete requirements workflow:
    1. /grilling-requirements    — relentless stakeholder interview
    2. /requirements-modeling   — formalize GLOSSARY.md + REQ-NNN.md
    3. /requirements-writer-skill — score (≥90/100) and refine
    4. feedback loops until all requirements approved

  Outputs land in /req/GLOSSARY.md (shared) and
  /req/{slug}/requirements-set/ (per project).

  HARD RULE: this skill produces requirements artifacts only. It MUST NOT
  modify application source code, configuration, build manifests, database
  schemas, or any file outside /req/ and .req-config.yml. The skill is
  tech-stack agnostic — it works equally well for backend (Laravel,
  Django, Rails, Spring, Express, FastAPI, .NET, Go, etc.), frontend
  (React, Vue, Angular, Svelte), mobile, data pipelines, infra, and
  embedded systems. Even when the user says "implementá X",
  "asigná este permiso", or "add this middleware", the answer is to
  capture the underlying need as a requirement — not to execute the
  change.

applyTo:
  - "user wants to capture or refine requirements"
  - "user wants to conduct a requirements interview"
  - "user describes a need, feature, permission, role, workflow, or bug"
  - "user asks to add, change, or remove source code, config, schema, or build files"
  - "user asks for an implementation that the skill should re-frame as a requirement"
  - user says: "interview requirements"
  - user says: "requirements interview"
  - user says: "generar requisitos"
  - user says: "asigná permisos"
  - user says: "add middleware"
  - user says: "creá un endpoint"
  - user says: "modificá una ruta"
  - pattern: "interview.*requirement"
  - pattern: "requisit|requirement"
  # Generic Spanish: imperative verb + tech entity (covers Laravel/Symfony/Django/etc. vocabulary)
  - pattern: "(asigná|agregá|modificá|cambiá|creá|eliminá|hacé|implementá|agrega|modifica|cambia|crea|elimina|haz|implementa|assign|add|modify|change|create|delete|implement).*(permiso|rol|ruta|middleware|controller|endpoint|route|permission|role|columna|column|campo|field|tabla|table|modelo|model|módulo|module|funcionalidad|feature)"
  # Catch-all for any "implementá/hacé X" that smells like an implementation request
  - pattern: "(implementá|implementa|hacé|haz|hazme|please add|please implement).+(en|a|to|in)\\s+(el\\s+sistema|the\\s+system|la\\s+app|the\\s+app)"

required_companions:
  - grilling-requirements
  - requirements-modeling
  - requirements-writer-skill
optional_companions:
  - seams-test

compatibility: |
  This skill is an orchestrator — it does not work standalone.
  REQUIRED companion skills (must be installed together): grilling-requirements,
  requirements-modeling, requirements-writer-skill. Without them, Phase 1
  (interview), Phase 2 (formalization), and Phase 3 (validation) fail.
  OPTIONAL: seams-test (only for refactoring legacy code without coverage).
  Install the full workflow pack: `npx skills add jagj77/req`.

disable-model-invocation: false

language_detection: |
  Detect project language from project_name (or read from .req-config.yml default):
  - If contains Spanish accents (á, é, í, ó, ú, ñ) → "es"
  - Else → "en"
  - Can override with explicit language parameter: language="es" or language="en"
  - Single execution = single language (no duplicates)
  - Global config: .req-config.yml (default_language, language_detection_strategy)

slug_transformation: |
  Convert project_name to valid directory slug:
  - Convert to lowercase
  - Replace spaces/underscores with hyphens
  - Remove special characters
  - Example: "Búsqueda Avanzada" → "busqueda-avanzada"
  - Example: "Payment Integration" → "payment-integration"

invokes:
  - skill: grilling-requirements
    with_context: [project_name, project_slug, stakeholders, scope, language]
    expect_output: grilling_requirements_output (needs, decisions, ambiguities, terminology, project_slug, language)

  - skill: requirements-modeling
    with_input: [grilling_requirements_output, project_slug, language]
    with_contract: requirements_writer_template_v1
    expect_output: modeling_output (glossary, requirement_candidates, project_slug, language)

  - skill: requirements-writer-skill
    with_input: [requirement_candidates, glossary, project_slug, language]
    expect_output: validation_output (validated_requirements, clarification_requests, quality_scores, project_slug, language)

  - skill: requirements-modeling
    when: "validation_output.any_score < 90"
    type: "feedback_loop"
    with_input: [clarification_request, project_slug, language]
    then_loop: "back to requirements-writer-skill"

# Forwarded to /requirements-modeling so it produces REQ files that already
# satisfy the writer's linter on the first draft. Without this contract,
# /requirements-modeling writes in freeform prose and the writer skill
# rewrites every file in the feedback loop (waste of cycles).
contracts:
  requirements_writer_template_v1:
    frontmatter:
      required_fields: [id, project_slug, language, validated_by, validated_at, score, approved]
      id_format: "REQ-{NNN}"
      validated_by_default: "requirements-writer-skill"
      validated_at_default: null
      score_default: null
      approved_default: false
    sections_required: ["Meta", "Rule", "Rationale", "Glossary Terms Used", "Clauses", "Validation"]
    rule_section:
      shall_count: 1
      single_observable_obligation: true
      avoid_combinators: true
      solution_free: true
      bracketed_terms:
        must_match_glossary_exactly: true
        no_invented_tokens: true
        example_canonical: "[Vista V_INFORME_EMITIDO]"
        example_code_to_avoid: "<schema>.<table_or_view>"
    clauses_section:
      sub_clause_format: "REQ-{NNN}.{M}"
      carries: [acceptance_criteria, file_paths, helper_names, library_choices, bem_tokens, tests]
    validation_section:
      populated_by: "requirements-writer-skill"
      placeholders_until_phase_3: [score, approved, rules_violated, corrections_applied]

---

## Description

  Orchestrate a complete requirements engineering workflow:
  1. Run /grilling-requirements session to extract stakeholder needs
  2. Run /requirements-modeling to formalize requirements
  3. Run /requirements-writer-skill to validate and score
  4. Handle feedback loops until all requirements >= 90/100
  5. Produce final deliverable (GLOSSARY.md [shared], project-slug/requirements-set/)
  6. Support multi-language: Spanish (es) or English (en)


## Orchestration Workflow

This is the primary orchestrator. Do NOT ask user to manually invoke other skills.
Instead, execute automatically in sequence:

**STEP 0: Project Slug Generation & Language Detection**
   - Capture: user's project_name (e.g., "Búsqueda Avanzada")
   - Generate: project_slug (e.g., "busqueda-avanzada")
   - Detect: language from project_name (auto or explicit parameter)
   - Propagate: project_slug + language to all phases
   - All output will use: `/req/{project_slug}/requirements-set/` directory structure in detected language

**STEP 0.1: Bootstrap `.req-config.yml` (only if missing)**
   - Check whether `.req-config.yml` exists at the repo root.
   - If it exists: read it and continue. Do NOT modify it.
   - If it does NOT exist: create it at the repo root with the
     minimal defaults below, then continue. Tell the user:
     "Created `.req-config.yml` with defaults; edit it to override
     `default_language`, `language_detection_strategy`, etc."
   - Minimum defaults (write exactly this content, no extra fields):

     ```yaml
     default_language: "en"
     language_detection_strategy: "auto"
     glossary:
       centralized: true
       path: "GLOSSARY.md"
     requirements:
       naming_pattern: "REQ-{NNN}"
       extension: ".md"
     documentation:
       summary_file: "requirements-summary.md"
       structure_file: "requirements-structure.md"
     validation:
       minimum_quality_score: 90
       check_glossary_consistency: true
       allow_language_mixing: false
     ```

   - Rationale: `skills.sh` / `npx skills add` does not copy files
     from the repo root, only files under each skill directory.
     Without this step, downstream consumers of the pack would have
     to author `.req-config.yml` manually before first run.

1. **Phase 1: Grilling-requirements** - Extract needs through relentless questioning
   - Invoke: `/grilling-requirements` with project context + project_slug + language
   - Questions asked in: detected language (Spanish or English)
   - Collect: needs, decisions, ambiguities, terminology
   - Proceed only when session complete
   - Output includes: project_slug, language for downstream use

2. **Phase 2: Requirements Modeling** - Formalize and structure
   - Invoke: `/requirements-modeling` with grilling output + project_slug + language
   - Update: `/req/GLOSSARY.md` (root-level, shared by all projects, in current language)
   - Create: `/req/{project_slug}/requirements-set/` directory
   - Generate: `/req/{project_slug}/requirements-set/REQ-NNN.md` (single language, e.g., REQ-001.md)
   - Collect: GLOSSARY updates, requirement candidates, in specified language
   - Ensure: no contradictions between requirements

   **2.1 Phase Template Contract (MANDATORY).** Every REQ file generated in this phase MUST
   already comply with the writer skill's `## Rule` template — the linter's Hard Check 0
   is the contract, not a target to retrofit later. The required structure is:

   ```yaml
   ---
   id: REQ-{NNN}                     # matches filename REQ-NNN-{slug}.md
   project_slug: {project_slug}
   language: es | en                 # detected by Phase 0
   validated_by: requirements-writer-skill
   validated_at: null               # populated in Phase 3
   score: null                      # populated in Phase 3
   approved: false                  # flipped to true in Phase 3
   ---
   ```

   - `## Meta` — `requirement_id`, `project_slug`, `language`, `verification_method`.
   - `## Rule` — EXACTLY ONE `SHALL` sentence. State the observable behavior in plain
     prose; do NOT bundle multiple obligations with `y`. Do NOT name helper functions,
     library names, file paths, exact JSON keys, or BEM tokens inside `## Rule` — those
     belong in `## Clauses`. Every `[bracketed]` token MUST match an entry in
     `/req/GLOSSARY.md` exactly (use `[Rol REPORTE]`, never `Role::REPORTE`; use
     `[Vista V_INFORME_EMITIDO]`, never the raw `<schema>.<view>` glyph).
   - `## Rationale` — short justification (3-5 sentences) of why this approach.
   - `## Glossary Terms Used` — list of `[bracketed]` terms referenced in `## Rule`.
   - `## Clauses` — sub-clauses `REQ-NNN.M` carrying acceptance criteria, file paths,
     helper names, library choices, BEM tokens, tests, etc. (the "how").
   - `## Validation` — leave `score`, `approved`, `rules_violated`, `corrections_applied`
     as placeholders; Phase 3 populates them.

   **2.2 Hard Check 0 quality gate (MANDATORY before Phase 3).** Before transitioning
   to Phase 3, run `python .agents/skills/requirements-writer-skill/scripts/lint-requirement.py
   /req/{slug}/requirements-set/REQ-NNN-{slug}.md` on every REQ. If Hard Check 0
   fails (missing front-matter, multiple SHALLs, bracketed terms not in GLOSSARY,
   malformed meta block), Phase 2 MUST re-write the REQ before Phase 3 starts.
   Re-writing is the responsibility of `/requirements-modeling`, not the writer.
   Phase 3 (writer) only scores C1-C9 + R1-R41; it MUST NOT be the place where the
   template is fixed.

   **2.3 One sub-requirement per file.** A REQ is one observable obligation in
   `## Rule`. Sub-clauses (`## Clauses`) carry the detail. If a candidate
   requirement bundles multiple observable obligations, split it into multiple
   REQ-NNN files in this phase — do not defer to Phase 3.

   **2.4 Use of `[bracketed]` glossary references (HINT).** When drafting `## Rule`,
   run `grep -E '^\| \[' /req/GLOSSARY.md | awk -F'|' '{print $2}'` first to list
   every canonical term. Copy the exact spelling from the table — including
   parentheses, accents, and suffixes like `(existente)`, `(vista Ciclo de Auditoría)`.
   Do not invent bracketed tokens that are not in the glossary.

3. **Phase 3: Validation** - Score and verify
   - Invoke: `/requirements-writer-skill` with requirement candidates + project_slug + language
   - Read: `/req/GLOSSARY.md` (centralized, root-level, in detected language)
   - Check: all requirements scored >= 90/100
   - Feedback messages in: detected language
   - If any score < 90: Identify ambiguities

   **3.1 Phase 3 assumes Phase 2 template contract is satisfied.** The writer skill
   scores substance (C1-C9 + R1-R41). If Hard Check 0 fails at this point, the
   orchestrator MUST return to Phase 2 to fix the template, not invoke the writer
   in a loop. The writer only re-scores; it MUST NOT silently rewrite `## Rule` to
   bypass the gate.

4. **Phase 4: Feedback Loops** - Iterate on low scores
   - For each requirement scored < 90:
     - Invoke: `/requirements-modeling` with clarification request + project_slug + language
     - Wait: for updated `/req/GLOSSARY.md` (root-level, same language)
     - Invoke: `/requirements-writer-skill` again (re-evaluation) + project_slug + language
     - Repeat until all >= 90

5. **Phase 5: Consolidation** - Produce final deliverable
   - Verify: `/req/GLOSSARY.md` (root-level) completeness in current language
   - Create: `/req/{project_slug}/requirements-set/requirements-summary.md` (in current language)
   - List: all approved requirements (score >= 90) in `/req/{project_slug}/requirements-set/` (single language)
   - Report: "Requirements engineering complete for '{project_name}' (language: {language}). Output in: /req/{project_slug}/"

**Multi-Language Support (Single Language per Execution):**
- ✅ Questions in grilling-requirements: Spanish (es) or English (en)
- ✅ GLOSSARY.md: Single source, entries in current language only
- ✅ REQ-NNN.md: No language suffix (single language per run)
- ✅ All feedback: In current language
- ✅ Configuration: .req-config.yml defines default_language

**Never skip phases. Always complete each phase before moving to next.**
**GLOSSARY.md is centralized at /req/GLOSSARY.md (shared by all projects, single language per execution).**
**Each project uses its own /req/{project_slug}/requirements-set/ directory with single-language files.**

### Backward compatibility & legacy grandfathering

The Phase 2 Template Contract and the Hard Check 0 quality gate apply **forward only**,
starting from the next run of this skill. They MUST NOT be retroactively enforced on
existing validated projects.

Concretely:

- A REQ file is **legacy** when its filename matches one of these existing patterns
  AND it predates this version of the skill (or carries no `validated_by` front-matter
  field):
  - `req/{slug}/requirements-set/REQ-NNN-{slug}.md` without `## Rule` section
  - `req/{slug}/requirements-set/REQ-NNN-{slug}.md` with multi-clause `REQ-NNN.M`
    sub-sections but no YAML front-matter
- The `/requirements-writer-skill` MUST be invoked on legacy REQs only if the user
  explicitly requests re-validation. By default the orchestrator treats legacy REQs
  as **grandfathered** — already approved, do not re-lint, do not break the build.
- New sub-requirements added to a legacy project MAY mix styles: new files use the
  template contract, old files keep their format. The `requirements-summary.md` for
  that project MUST declare which REQs are legacy vs templated.
- If the user explicitly asks to migrate a legacy project to the new template, that
  is a separate change and MUST be tracked as such in the summary (do not silently
  rewrite).


## Hard Rules (Non-Negotiable)

This skill is a **requirements engineering** orchestrator. It produces
requirement artifacts only. It MUST NOT modify application code,
configuration files, or any non-requirements file — even when the user
asks for implementation directly.

### Allowed file outputs (only these)

| Path | Purpose |
|---|---|
| `/req/GLOSSARY.md` | Shared glossary (root-level) |
| `/req/{slug}/requirements-set/REQ-NNN.md` | Per-requirement files |
| `/req/{slug}/requirements-set/requirements-summary.md` | Final summary |
| `/req/{slug}/docs/adr/NNNN-*.md` | NEW ADRs only |
| `.req-config.yml` | Project-level config (at repo root) |

### Forbidden actions

These rules apply to **any** tech stack (Laravel, Symfony, Django,
Rails, Spring, Express, FastAPI, .NET, Go, React, Vue, Angular,
Svelte, mobile, data pipelines, infra, embedded, etc.). The skill is
tech-stack agnostic — it produces requirements, never implementation.

- ❌ Modify any source code, configuration, build manifest, schema,
  migration, test file, infrastructure-as-code file, or any other
  non-requirements file. Concretely this includes (non-exhaustive):
    - Any backend source tree (`app/`, `src/`, `lib/`, `internal/`,
      `pkg/`, `cmd/`, `services/`, `controllers/`, `models/`,
      `routes/`, `middleware/`, etc.).
    - Any frontend source tree (`client/`, `web/`, `ui/`,
      `components/`, `pages/`, `views/`, `composables/`, etc.).
    - Any configuration (`config/`, `settings/`, `.env*`,
      `application.{yml,yaml,properties}`, `appsettings.json`, etc.).
    - Any package / build manifest (`package.json`, `composer.json`,
      `requirements.txt`, `pyproject.toml`, `Pipfile`, `pom.xml`,
      `build.gradle*`, `Cargo.toml`, `go.mod`, `Gemfile`, `*.csproj`,
      `*.sln`, `pubspec.yaml`, etc.).
    - Any test tree (`tests/`, `test/`, `__tests__/`, `spec/`,
      `*.test.*`, `*.spec.*`, etc.).
    - Any DB schema, migration, ORM model, or seed file.
    - Any `Dockerfile`, `docker-compose.*`, IaC (`*.tf`, `*.yaml` for
      k8s/ansible), CI config (`.github/workflows/*`,
      `.gitlab-ci.yml`, etc.).
- ❌ Run any install / build / migrate / deploy / lint / format command
  (`composer require`, `npm install`, `pip install`, `bundle install`,
  `cargo build`, `dotnet restore`, `artisan migrate`, `rails db:migrate`,
  `python manage.py migrate`, `npm run build`, `make deploy`,
  `pnpm i`, `yarn add`, `go mod tidy`, etc.).
- ❌ Run `git commit`, `git push`, branch creation, or open a PR /
  MR — those are downstream concerns, not the skill's job.
- ❌ Treat a user request as an implementation ticket and execute it
  ("asigná este permiso", "add this middleware", "creá este controller",
  "add an endpoint POST /foo", "filter this query by org"). The
  underlying need is a requirement; capture it via the workflow.
- ❌ Replace or overwrite existing project documentation under
  `docs/`, `README*`, `CONTEXT*`, or anywhere else outside `/req/`.
  Only CREATE new artifacts under `/req/{slug}/docs/adr/`.

### Trigger detection: "is this a requirements problem?"

Almost every product/code request is a requirements problem in disguise.
The re-framing pattern is **tech-stack agnostic** — the examples below
span multiple stacks (Laravel, Django, Express, generic SQL, frontend
forms, etc.) to illustrate the universal shape:

`"do X to Y"` → `"The system SHALL [capability] for [actor] under [scope]."`

| User says (literal) | Re-frame as requirement |
|---|---|
| "Assign X permission to Y role to view reports" | "The system SHALL allow [actor] to [action] on [resource] within [scope]." |
| "Add this middleware/guard to route Z" | "The system SHALL restrict access to [endpoint] to users with [roles/conditions]." |
| "Add a column to table T" | "The system SHALL persist [field] per [entity]." |
| "Add a field to form F" | "The system SHALL capture [field] during [process]." |
| "Make the API return JSON instead of XML" | "The system SHALL respond to [endpoint] with Content-Type [type]." |
| "Implement a two-step approval flow" | "The system SHALL require approval from [N] distinct [role] before [action]." |
| "Expose POST /foo that takes a JSON body" | "The system SHALL expose POST /foo with the documented request/response contract." |
| "Filter the listing by the user's organization" | "The system SHALL scope [listing] to records belonging to the user's [org/unit]." |
| "Send an email when X happens" | "The system SHALL notify [recipient] via [channel] when [event] occurs." |

If you catch yourself reaching for `Edit`/`Write`/`Bash` on a non-`/req/`
file, STOP. Re-frame the user request as a requirement and continue
with the workflow.

### Self-check before each phase

Before transitioning from grilling → modeling → writer → consolidation,
verify no source files were touched by accident:

```bash
git status --short -- ':!req' ':!.req-config.yml'
```

If anything outside `/req/` and `.req-config.yml` shows up, revert it
immediately with `git checkout -- <path>` and warn the user. NEVER
commit those changes.

---

## Failure recovery

If the skill is invoked but the user already asked for implementation
in the same turn and the orchestrator started modifying code:

1. STOP executing further edits.
2. Run `git checkout -- <file>` for every out-of-scope path that was
   touched.
3. Acknowledge to the user: "I started touching source code; I should
   have captured that as a requirement instead. Reverting and resuming
   the requirements workflow."
4. Continue with STEP 0 (slug + language detection) and Phase 1
   (grilling-requirements).
