# Domain Glossary (lazy)

This file is **lazily populated** by the `feature-slice-review` skill when grilling produces a term that survives. It is not pre-authored.

The skill creates the file on first write. Until then, this stub is the only content.

## Format

When the skill (or any other agent) adds a term, the format is:

```
## Bounded contexts

- **<Name>**: <one-sentence definition>. Owns: <list of file paths or namespaces>.
  Anti-corruption layer: <yes/no, with the external system>.
  Shared kernel: <yes/no, with the names of the shared concepts>.
```

## Why lazy

The skill's job is to surface gaps, not invent them. A pre-authored glossary would tempt the skill to fit the codebase into the author's pre-existing mental model. Instead, the skill asks the user for the term when none of the scout's signals or the project's existing docs supply one.
